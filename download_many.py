
import requests

import json
import random
import time
from pathlib import Path


def random_wait():
    time.sleep(random.randint(3, 10))


def download_docx_contracts(contracts_ids, contracts_num):
    cookie = {
        '__cfduid': 'd4a23cb5a2d676396be7fd88a0b82b78f1505115716',
        'session': 'eyJjc3JmIjoiYlZINGFPb0kxNXlnN3V1cXFveUlYaCJ9|1505115716|eff56d3da7623bd2aef4f8d43247ef75bcd75f2d',
        'ajs_anonymous_id': '%22e709dd72-97e4-444f-b685-73913b836bb8%22',
        'csrf': 'bVH4aOoI15yg7uuqqoyIXh',
        'auth': '"eyJfdXNlciI6WzU2Nzc1ODY3MDUyODUxMjAsMSwiUm4wdFJ6MXRIRXg5YmppMUxjZWhEeiIsMTUwNjc2MDEzNSwxNTA2NzYwMTM1LCJWaXRhbGlpIFZydWJsZXZza3lpIiwwXX0\075|1506760144|c52efcc5f99048d842dbdf8025629135b47d5dc4"',
        '_ga': 'GA1.2.923972133.1505115718',
        '_gid': 'GA1.2.857001817.1505295653',
        'v': '42',
        'ajs_user_id': 'null',
        'ajs_group_id': 'null',
        '_gat': '1'
    }

    ind = 0
    for contract_id in contracts_ids:
        if (ind == contracts_num):
            break
        url = 'https://www.lawinsider.com/contracts/' + contract_id + '.docx'
        path = 'documents/' + contract_id + '.docx'

        file = Path(path)
        if not file.is_file():
            response = requests.get(url, cookies=cookie)
            print url
            if response.status_code == 403:
                print 'Fuck'
            else:
                f = open('documents/' + contract_id + '.docx', 'w')
                f.write(response.content)
                    # print response.content
        else:
            print('Already have')
        ind += 1


def get_contracts_ids():
    with open('short.json') as data_file:
        data = json.load(data_file)

    contracts_ids = []

    for contract in data:
        contracts_ids.append(contract['data']['id'])

    return contracts_ids


contracts_ids = get_contracts_ids()
download_docx_contracts(contracts_ids, 10)