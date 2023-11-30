import re
import base64
import os
from pprint import pprint
from time import sleep

import openai
import requests
from io import BytesIO
import json

import pytesseract
from dotenv import load_dotenv
from mitmproxy import http

from PIL import Image

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


API_URL = "https://api-inference.huggingface.co/models/rsvp-ai/bertserini-bert-base-squad"


def ask_gpt3(question, context_answers):
    prompt = """
    Given the following question and answers:
    User: Question: {question}
    User: Answers: {context_answers}
    System: Simply answer the question without giving any explanation or context
    """

    prompt = prompt.format(question=question, context_answers=context_answers)

    res = openai.ChatCompletion.create(model="davinci", messages=[{"role": "system", "content": prompt}])

    return res


def ask_pipeline(element_dict):
    headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}", "Content-Type": "application/json"}
    image_context = element_dict.get('image_context', '') or ' '
    question = element_dict['question_text']
    context_answers = element_dict['answers']
    options_string_question = '\n'.join([f'Option {i+1}: {answer}' for i, answer in enumerate(context_answers)])
    options_string_question = options_string_question + '\n'
    payload = {
        "inputs": {"question": f'{question}. {image_context}.', "context": options_string_question},
        "parameters": {
            "temperature": 0.0,
            "top_p": 0.9,
            "top_k": 50,
            "length_penalty": 0.2,
            "no_repeat_ngram_size": 3,
            "beam_search": 5,
            "early_stopping": True,
            "wait_for_model": True,
        },
    }

    try:
        json_response = None
        while not json_response:
            res = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            json_response = res.json()

            json_response = sorted(json_response, key=lambda x: x['score'], reverse=True)[0]
            if 'loading' in json_response.get('error', ''):
                print("Model is still loading...", json_response)
                sleep(10)
        element_dict['final_answer'] = json_response
        pprint(element_dict)
        return json_response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def remove_tags(content):
    content = content.replace('<p>', '').replace('</p>', '').replace('&nbsp;', ' ').replace('<br>', '')
    clean = re.compile('<.*?>')
    return re.sub(clean, '', content)


def have_image(content):
    return content.find('<img src="data:image/png;base64') > -1


def request(flow: http.HTTPFlow):
    if "/api/candidatures/anticheating/" in flow.request.path:
        resp = flow.response
        if not resp:
            return
        flow.response.content = '{"is_left_screen":false}'.encode('utf-8')
        print("[************] Dropping request")
        return flow


def response(flow: http.HTTPFlow):
    responses = []
    if "/api/candidatures/questions/next/" in flow.request.path:

        def process_response_data(content):
            if not content:
                return

            d = json.loads(content)

            for d in d:
                el_dt = {}

                text = d.get('text')
                has_image = have_image(text)

                if has_image:
                    el_dt['image_context'] = extract_image_text(text)

                question = remove_tags(text)
                el_dt['question'] = question
                answers = [remove_tags(i.get('text')) for i in d.get('context').get('answers')]
                el_dt['answers'] = answers
                question_text = question[: question.find('<img src="data:image/png;base64')]
                el_dt['question_text'] = remove_tags(question_text)

                final_answer = ask_pipeline(el_dt)
                el_dt['final_answer'] = final_answer

                yield el_dt

        def extract_image_text(text):
            image_src = text[text.find('<img src="data:image/png;base64') :]
            image_content = image_src[image_src.find('base64,') + 7 :]
            image_binary = image_content.encode('utf-8')

            try:
                im = Image.open(BytesIO(base64.b64decode(image_binary)))
                image_text = pytesseract.image_to_string(im)
            except Exception as e:
                print(f"Error processing image: {e}")
                image_text = None

            return image_text

        responses = []
        for e_data in process_response_data(flow.response.content):
            responses.append(e_data)

    if responses:
        with open('gorilla_test.json', 'w') as f:
            json.dump(responses, f, indent=4, sort_keys=False)
        print("[************] Wrote responses to file")

    return flow


if __name__ == '__main__':
    from mitmproxy.tools.main import mitmdump

    mitmdump(['-p', '8081', '-s', __file__])
