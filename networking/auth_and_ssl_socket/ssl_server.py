from socket import socket, AF_INET, SOCK_STREAM
import ssl

KEY_FILE = 'server_key.pem'  # private key of the server
CERT_FILE = 'server_cert.pem'    # server certificate (given to client)

def echo_client(conn):
    while True:
        data = conn.recv(8196)
        if data == b'':
            break
        conn.send(data)
    conn.close()
    print("Connection closed")


def echo_server(address):
    tcp_sock = socket(AF_INET, SOCK_STREAM)
    tcp_sock.bind(address)
    tcp_sock.listen(0)

    tcp_sock_ssl = ssl.wrap_socket(tcp_sock, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True)
    while True:
        try:
            conn, addr = tcp_sock_ssl.accept()
            print('Got connection', conn, addr)
            echo_client(conn)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    echo_server(('', 20000))

