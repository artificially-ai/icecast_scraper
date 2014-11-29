from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import requests
import json

#The column width in IceCast admin page. Looks weird to make it based on a width,
#but they use the same value for all columns.
WIDTH = '130'

def parse_content():
    #Do not forget the trailing / in the URL, otherwise it won't work
    rs = requests.get('http://your_host.com/admin/', auth=HTTPBasicAuth('admin', 'pass'))
    html_data = rs.text
    
    soup = BeautifulSoup(html_data)

    details = {'stream_details' : []}
    details_list = []

    alt = 1
    key = None

    for td in soup.find_all('td'):
    
        if alt:
            if td.get('width') and td.get('width') == WIDTH:
                key = td.text
                alt = not alt
        elif not alt:
            if td.get('class') and td.get('class')[0] == 'streamdata':
                alt = not alt
                value = td.text
                d = {key : value}
                details_list.append(d)

    details['stream_details'] = details_list
    details_json = json.dumps(details)
    
    return  details_json

if __name__ == '__main__':
    details = parse_content()
    
    print details
