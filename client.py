import socket
import sys

class Client():
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.max_recv = 4096
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((self.host, self.port))

  def send_request(self, filename):
    request = f'GET /{filename} HTTP/1.1\r\nHost: {self.host}\r\n\r\n'
    self.client.sendall(request.encode())

    response = b''
    while True:
        msg = self.client.recv(self.max_recv)
        if not msg:
            break
        response += msg
    print("[Server Response]: ")
    print(response.decode())

    self.client.close()
    print(f'[CLOSED] Connection to server')

if __name__ == '__main__':
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]
    c = Client(server_host, server_port)
    c.send_request(filename)