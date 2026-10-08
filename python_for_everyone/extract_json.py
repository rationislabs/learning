"""
import json

data = '''
[
  { "id" : "001",
    "x" : "2",
    "name" : "Chuck"
  } ,
  { "id" : "009",
    "x" : "7",
    "name" : "Brent"
  }
]'''

info = json.loads(data)
print('User count:', len(info))

for item in info:
    print('Name', item['name'])
    print('Id', item['id'])
    print('Attribute', item['x'])
"""

import urllib.request, urllib.parse, urllib.error
import json
import xml.etree.ElementTree as ET

url = 'http://py4e-data.dr-chuck.net/comments_2358702.json'

req = urllib.request.urlopen(url).read().decode('utf-8') 

char_count = len(req)

data = json.loads(req) 


sum_list = []
for item in data['comments']:
    sum_list.append(item['count'])

print('Sum:', sum(sum_list))