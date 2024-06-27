import requests

r = requests.request('GET','https://httpbin.org/get',verify=False) # CWEID 295
r = requests.get('https://httpbin.org/get', verify=False) # CWEID 295
r = requests.post('https://httpbin.org/get', verify=False) # CWEID 295
r = requests.put('https://httpbin.org/get', verify=False) # CWEID 295
r = requests.delete('https://httpbin.org/get', verify=False) # CWEID 295
r = requests.patch('https://httpbin.org/get', verify=False) # CWEID 295
r = requests.options('https://httpbin.org/get', verify=False) # CWEID 295
r = requests.head('https://httpbin.org/get', verify=False) # CWEID 295
