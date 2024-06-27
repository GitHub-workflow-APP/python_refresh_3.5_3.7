# Works in conjuction with server: socket_server_recvmsg.py
# Payload: python3 socket_client_recvmsg_into.py "ls"

import socket
import sys
import subprocess

HOST = ''               # The remote host
PORT = 50007              # The same port as used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # CWEID 923
    s.sendall(bytes(sys.argv[1],'utf-8')) # CWEID 201
    
    b1 = bytearray(b'--')
    s.recvmsg_into([b1]) # Network.Tainted Source

p = subprocess.Popen(b1.decode("utf-8"), stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
print(p.communicate()[0])

