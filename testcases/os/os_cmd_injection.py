import os
import sys

# Attack Payload: python3 os_cmd_injection.py "/bin/cat /etc/passwd"
os.system(sys.argv[1]) # CWEID 78
print(os.popen(sys.argv[1]).read()) # CWEID 78
