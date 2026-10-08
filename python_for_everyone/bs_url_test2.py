import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors for https
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

todo = list()
visited = list()
url = input('Enter - ')
count = int(input('How many to retrieve - '))
pos = int(input('position: '))

while count > 0:
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    lst=list()
    for tag in tags:
        lst.append(tag.get('href', None))  # Appends all the links to lst
    url = lst[pos-1] #might need -1 later
    count = count - 1
    print("Retrieving:", url)