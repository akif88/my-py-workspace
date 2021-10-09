from multiprocessing.connection import Listener
from threading import Thread

from jsonrpcserver import RPCHandler


def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client,))
        t.deamon = True   # for alive for long-running thread, can't join
        t.start()


def add(x, y):
    return x + y

def sub(x, y):
    return x - y


if __name__ == "__main__":
    # register with a handler
    handler = RPCHandler()
    handler.register_function(add)
    handler.register_function(sub)
    
    # Run the Server
    rpc_server(handler, ('', 17000), authkey=b'peekaboo')



