__author__ = 'vitaliyvrublevskiy'


url = 'https://www.lawinsider.com/contracts/1UvT1mgEAKfaPL5IUpNk6Q.docx'
import requests

cookie = {
    '__cfduid' : 'd4a23cb5a2d676396be7fd88a0b82b78f1505115716',
    'session' : 'eyJjc3JmIjoiYlZINGFPb0kxNXlnN3V1cXFveUlYaCJ9|1505115716|eff56d3da7623bd2aef4f8d43247ef75bcd75f2d',
    'ajs_anonymous_id' : '%22e709dd72-97e4-444f-b685-73913b836bb8%22',
    'csrf' : 'bVH4aOoI15yg7uuqqoyIXh',
    'auth' : '"eyJfdXNlciI6WzU2Nzc1ODY3MDUyODUxMjAsMSwiZzNlN05sU2U1bmJWR2VBOGV1YkY0byIsMTUwNTI5NTY1MSwxNTA1Mzc4NjU5LCJWaXRhbGlpIFZydWJsZXZza3lpIiwwXX0\075|1505379129|06c4dbbd97fcda18736dc32a9851bebd75299725"',
    '_ga' : 'GA1.2.923972133.1505115718',
    '_gid' : 'GA1.2.857001817.1505295653',
    'v' : '31',
    'ajs_user_id' : 'null',
    'ajs_group_id' : 'null',
    '_gat' : '1'
}

response = requests.get(url, cookies=cookie)
f = open('file.docx','w')

f.write(response.content)