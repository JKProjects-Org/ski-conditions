import requests
from bs4 import BeautifulSoup

# first look at onthesnow's terrain report to get:
# trails open/ trails total
# lifts open/ lifts total
url_terrain = 'https://www.onthesnow.com/colorado/keystone/skireport.html'
page = requests.get(url_terrain)

# create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# look for block of html that contains relevant info
keystone_summary = soup.find(id = 'resort_terrain')

# store all values in class = 'open value'
keystone_open = keystone_summary.find_all(class_ = 'open value')

# print text of each item where class = 'open value'
for item in keystone_open:
    print(item.get_text())

keystone_trails_open = keystone_open[0].get_text()
keystone_lifts_open = keystone_open[1].get_text()

#print(keystone_summary.prettify())

# look at onthesnow's ski resort home page to get:
# percent of greens open
# percent of blues open
# percent of blacks and double blacks open
url_terrain_percent = 'https://www.onthesnow.com/colorado/keystone/ski-resort.html'
page = requests.get(url_terrain_percent)

# create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# look for block of html that contains relevant info
keystone_percent = soup.find(class_ = 'rt_trail diamonds')

# get stuff from each difficulty class
keystone_percent_green = keystone_percent.find(class_ = 'value beginner').get_text()
keystone_percent_blue = keystone_percent.find(class_ = 'value intermediate').get_text()
keystone_percent_black = keystone_percent.find(class_ = 'value advanced').get_text()
keystone_percent_double_black = keystone_percent.find(class_ = 'value expert').get_text()

print(keystone_percent_green)
print(keystone_percent_blue)
print(keystone_percent_black)
print(keystone_percent_double_black)

# report
print('Keystone Ski Conditions:\n')
print(f'{keystone_trails_open} trails open')
print(f'{keystone_lifts_open} lifts open')
print(f'Beginner Runs: {keystone_percent_green}')
print(f'Intermediate Runs: {keystone_percent_blue}')
print(f'Advanced Runs: {keystone_percent_black}')
print(f'Expert Runs: {keystone_percent_double_black}')



















