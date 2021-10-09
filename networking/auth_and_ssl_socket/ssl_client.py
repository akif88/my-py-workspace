from socket import socket, AF_INET, SOCK_STREAM
import ssl

tcp_sock = socket(AF_INET, SOCK_STREAM)
tcp_sock_ssl = ssl.wrap_socket(tcp_sock, cert_reqs=ssl.CERT_REQUIRED, ca_certs='server_cert.pem')

tcp_sock_ssl.connect(('localhost', 20000))
tcp_sock_ssl.send(b'Hello world!')
print(tcp_sock_ssl.recv(8196))
tcp_sock_ssl.close()


