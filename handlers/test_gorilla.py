import base64
from io import BytesIO
import json

import pytesseract

from PIL import Image

from mitmproxy.http import HTTPFlow

from handlers.llm_model import have_image, remove_tags, ask_pipeline


def api_candidatures_questions_next(flow: HTTPFlow):

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

    return flow
