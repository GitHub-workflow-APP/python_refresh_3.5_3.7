# Client code works in conjuction with sockerserver_vuln_cwe_*.py files
# Attack Payload: python3 socketserver_client.py "ls"
# Output: Output of ls command
import socket
import sys
import subprocess

HOST, PORT = "localhost", 9999
data = sys.argv[1]

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data , "utf-8")) # CWEID 99

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8") # <--- Network.Tainted SOURCE
    p = subprocess.Popen(received, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78

    print(p.communicate()[0])
