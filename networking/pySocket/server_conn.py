import socket

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host=socket.gethostname()
port=12345
s.bind(('', port))
s.listen(5)

while True:
    c, addr=s.accept()
    print ('Got connection from', addr)
    c.send(b'Thank you for connecting')
    c.close()
