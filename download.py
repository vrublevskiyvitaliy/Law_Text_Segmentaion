__author__ = 'vitaliyvrublevskiy'


url = 'https://www.lawinsider.com/contracts/1UvT1mgEAKfaPL5IUpNk6Q.docx'
import requests
from requests.auth import HTTPBasicAuth


cookie = {
    '__cfduid' : 'd4a23cb5a2d676396be7fd88a0b82b78f1505115716',
    'session' : 'eyJjc3JmIjoiYlZINGFPb0kxNXlnN3V1cXFveUlYaCJ9|1505115716|eff56d3da7623bd2aef4f8d43247ef75bcd75f2d',
    'ajs_anonymous_id' : '%22e709dd72-97e4-444f-b685-73913b836bb8%22',
    'csrf' : 'bVH4aOoI15yg7uuqqoyIXh',
    'auth' : '"eyJfdXNlciI6WzU2Nzc1ODY3MDUyODUxMjAsMSwiZHZQV0JLQWtydlRsT0hhaGRTNUdaSSIsMTUwNTM4OTg5MSwxNTA1Mzg5ODkxLCJWaXRhbGlpIFZydWJsZXZza3lpIiwwXX0\075|1505389892|a7f849e25b4c11e40dbb2eb028f98296b5c4360e"',
    '_ga' : 'GA1.2.923972133.1505115718',
    '_gid' : 'GA1.2.857001817.1505295653',
    'v' : '34',
    'ajs_user_id' : 'null',
    'ajs_group_id' : 'null',
    '_gat' : '1'
}

response = requests.get(url, cookies=cookie)
if response.status_code == 403:
    print 'Fuck'
else:
    # response = requests.get(url, auth=HTTPBasicAuth('yakymiv1995@gmail.com', '123456'))
    f = open('file.docx','w')
    print response.content
    f.write(response.content)