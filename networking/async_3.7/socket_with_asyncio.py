import asyncio
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


loop = asyncio.get_event_loop()

async def handler(conn):
    while True:
        msg = await loop.sock_recv(conn, 1024)
        if not msg:
            break
        await loop.sock_sendall(conn, msg)
    conn.close()


async def server():
    sock = socket(AF_INET, SOCK_STREAM, 0)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.setblocking(False)
    sock.bind(('', 9527))
    sock.listen(5)
    while True:
        conn, addr = await loop.sock_accept(sock)
        loop.create_task(handler(conn))



if __name__ == "__main__":
    loop.create_task(server())
    loop.run_forever()
    loop.close()
