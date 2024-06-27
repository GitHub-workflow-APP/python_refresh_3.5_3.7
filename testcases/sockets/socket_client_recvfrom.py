# Works in conjuction with server: socket_echo_server_connect.py
# Payload: python3 socket_client_recvfrom.py "ls"

import socket
import sys
import subprocess

HOST = ''               # The remote host
PORT = 50007              # The same port as used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # CWEID 923
    s.sendall(bytes(sys.argv[1],'utf-8')) # CWEID 201

    data = s.recvfrom(4096) # Network.Tainted Source

print(data)