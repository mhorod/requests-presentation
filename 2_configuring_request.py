# Adding options to the request

import requests

def get_with_params():
    # GET request with query parameters
    # We can add query parameters to the URL using the `params` keyword argument
    params = {
        'param1': 'value1',
        'param2': 'value2',
    }
    response = requests.get('https://httpbin.org/get', params=params)

    print("Response URL:", response.url)
    print("Response text:", response.text)


def post_file():
    # POST file
    # We can add files to the request using the `files` keyword argument
    # File can have any name, including empty string which is impossible in normal case
    files = { '': open('file.txt', 'rb') }
    response = requests.post('https://httpbin.org/post', files=files)

    print("Response text:", response.text)


def redirections():
    # Redirections
    # By default requests follows redirections
    # We can see the history of redirections in the `history` attribute
    print("Allowing redirections")
    # This URL redirects 3 times
    response = requests.get('https://httpbin.org/redirect/3')
    print("Response URL:", response.url)
    print("Redirection history:", response.history)
    print()

    # We can disable this behavior by setting `allow_redirects` to False
    print("Disabling redirections")
    # This URL would redirect 3 times, but because we disabled it, we get the first URL
    response = requests.get('https://httpbin.org/redirect/3', allow_redirects=False)

    print("Response URL:", response.url)
    print("Redirection history:", response.history)

def headers():
    # We can add headers to the request using the `headers` keyword argument
    # For example we can pretend that we're using a different browser
    headers = {
        'User-Agent': 'Internet Exploder',
        'X-My-Header': 'My value',
    }
    response = requests.get('https://httpbin.org/get', headers=headers)

    print("Response text:", response.text)

def timeout():
    # Requests are blocking
    # To prevent waiting forever for a response, we can set a timeout

    # This server does not respond
    try:
        requests.get('http://mhorod.ninja', timeout=2)
    except requests.exceptions.Timeout:
        print("Timeout :(")


# get_with_params()
post_file()
# redirections()
# headers()
# timeout()