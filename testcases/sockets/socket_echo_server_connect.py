# Echo server program
# Run this server as python3 socket_echo_server_connect.py
# Send os commands from client using
# Run in conjuction with socket_client_recvfrom.py

import socket
import subprocess

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # CWEID 923
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024) # Network.Tainted SOURCE
            if not data: break
            p = subprocess.Popen(data, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
            conn.sendall(p.communicate()[0]) # CWEID 201
    s.close()
