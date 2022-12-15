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

# get_with_params()
# post_file()
redirections()