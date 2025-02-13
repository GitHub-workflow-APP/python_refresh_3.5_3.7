import socketserver
import sys

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    ## Entry Point
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip() # <--- Network.Tainted Source
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper()) # CWEID 201


if __name__ == "__main__":
    HOST, PORT = sys.argv[1], 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server: # 99
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


