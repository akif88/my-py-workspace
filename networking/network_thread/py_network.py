from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def echo_handler(address, client_sock):
    print('Got connection from {}'.format(address))
    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)
    client_sock.close()
            
def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(0)
    while True:
        client_sock, client_addr = sock.accept()
        try:
            Thread(target=echo_handler, args=(client_addr, client_sock)).start(            
        except RuntimeError:
            raise
        

if __name__ == '__main__':
    echo_server(('', 20001))
