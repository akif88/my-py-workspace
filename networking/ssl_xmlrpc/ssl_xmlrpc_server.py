import ssl
from xmlrpc.server import SimpleXMLRPCServer
from ssl_mix_xmlrpc import SSLMixin

class SSLSimpleXMLRPCServer(SSLMixin, SimpleXMLRPCServer):
    pass


class KeyValueServer:
    def __init__(self, *args, **kwargs):
        _rpc_methods_ = ['get', 'set', 'delete', 'exists', 'keys']
        self._data = dict()
        self._serv = SSLSimpleXMLRPCServer(*args, allow_none=True, **kwargs)
        for name in _rpc_methods_:
            self._serv.register_function(getattr(self, name))
     
    def get(self, name):
        return self._data[name]
    def set(self, name, value):
        self._data[name] = value
    def delete(self, name):
        del self._data[name]
    def exists(self, name):
        return name in self._data
    def keys(self):
        return list(self._data)
    def serv_forever(self):
        self._serv.serve_forever()


if __name__ == "__main__":
    KEYFILE='server_key.pem'    # Private key of the server
    CERTFILE='server_cert.pem'  # Server certificate
    #CA_CERT='client_cert.pem'

    key_value_server = KeyValueServer(('', 15000),
            keyfile=KEYFILE,
            certfile=CERTFILE)
    key_value_server.serv_forever()

