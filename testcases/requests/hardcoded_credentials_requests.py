# Payload:  python3 hardcoded_credentials_requests.py "password"

import requests
import sys

passwd = sys.argv[0]

r = requests.get('https://api.github.com/user', auth=('user', 'pass')) # CWEID798

r = requests.get('https://api.github.com/user', auth=('user', passwd)) # FP CWEID 798

