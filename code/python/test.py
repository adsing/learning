''' Test code '''

import json
import requests

# Create python env
## python3 -m venv venv             # creates local folder venv
## source ./venv/bin/activate
## (venv) user@user-desktop:~/Desktop/code/python$
## /home/user/Desktop/code/python/venv/bin/python3 -m pip install -U autopep8 for pylint

# from https://www.youtube.com/watch?v=W--_EOzdTHk
# "arpl" extension to run code in parallel at run-time - good for testing REST API
# kite & copilot - AI powered - show module docs
# auto docstring - provide template for class/module to make it easy to document
# pytest enabled in settings->test->python (gives a lab icon on left bar)


# Lookup these?
# code snippet
# pytest

CONST_X=5
CONST_Y = CONST_X + 1
print(CONST_Y)
print("done")

if CONST_Y == 6:
    print("6")

def greet(greeting:str, name:str):
    return f'{greeting} {name}!'

print(greet("Hello", "name"))

items = json.loads('[{"a":1,"b":2}, {"a":3,"b":4}]')
print(items)
for item in items:
    print(item['b'])


response = requests.get('https://randomuser.me/api')
print("response")
data = response.json()
print(data)


