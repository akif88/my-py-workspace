import socket
import rsa_ver0 as rsa


server_port = 12000

n, e, d = rsa.generate()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print('The Server Listen to Clients')

while 1:
    connection_socket, address = server_socket.accept()
    print('Connected Client: ', address)

    connection_socket.send(b'Please Enter Your Key')

    # send Public Key n, e
    connection_socket.send(bytes(str(n), "ascii"))
    connection_socket.send(bytes(str(e), "ascii"))
    print(n, e)


    secret_key = connection_socket.recv(1024)
    print(secret_key)

    # rsa M = C^d(mod n)
    C = int(secret_key)
    key = (C**d) % n
    print(key)

    connection_socket.send(b'Recevied Your Key')

    connection_socket.close()


