# Sessions allow us to persist data across multiple requests.
# This way we can interact with websites that require authentication or have other stateful behavior.

import requests
from satori import *


def get_contests_without_session():
    # What happens if we just make multiple requests without using a session?

    response = requests.get(CONTEST_LIST_URL)
    contests = get_contest_list(response.text)
    print("Contests without logging in:", contest_names(contests))

    # Log in asking to be redirected to the contest list
    login, password = get_auth('auth')
    response = requests.post(
        url('/login?redir=/contest/select'), data={'login': login, 'password': password})
    contests = get_contest_list(response.text)
    print("Contests after logging in:", contest_names(contests))

    # Ask for the contest list again
    response = requests.get(CONTEST_LIST_URL)
    contests = get_contest_list(response.text)
    print("Contests after logging in again:", contest_names(contests))


def get_contests_with_session():
    # This time we create a session and use it to make requests
    session = requests.Session()

    # log in
    login, password = get_auth('auth')
    session.post(url('/login'), data={'login': login, 'password': password})

    # get the contest list
    response = session.get(CONTEST_LIST_URL)
    contests = get_contest_list(response.text)
    print("Contests after logging in:", contest_names(contests))


print("WITHOUT SESSION")
get_contests_without_session()


print()
print("WITH SESSION")
get_contests_with_session()
