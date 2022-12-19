# Helper functions that abstract out communication with satori

from dataclasses import dataclass

from bs4 import BeautifulSoup
import re
import os

BASE_URL = 'https://satori.tcs.uj.edu.pl'

CONTEST_LIST_URL = BASE_URL + '/contest/select'

TOKEN_COOKIE_NAME = 'satori_token'

@dataclass
class Contest:
    id: str
    name: str
    url: str
    description: str
    
    def __str__(self):
        return f'[{self.name}] {self.description} ({self.url})'

@dataclass
class Problem:
    id: str
    code: str
    name: str
    pdf_url: str
    deadline: str
    submit_url: str
    page_url: str

    def __str__(self):
        return f'[{self.code}] {self.name}, {self.deadline}'

# URLS

def url(path):
    return BASE_URL + path

def problem_list_url(contest):
    return contest.url + '/problems'

# Parsing

def get_contest_list(html):
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('table', class_='results')
    if results is None:
        return []
    rows = results.find_all('tr')
    contests = [contest_from_row(row) for row in rows if row is not None]
    return [contest for contest in contests if contest is not None]

def contest_from_row(row):
    cells = row.find_all('td')
    if len(cells) != 3:
        return None
    name = cells[0].text
    url = BASE_URL + cells[0].find('a')['href']
    description = cells[1].text
    id = url.split('/')[-1]
    return Contest(id, name, url, description)


def get_problem_list(html):
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('table', class_='results')
    if results is None:
        return []
    rows = results.find_all('tr')
    problems = [problem_from_row(row) for row in rows if row is not None]
    return [problem for problem in problems if problem is not None]


def problem_from_row(row):
    cells = row.find_all('td')
    if len(cells) != 5:
        return None
    code = cells[0].text
    name = cells[1].text
    page_url = cells[1].find('a')
    if page_url is not None:
        page_url = BASE_URL + page_url['href']
    pdf_url = BASE_URL + cells[2].find('a')['href']
    deadline = cells[3].text.strip()
    submit_url = BASE_URL + cells[4].find('a')['href']
    id = submit_url.split('=')[-1]

    return Problem(id, code, name, pdf_url, deadline, submit_url, page_url)



def contest_names(contests):
    return [contest.name for contest in contests]

def problem_codes(problems):
    return [problem.code for problem in problems]

def get_displayed_name(html):
    pattern = re.compile(r"<li>Logged in as (.*)</li>")
    match = pattern.search(html)
    if match:
        return match.group(1)
    return None

# Display

def print_contests(contests):
    for contest in contests:
        print(contest)

def print_problems(problems):
    for problem in problems:
        print(problem)

# Local interaction

def get_auth(filename):
    if not os.path.exists(filename):
        return None, None
    with open(filename) as f:
        return f.read().split('\n')

def get_token(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        return f.read().strip()

def save_token(filename, token):
    with open(filename, 'w') as f:
        f.write(token)




# Interactive

def select_contest(contests):
    print('Select a contest:')
    for i, contest in enumerate(contests):
        print(f'{i + 1}. {contest.name}')
    while True:
        try:
            choice = int(input())
            if 1 <= choice <= len(contests):
                return contests[choice - 1]
            print('Invalid choice')
        except ValueError:
            print('Invalid choice')


def find_match(prefix, names):
    matches = [name for name in names if name.startswith(prefix)]
    if len(matches) == 1:
        return matches[0]
    return None
