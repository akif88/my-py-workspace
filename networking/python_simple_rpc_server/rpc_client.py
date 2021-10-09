from multiprocessing.connection import Client

from jsonrpcclient import RPCProxy 

c = Client(('10.0.2.7', 17000), authkey=b'peekaboo')
proxy = RPCProxy(c)
print(proxy.add(5,3))
print(proxy.sub(5,3))
