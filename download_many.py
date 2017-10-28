
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
        'auth': 'eyJfdXNlciI6WzU3NjE5MzUwODE0NzIwMDAsMCwiUG9OTVhnNWo4OVM1S045UU90RnE5TSIsMTUwODc0NzI3NCwxNTA4NzQ3Mjc0LG51bGxdfQ\075\075|1508747280|afaf02f5eb311ae7a3d81f8d6efd229385fb8230',
    }

    cookie = {
        'auth': 'eyJfdXNlciI6WzU2Nzc1ODY3MDUyODUxMjAsMSwiMXBQMnJUcEw0OU5LYXpTa3kwY0oxMSIsMTUwODc1MTI5MCwxNTA4NzUxMjkwLCJWaXRhbGlpIFZydWJsZXZza3lpIl19|1508751294|b44520043e9ce95397453a2a19699fd759910356',
    }


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
download_docx_contracts(contracts_ids[1000:], 48)