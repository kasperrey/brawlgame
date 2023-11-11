import socket
import time

s = socket.socket()
port = 12346
s.connect(('127.0.0.1', port))
s.send(input("naam: ").encode())
time.sleep(1)
s.send("ik ben cool".encode())
print(s.recv(1024).decode())
s.close()
