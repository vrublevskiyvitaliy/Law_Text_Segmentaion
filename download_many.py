
import requests

import json
import random
import time
from pathlib import Path


def random_wait():
    time.sleep(random.randint(2, 7))


def get_bad_docx():
    with open('bad_docx.json') as data_file:
        data = json.load(data_file)
    return data

def download_docx_contracts(contracts_ids, contracts_num):
    cookie = {
        '__cfduid': 'd4a23cb5a2d676396be7fd88a0b82b78f1505115716',
        'session': 'eyJjc3JmIjoiYlZINGFPb0kxNXlnN3V1cXFveUlYaCJ9|1505115716|eff56d3da7623bd2aef4f8d43247ef75bcd75f2d',
        'ajs_anonymous_id': '%22e709dd72-97e4-444f-b685-73913b836bb8%22',
        'csrf': 'bVH4aOoI15yg7uuqqoyIXh',
        'auth': 'eyJfdXNlciI6WzU2Nzc1ODY3MDUyODUxMjAsMSwiSVJ2RGdFR2FqcXJJYzVkTGJGUXdRNyIsMTUwODA5MTc3NywxNTA4MDkxNzc3LCJWaXRhbGlpIFZydWJsZXZza3lpIl19|1508091782|7f657355f2b2b306d028123ce739649fb8a8a675',
        '_ga': 'GA1.2.923972133.1505115718',
        '_gid': 'GA1.2.1020241738.1506851128',
        'v': '60',
        'ajs_user_id': 'null',
        'ajs_group_id': 'null',
        '_gat': '1'
    }

    # cookie = {
    #     # '__cfduid': 'd4a23cb5a2d676396be7fd88a0b82b78f1505115716',
    #     # 'session': 'eyJjc3JmIjoiYlZINGFPb0kxNXlnN3V1cXFveUlYaCJ9|1505115716|eff56d3da7623bd2aef4f8d43247ef75bcd75f2d',
    #     # 'ajs_anonymous_id': '%22e709dd72-97e4-444f-b685-73913b836bb8%22',
    #     # 'csrf': 'bVH4aOoI15yg7uuqqoyIXh',
    #     'auth': 'eyJfdXNlciI6WzU3NjE5MzUwODE0NzIwMDAsMCwiaFZjNlhZTGJ3TWdjekJMNnRlWjk5OCIsMTUwODA3NjYxMCwxNTA4MDc2NjEwLG51bGxdfQ\075\075|1508076621|7e825751cf3965bd4f4fa1b089fa63ab831907ef',
    # }


    bad_docx = get_bad_docx()
    ind = 0
    for contract_id in contracts_ids:
        if contract_id + '.docx' in bad_docx:
            print('Found bad docx')
            continue
        print (str(ind))
        if (ind == contracts_num):
            break
        url = 'https://www.lawinsider.com/contracts/' + contract_id + '.docx'
        path = 'documents/' + contract_id + '.docx'

        file = Path(path)
        if not file.is_file():
            random_wait()
            response = requests.get(url, cookies=cookie)
            print url
            if response.status_code == 403:
                print 'Fuck'
            else:
                f = open('documents/' + contract_id + '.docx', 'w')
                f.write(response.content)
                ind += 1
                    # print response.content
        else:
            print('Already have')
        #ind += 1


def get_contracts_ids():
    with open('1.json') as data_file:
        data = json.load(data_file)

    contracts_ids = []

    for contract in data:
        contracts_ids.append(contract['data']['id'])

    return contracts_ids


contracts_ids = get_contracts_ids()
download_docx_contracts(contracts_ids[1000:], 50)