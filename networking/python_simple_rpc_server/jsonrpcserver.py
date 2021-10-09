import json

class RPCHandler:
    
    def __init__(self):
        self._functions = { }

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                # args for list, kwargs for dict(key:value) parameters, if they exists
                func_name, args, kwargs = json.loads(connection.recv())  # decode   
                # Run the RPC and send a response
                try:
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(json.dumps(r))  # encode
                    print("send value: {}".format(r))
                except Exception as e:
                    connection.send(json.dumps(str(e)))
        except EOFError:
            pass
