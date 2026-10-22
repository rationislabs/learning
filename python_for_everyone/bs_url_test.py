from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()

url = input('Enter - ')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

sum_list = []

# Retrieve all of the anchor tags
tags = soup('span')
for tag in tags:
    # Look at the parts of a tag
    #print('TAG:', tag)
    #print('URL:', tag.get('href', None))
    print('Contents:', tag.contents[0])
    sum_list.append(int(tag.contents[0]))

final_sum = sum(sum_list)
print(final_sum)
    #print('Attrs:', tag.attrs)