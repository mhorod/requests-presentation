# Bundling together everything we've learned so far to create a simple CLI

import requests
from satori_parser import *

def log_in_with_token(session, token):
    session.cookies.set(TOKEN_COOKIE_NAME, token)
    response = session.get(BASE_URL)
    user = get_displayed_name(response.text)
    return user

def log_in_with_credentials(session, login, password):
    response = session.post(url('/login'), data={'login': login, 'password': password})
    user = get_displayed_name(response.text)
    token = session.cookies.get(TOKEN_COOKIE_NAME)
    return user, token

def log_in(session, auth_filename, token_filename):
    user = log_in_with_token(session, get_token(token_filename))
    if user is not None:
        print(f'Logged in with token as {user}')
    else:
        print('Token expired, logging in with credentials')
        login, password = get_auth(auth_filename)
        user, token = log_in_with_credentials(session, login, password)
        if token is None:
            print('Invalid credentials')
        else:
            save_token(token_filename, token)
            print(f'Logged in as {user}')

def get_contests(session):
    print('Getting contest list...')
    response = session.get(CONTEST_LIST_URL)
    contests = get_contest_list(response.text)
    return contests

def get_problems(session, contest):
    print(f'Getting problem list for {contest.name}...')
    response = session.get(problem_list_url(contest))
    problems = get_problem_list(response.text)
    return problems

def download_pdf(session, problem):
    response = session.get(problem.pdf_url)
    if response.status_code != 200:
        print(f'Failed to download PDF: {response.status_code}')
        return
    else:
        print(f'Downloaded PDF: {problem.pdf_url} to {problem.code}.pdf')
        with open(f"{problem.code}.pdf", 'wb') as f:
            f.write(response.content)


def submit_solution(session, problem, filename):
    with open(filename, 'rb') as f:
        file_content = f.read()
        if len(file_content) == 0:
            print('Empty file')
            return
        data = {'problem': problem.id}
        files = {'codefile': file_content}
        response = session.post(problem.submit_url, data=data, files=files)
        if 'Status' in response.text:
            print('Submitted successfully')
        else:
            print('Failed to submit')


def get_cached_contests(session, cache):
    contests = cache.get('contests', None)
    if contests is None:
        contests = get_contests(session)
        cache['contests'] = { contest.name: contest for contest in contests }
    return cache['contests']

def get_cached_problems(session, cache, contest):
    problems = cache.get(contest.name, None)
    if problems is None:
        problems = get_problems(session, contest)
        cache[contest.name] = { problem.code: problem for problem in problems }
    return cache[contest.name]


if __name__ == '__main__':
    print('Satori CLI DEMO')
    print('-' * 80)
    session = requests.Session()
    log_in(session, 'auth', 'token')

    cache = {}

    print("Available commands:")
    print("  contests - list available contests")
    print("  problems <contest> - list problems in a contest")
    print("  pdf <contest> <problem> - download problem statement as PDF")
    print("  submit <contest> <problem> <file> - submit a solution")
    print("  exit - exit the program")
    while True:
        command = input('覚> ')
        parts = command.split()
        if len(parts) == 0:
            continue

        if parts[0] == 'contests':
            contests = get_cached_contests(session, cache)
            for contest in contests.values():
                print(contest)
        elif parts[0] == 'problems':
            if len(parts) != 2:
                print('Invalid command')
                continue
            contest_name = parts[1]
            contests = get_cached_contests(session, cache)
            contest_name = find_match(contest_name, contests.keys())
            if contest_name is None:
                print('Invalid contest')
                continue
            contest = contests[contest_name]
            problems = get_cached_problems(session, cache, contest)
            for problem in problems.values():
                print(problem)
        elif parts[0] == 'pdf':
            if len(parts) != 3:
                print('Invalid command')
                continue
            contest_name = parts[1]
            problem_code = parts[2]
            contests = get_cached_contests(session, cache)
            contest_name = find_match(contest_name, contests.keys())
            if contest_name is None:
                print('Invalid contest')
                continue
            contest = contests[contest_name]
            problems = get_cached_problems(session, cache, contest)
            problem_code = find_match(problem_code, problems.keys())
            if problem_code is None:
                print('Invalid problem')
                continue
            problem = problems[problem_code]
            download_pdf(session, problem)

        elif parts[0] == 'submit':
            if len(parts) != 4:
                print('Invalid command')
                continue
            contest_name = parts[1]
            problem_code = parts[2]
            filename = parts[3]
            contests = get_cached_contests(session, cache)
            contest_name = find_match(contest_name, contests.keys())
            if contest_name is None:
                print('Invalid contest')
                continue
            contest = contests[contest_name]
            problems = get_cached_problems(session, cache, contest)
            problem_code = find_match(problem_code, problems.keys())
            if problem_code is None:
                print('Invalid problem')
                continue
            problem = problems[problem_code]
            submit_solution(session, problem, filename)

        elif parts[0] == 'exit':
            break
        else:
            print('Invalid command')