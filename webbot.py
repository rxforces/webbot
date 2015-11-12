import json
import os
import requests
import socket
import time
import logging
from bs4 import BeautifulSoup
import re





TOPIC_URL = "https://wwwin-tools.cisco.com/srchui/Search.do"

def do_topic_search(query_string):
    """Do a topic seach with the query string and return the HTML response

    :param query_string: String to search topic for
    :param cookies: SSO cookie required for topic searches
    """
    logging.debug('Query: '.format(query_string))
    search_parameters = {
        'searchResultsPerPage': '20',
        'method': 'getSearchResults',
        'queryText': query_string,
        'repository': ['cdets', 'c3'],
        'repoInc': 'cdets',
        'sortBy': 'Relevance'
    }
    # response = requests.get(TOPIC_URL, cookies=cookies, params=search_parameters)
    response = requests.get(TOPIC_URL, auth=('username','###'), params=search_parameters)
    if response.status_code != 200:
        raise ValueError('HTTP {} error encountered when connecting to topic'.format(response.status_code))
    html = response.text
    return html

def parse_topic_html(html):
    """Parses the topic search HTML and returns the results as a dictionary

    :param html: (str) The HTML associated with the topic search

    raises ValueError on bad HTML
    """
    results = []
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all("div", "result-entry"):
        label = item.find("label", "boldDs")

        if label:
            title = item.find("a", "title")
            url = title.attrs['href']
            title_text = title.text

            for seq in ['\t', '\n', '\r', '<b>', '</b>']:
                title_text = title_text.replace(seq, '')
            title_text = title_text.strip()

            #if 'C3/CSOne/CARE' in label.string:
            if 'SR' in label.string:
                _type = 'sr'
                match = re.search(r'^(\d{9}):\s*(.*)$', title_text)
            #elif 'CDETS/DDTS' in label.string:
            elif 'CDETS' in label.string:
                _type = 'cdets'
                match = re.search(r'^(\w{10}):\s*(.*)$', title_text)
            else:
                raise ValueError('Not a topic search result')
            _id = match.group(1)
            _title = match.group(2).strip(' -')
            if type == 'sr':
                url = 'http://www-tac.cisco.com/Teams/ks/c3/casekwery.php?Case={}'.format(url)
            _res = {
                'type': _type,
                'id': _id,
                'title': _title,
                'url': url
            }
            results.append(_res)
    return results

# oauth_token = os.environ.get('OAUTH_TOKEN')
# cookies = {'ObSSOCookie': os.environ['sso_cookie']}
query_string = os.environ['Query']


topic_html = do_topic_search(query_string=query_string)

#print topic_html

results = parse_topic_html(topic_html)
print('Found {} results'.format(len(results)))
print(json.dumps(results, indent=4, sort_keys=True))


