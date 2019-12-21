import requests
from bs4 import BeautifulSoup

url = 'https://www.keystoneresort.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'
page = requests.get(url)

# check if page retrieved. should output 200
#print('page status code: ', page.status_code)

# create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')
'''
# search for class terrain_summary__tab_main__text
trails_summary = soup.find(class_ = 'terrain_summary__tab_main__text')
'''
# search for class c118__number1--v1
trails_summary = soup.find(class_ = 'terrain_summary row')

# look for stuff in <span> tags
trails_summary_items = trails_summary.find_all(class_= 'c118__number1--v1')

# look for trail and lift totals
trail_totals = trails_summary.find_all(class_='c118__number2--v1')

# get text from span tags
for item in trails_summary_items:
    print(item.get_text())

for item in trail_totals:
    print(item.get_text())

total_trails = trail_totals[2].get_text()
total_lifts = trail_totals[3].get_text()

acres_open = trails_summary_items[0].get_text()
terrain_percent = trails_summary_items[1].get_text()
trails_open = trails_summary_items[2].get_text()
lifts_open = trails_summary_items[3].get_text()

# report
print(f'Acres Open: {acres_open}')
print(f'Terrain Open: {terrain_percent}%')
print(f'Trails Open: {trails_open}{total_trails}')
print(f'Lifts Open: {lifts_open}{total_lifts}')

# look for status of specific lift, ex. Montezuma Express
# revisit this..need to look inside <script>
#lift_status = soup.find(class_= 'column--left')
#print(lift_status)
'''
lift_status = soup.find(class_= 'liftStatus__statusPanel togglePanel panelOpen')
lift_status = lift_status.find(class_='liftStatus__lifts row')
print(lift_status)
lift_status_left = lift_status.find(class_= 'column--left')
print(lift_status_left)
lift_status_items = lift_status_left.find_all(class_ = 'liftStatus__lifts__row c118__name--v1')
print(lift_status_items)
for item in lift_status_left:
    lift_name = item.find(class_='liftStatus__lifts__row--name').get_text()
    print(lift_name)
    status = item.find_all(class_ = 'sr-only')
    print(status)
    
    #if item.find(class_='liftStatus__lifts__row--name').get_text() == 'Montezuma Express':
    #status = item.find_all(class_='sr-only')
    #status = status[1].get_text()
    #print('Montezuma Express is ', status)

'''


'''
print(trails_summary.prettify())
print(trails_summary)
print(trails_summary_items)
'''
