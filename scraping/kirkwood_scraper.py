
def ski_scraper(url):
    '''
    Inputs:
    url: string; URL of resort to scrape
    --------
    Returns:
    total_trails: string; total trails in resort
    total_lifts: string; total lifts in resort
    acres_open: int; current acres open in resort
    terrain_percent: int; current percent of terrain open
    trails_open: int; current number of trails open
    lifts_open: int; current number of lifts open

    '''
    from bs4 import BeautifulSoup
    import requests
    
    page = requests.get(url)

    # check if page retrieved. should output 200
    #print('page status code: ', page.status_code)

    # create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # search for class terrain_summary row
    trails_summary = soup.find(class_ = 'terrain_summary row')

    # look for open data in class c118__number1--v1
    trails_summary_items = trails_summary.find_all(class_= 'c118__number1--v1')

    # look for trail and lift totals in class c118__number2--v1
    trail_totals = trails_summary.find_all(class_='c118__number2--v1')

    print(trails_summary_items)
    print(trail_totals)

    # assign text to variables
    #total_trails = trail_totals[3].get_text()[2:]
    #total_lifts = trail_totals[1].get_text()[2:]

    # assign ints to variables
    acres_open = int(trails_summary_items[1].get_text())
    terrain_percent = int(trails_summary_items[0].get_text())
    #trails_open = int(trails_summary_items[3].get_text())
    #lifts_open = int(trails_summary_items[1].get_text())

    #return total_trails, total_lifts, acres_open, terrain_percent, trails_open, lifts_open
    return acres_open, terrain_percent

def trails_report(url):
    from bs4 import BeautifulSoup
    import json
    import re
    import requests

    page = requests.get(url)

    # create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    pattern = re.compile("FR.TerrainStatusFeed = ({.*})")
    regex_find = soup.find_all('script',text=pattern)
    print(type(regex_find))
    print('len', len(regex_find))
    # has words for Status, Type. ex. Status = Open, Type = Black
    regex_find_item = regex_find[1].text
    # has numbers for Status. ex. Status = 0 or 1
    lift_report = regex_find[0].text

    terrain_status = re.findall(pattern, regex_find_item)[0]
    json_data = json.loads(terrain_status)
    #print('lifts', json_data['Lifts'])
    sunrise_dict = json_data['Lifts'][3]
    lifts_words = json_data['Lifts']
    json_trails = json_data['GroomingAreas']
    print(f"{sunrise_dict['Name']}, Status: {sunrise_dict['Status']}")

    lift_numbers = re.findall(pattern, lift_report)[0]
    json_data = json.loads(lift_numbers)
    json_lifts = json_data['Lifts']
    # GroomingAreas = [{frontside,runs[]}, {backside,runs[]}]
    # to make applicable to all resorts, go through each element in GroomingAreas list
    trails_open = 0
    total_trails = 0
    blacks_open = 0
    for area in json_trails:
        # tally runs in this area, ex. frontside
        area_runs = area['Runs']
        for run in area_runs:
            if run['IsOpen']:
                trails_open += 1
                
                if run['Type'] == 'Black' or run['Type'] == 'DoubleBlack':
                    blacks_open += 1
            total_trails += 1

    print('blacks open', blacks_open)
    print(f"trails open: {trails_open}/{total_trails}")

    #print('json lifts', json_lifts)
    # go through list of dicts, tally status
    lifts_open = 0
    total_lifts = 0

    lift_string = "{lift['Name']}: {lift['Status']}"
    for lift in lifts_words:
        #print('lift', lift)
        if lift['Status'] == 'Open':
            lifts_open += 1
        if 'Sunrise' in lift['Name']:
            print(f"{lift_string}")
        total_lifts += 1

    print(f"lifts open: {lifts_open}/{total_lifts}")
    


url_trails = 'https://www.kirkwood.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'
trails_report(url_trails)
url = 'https://www.skiheavenly.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'
trails_report(url)
# need to tally lifts as well. summary on site says open but really on hold..
 

def snow_report(url):
    from bs4 import BeautifulSoup
    import json
    import re
    import requests

    page = requests.get(url)

    # create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    script_items = soup.find_all('script',type='text/javascript')
    require_items = script_items[1].text
    print('require items', require_items)
    # regex
    snow_data_finder = re.compile("snowReportData = ({.*})")
    # returns list, so get 1st element
    snow_data = re.findall(snow_data_finder, require_items)[0]
    print("regex", snow_data)
    # json
    json_data = json.loads(snow_data)
    print("json", json_data)

    print('base', json_data['BaseDepth']['Inches'])


'''
snow_url = 'https://www.kirkwood.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx'
snow_report(snow_url)
'''

'''

url = 'https://www.skiheavenly.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx'
resort_name = 'Heavenly'
total_trails, total_lifts, acres_open, terrain_percent, trails_open, lifts_open = \
        ski_scraper(url)

print(total_trails, total_lifts, acres_open, terrain_percent, trails_open, lifts_open)
'''
