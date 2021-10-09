from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from auth_client import server_authenticate

SECRET_KEY = b'peekaboo'


def echo_handler(client_sock, addr):
    if not server_authenticate(client_sock, SECRET_KEY):
        client_sock.close()
        print("Failed Auth {}".format(addr))
        return
    else:
        print("auth succesful for {}".format(addr))
    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)


def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    while True:
        conn, addr = s.accept()
        print("{} connected".format(addr))
        Thread(target=echo_handler, args=(conn,addr)).start()
        
        
if __name__ =="__main__":
    echo_server(('', 18000))

