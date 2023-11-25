import socket
import threading
import time
import json

# next create a socket object

class Server:
    def __init__(self):
        self.start = 0
        self.data = {}
        self.s = socket.socket()
        print("Socket successfully created")
        port = 12346
        self.lock = threading.Lock()

        self.s.bind(('', port))

        self.s.listen(5)

        while True:
            c, addr = self.s.accept()
            print ('Got connection from', addr)
            threading.Thread(target=self.thread, args=(c, addr)).start()
            self.start += 1

    def thread(self, c, addr):
        while self.start < 2:
            time.sleep(0.02)
        c.recv(1024)
        c.send(json.dumps([{"position": [240, 100], "foto": "self.images.stilstaan_img", "aanvallen": []}]).encode())
        try:
            while True:
                andere_data = []
                self.data[addr] = json.loads(c.recv(1024).decode())
                self.lock.acquire()
                for data in self.data.keys():
                    if data != addr:
                        andere_data.append(self.data[data])
                for data in andere_data:
                    del self.data[list(self.data.keys())[list(self.data.values()).index(data)]]
                self.lock.release()
                c.send(json.dumps(andere_data).encode())
        except json.decoder.JSONDecodeError as e:
            self.start -= 1

Server()
