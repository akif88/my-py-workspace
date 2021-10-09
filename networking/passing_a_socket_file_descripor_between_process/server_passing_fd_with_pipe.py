import multiprocessing
from multiprocessing.reduction import recv_handle, send_handle

from socket import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

def worker(in_proc, out_proc):
    out_proc.close()
    while True:
        fd = recv_handle(in_proc)
        print('CHILD: GOT FD', fd)
        with socket(AF_INET, SOCK_STREAM, fileno=fd) as s:
            while True:
                msg = s.recv(1024)
                if not msg:
                    break
                print('CHILD: RECV {!r}'.format(msg))
                s.send(msg)

def server(address, in_proc, out_proc, worker_pid):
    in_proc.close()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind(address)
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        print('SERVER: Got connection from', addr)
        send_handle(out_proc, client.fileno(), worker_pid)
        client.close()


if __name__ == "__main__":
    client_1, client_2 = multiprocessing.Pipe()
    worker_proc = multiprocessing.Process(target=worker, args=(client_1, client_2))
    worker_proc.start()

    server_proc = multiprocessing.Process(target=server, args=(('', 15000), client_1, client_2, worker_proc.pid))
    server_proc.start()

    client_1.close()
    client_2.close()

