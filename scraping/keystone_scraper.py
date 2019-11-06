import requests
from bs4 import BeautifulSoup

url = 'https://www.keystoneresort.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'
page = requests.get(url)

# check if page retrieved. should output 200
print(page.status_code)

# create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')
'''
# search for class terrain_summary__tab_main__text
trails_summary = soup.find(class_ = 'terrain_summary__tab_main__text')
'''
# search for class c118__number1--v1
trails_summary = soup.find(class_ = 'terrain_summary row')

# look for stuff in <span> tags
trails_summary_items = trails_summary.find_all('span')

# get text from span tags
for item in trails_summary_items:
    print(item.get_text())

print(trails_summary.prettify())
print(trails_summary)
print(trails_summary_items)

