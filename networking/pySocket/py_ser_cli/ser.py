from socket import *
import base64

server_port=12000
server_socket=socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print("The server is ready to receive")

while 1:
    conn_socket, addr = server_socket.accept()
    sentence = conn_socket.recv(1024)
    print('Recevied sentence:', sentence)
    cap_sentence=sentence.upper()
    conn_socket.send(base64.b64encode(cap_sentence))
    print('Sending sentence:', cap_sentence)
    conn_socket.close()

