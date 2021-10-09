import selectors
from socket import socket, AF_INET, SOCK_STREAM


sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    

def read(conn, mask):
    data = conn.recv(1000)
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', 12345))
sock.listen(1)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)
   
while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)


