# Basic properties of a Response object

import requests


# GET request
# requests.get performs a GET request on the given URL
# and returns a Response object
response = requests.get('https://httpbin.org/get')

# Most important attributes of a Response object

# http status code
print("STATUS CODE & REASON")
print(response.status_code, response.reason)
print()

# For responses with text content we can use the `text` attribute
# Response also has `content` attribute which returns the raw bytes
print("TEXT")
print(response.text)
print()

# If response is binary we'll need `content` rather than text
print("CONTENT")
print(response.content)
print()


# For responses with JSON content we can call `json` method to get parsed dictionary
print("JSON")
print(response.json())
print()

# Where the request was redirected to
print("URL")
print(response.url)
print()

# dictionary of the response headers
print("HEADERS")
for key, value in response.headers.items():
    print(key,":", value)
print()

# cookies
print("COOKIES")
for key, value in response.cookies.items():
    print(key,":", value)
print()

