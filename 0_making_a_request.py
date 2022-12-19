# Basic interface of the library - sending a simple request

import requests

def simplest_request():
    # GET satori home page
    # It's not too useful for humans (because of no CSS and JS) but it works for computers
    response = requests.get('https://satori.tcs.uj.edu.pl')
    print(response.text)

def http_methods():
    methods = ['get', 'post', 'put', 'delete', 'head', 'options', 'patch']
    for method in methods:
        response = requests.request(method, 'https://httpbin.org/' + method)
        print(response.text)

def alternative_syntax():
    # Instead of using the `request` method, we can use the shortcut methods
    # They are named after the HTTP method they use
    requests.get('https://httpbin.org/get')
    requests.post('https://httpbin.org/post')
    requests.put('https://httpbin.org/put')
    # etc.


# simplest_request()
# http_methods()
# alternative_syntax()