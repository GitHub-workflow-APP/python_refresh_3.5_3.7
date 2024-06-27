# To make sure, different formats of insecure addr are being flagged appropriately
import socket

addr = ("", 8080)  # all interfaces, port 8080

s = socket.create_server(addr) # CWEID 923
