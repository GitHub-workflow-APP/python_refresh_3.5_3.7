# Echo client program to receive sendfile from socket_send_file_server.py
# Run corresponding server code as python3 socket_send_file_server.py ''
# Attach Payload: python3 socket_sendfile_client.py '/etc/passwd'
import socket
import sys
import subprocess

HOST = ''    # The remote host
PORT = 50007              # The same port as used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(sys.argv[1],'utf-8')) # CWEID 201
    data = s.recv(4096) # Network.Tainted Source

print(data)

