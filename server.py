import socket;
import threading;

class ThreadedServer():
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.max_recv = 4096
    self.max_conn = 1
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((self.host, self.port))

  def handle_connection(self, client_sock, client_address):
    print(f'[NEW CONNECTION] {client_address} connected!')
    try:
      msg = client_sock.recv(self.max_recv).decode()
      filename = msg.split()[1]
      file = open(filename[1:])
      data = file.read()
      print(f'[{client_address}] message: {msg}')
      client_sock.send('HTTP/1.1 200 OK \r\n\r\n'.encode())
      client_sock.sendall(data.encode())
      client_sock.send('\r\n'.encode())
    except IOError or FileNotFoundError:
      client_sock.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
    except IndexError:
      print('[CLOSING CONNECTION]')
    finally:  
      print(f'[CLOSED]: {client_address}')
      client_sock.close()
  
  def run(self):
    self.server.listen(self.max_conn)
    print(f'[LISTENING] Server listening on {self.host}:{self.port}')
    while True:
      conn, addr = self.server.accept()
      thread = threading.Thread(target= self.handle_connection, args= (conn, addr) )
      thread.start()
      print(f'[ACTIVE CONNECTION] {threading.active_count()-1}')

if __name__ == '__main__':
  s = ThreadedServer('127.0.0.1', 80)
  s.run()