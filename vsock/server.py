import argparse
from cgitb import handler
import socket

class VSocketServer:
    """
    A simple vsock server.
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.bind(('\x00\x00\x00\x00\x00\x00\x00\x01', 80))
        self.sock.listen(1)
    def recv(self):
        while True:
            conn, addr = self.sock.accept()
            data = conn.recv(1024)
            # receive the enclave keys
def handle_server(self):
    """
    Handle the server.
    """
    # Create a socket for the server.
    server = VSocketServer()
    print('Server is listening ', self.port)
    # Start receiving from connection.
    server.recv()
    
if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(prog='vsock-sample')
    # Add arguments required by the server
    parser.add_argument('--port', type=int, default=8000)
    # Handle arguments
    parser.set_defaults(func=handle_server)
