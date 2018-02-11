import json
import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib'))

import requests

QIITA_BASE_URL = os.environ['QIITA_BASE_URL']


def run(event, context):
    page = 1

    result = []
    is_loop = True
    print(event)
    while is_loop:
        url = QIITA_BASE_URL.format(user_id = event['name'], page = page)
        result = requests.get(url)
        page+=1
        if len(result) == 0:
            is_loop = False

    return "SUCCESS"

