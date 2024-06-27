import http.client
import subprocess

# Note: This attacks wont work, since we are assuming google.com response is injected. This is just for dummy testcase purposes.
conn = http.client.HTTPConnection("www.google.com")
conn.request("GET","/")

# Don't trust anything which comes back frm network... even  trusted site, can be injected.
# Network.Taint returned
r1 = conn.getresponse()

# Network.Tainted SOURCE
data1 = r1.read()

p = subprocess.Popen(data1, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
p = subprocess.Popen(data1, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78

# getheaders is a Network.Tainted Source
p = subprocess.Popen(r1.getheaders()[0][0], stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78

