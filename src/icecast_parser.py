from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import requests
import json

def parse_content():
    rs = requests.get('http://soundspectra.com/admin/', auth=HTTPBasicAuth('admin', 'h@ckm3'))
    html_data = rs.text
    
    soup = BeautifulSoup(html_data)

    details = {'stream_details' : []}
    details_list = []

    alt = 1
    key = None

    for td in soup.find_all('td'):
    
        if alt:
            if td.get('width') and td.get('width') == '130':
                key = td.text
                alt = not alt
        elif not alt:
            if td.get('class') and td.get('class')[0] == 'streamdata':
                alt = not alt
                value = td.text
                d = {key.encode("utf-8") : value.encode("utf-8")}
                details_list.append(d)

    details['stream_details'] = details_list
    print details

if __name__ == '__main__':
    parse_content()