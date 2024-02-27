import re
import os
from pprint import pprint

from time import sleep

import requests


HUGGING_FACE_API_URL = os.getenv(
    "HUGGING_FACE_API_URL",
    "https://api-inference.huggingface.co/models/rsvp-ai/bertserini-bert-base-squad"
)


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
            res = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload, timeout=30)
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
