import xmlrpc.client as xrc

s = xrc.ServerProxy('http://localhost:8000')
print(s.pow(2,3))
print(s.add(2,3))  
print(s.mul(5,2))  

# Print list of available methods
print(s.system.listMethods())


