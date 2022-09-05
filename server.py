import socket

s = socket.socket()
print("Socket Created")

s.bind(('localhost',5058))

s.listen(3)
print("Waiting for a Connection !!")

while True:
    c, addr = s.accept()
    name = c.recv(1024).decode()
    print("Connected with :",addr, " ", name)
    c.send(bytes("Welcome to Socket Programming",'utf-8', name))
    c.close()