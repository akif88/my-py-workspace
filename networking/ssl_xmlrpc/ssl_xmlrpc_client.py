import ssl
from xmlrpc.client import SafeTransport, ServerProxy

class VerifyCertSafeTransport(SafeTransport):
    
    def __init__(self, cafile, certfile=None, keyfile=None):
        SafeTransport.__init__(self)
        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self._ssl_context.load_verify_locations(cafile)
        if certfile:
            self._ssl_context.load_cert_chain(certfile, keyfile)
        self._ssl_context.verify_mode = ssl.CERT_REQUIRED

    def make_connection(self, host):
        s = super().make_connection(host)
        return s

if __name__ == "__main__":
    transport = VerifyCertSafeTransport('server_cert.pem')
    s = ServerProxy('https://localhost:15000', transport = transport, allow_none=True)
    s.set('foo','bar')
    s.set('spam', [1, 2, 3])
    print(s.keys())
    print(s.get('foo'))
    print(s.get('spam'))
