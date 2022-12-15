# Helper functions that abstract out communication with satori

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://satori.tcs.uj.edu.pl'

CONTEST_LIST_URL = BASE_URL + '/contest/select'

def url(path):
    return BASE_URL + path

@dataclass
class Contest:
    name: str
    url: str
    description: str

def get_auth(filename):
    with open(filename) as f:
        return f.read().split('\n')

def contest_from_row(row):
    cells = row.find_all('td')
    if len(cells) != 3:
        return None
    name = cells[0].text
    url = BASE_URL + cells[0].find('a')['href']
    description = cells[1].text
    return Contest(name, url, description)

def get_contest_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('table', class_='results')
    rows = results.find_all('tr')
    contests = [contest_from_row(row) for row in rows]
    return [contest for contest in contests if contest is not None]

def contest_names(contests):
    return [contest.name for contest in contests]