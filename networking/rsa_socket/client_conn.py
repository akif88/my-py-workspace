import socket

server_name = '192.168.0.7'
server_port = 12000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_name, server_port))

# public_key_server = client_socket.recv(1024)

server_message = client_socket.recv(21)
print(server_message)

M = int(input('Key: '))
# C = M^e(mod n)
public_n = client_socket.recv(37)
public_e = client_socket.recv(37)
print(public_n, public_e)
n = int(public_n)
e = int(public_e)
C = pow(M, e, n)

client_socket.send(bytes(str(C), "ascii"))
print(C)

server_message = client_socket.recv(1024)
print(server_message)

client_socket.close()
