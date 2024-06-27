# Server code works in conjuctio with socket_client_recvmsg_into.py
# Run this server python3 socket_server_recvmsg.py ''
# This server returns a command to client. So client code has a CWEID 78 (Command Injection)

import socket
import sys

HOST = sys.argv[1]    	# Network.Tainted data being set
PORT = 50007	  	  # Arbitrary non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # bind using Network.Tainted data
    s.bind((HOST, PORT)) # CWEID 99
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)

        while True:
            msg, ancdata, flags, addr = conn.recvmsg(1024) # Network.Tainted SOURCE

            if not msg: break
            conn.sendall(msg) # CWEID 201

            s.close()
        s.close()
s.close()
