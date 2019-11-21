# import libraries
import csv

import requests
from bs4 import BeautifulSoup

# create a file to write to, add headers rows
f = csv.writer(open('z-artist-names.csv', 'w'))
f.writerow(['Name', 'Link'])

pages = []

for i in range(1,5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

for item in pages:
    page = requests.get(item)


    # Collect first page of artists’ list
    #page = requests.get('https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ1.htm')

    # create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # remove bottom links
    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    # pull all text from the BodyText div
    artist_name_list = soup.find(class_='BodyText')

    # pull text from all instances of <a> tag within BodyText div
    artist_name_list_items = artist_name_list.find_all('a')

    # use .contents to pull out the <a> tag's children
    for artist_name in artist_name_list_items:
        names = artist_name.contents[0]
        links = 'https://web.archive.org' + artist_name.get('href')
        print(names)
        print(links)
        f.writerow([names, links])
