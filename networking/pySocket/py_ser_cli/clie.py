from socket import *

server_name='127.0.0.1'
server_port=12000

client_sock=socket(AF_INET, SOCK_STREAM)
client_sock.connect((server_name, server_port))
sentence = input('Input lower sentence: ')
client_sock.send(bytes(sentence, "ascii"))
modif_sentence=client_sock.recv(1024)
print('From Server', modif_sentence)
client_sock.close()
