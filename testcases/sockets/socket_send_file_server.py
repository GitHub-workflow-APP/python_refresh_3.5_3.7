# Server program to send requested file back to client. Used in conjuction with socket_sendfile_client.py
# Run this server as python3 socket_send_file_server.py ''
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # CWEID 923
    s.listen(5)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024) # Network.Tainted SOURCE
            if not data: break
            with open(data,'rb') as f: # CWEID 73
                conn.sendfile(f,0) # CWEID 73
    s.close()
