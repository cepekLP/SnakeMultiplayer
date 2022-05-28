import socket
import struct
import random
import _thread
#import numpy as np



class SocketHandler:

  HOST = "127.0.0.1"  # The server's hostname or IP address
  PORT = 5000  # The port used by the server

  def connect(self):
    self.socketh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socketh.connect((self.HOST, self.PORT))

  def sendStruct(self, message):  
    self.socketh.sendall(message)

  def sendCommnad(self, command):
    self.socketh.sendall(bytes(command,'ascii'))

  def close(self):
    self.socketh.close()

  def asyncRecv(self):
    while True:
      try:
        recv_data = self.socketh.recv(4096)
        self.dataHandler(recv_data)   
      except:
        print("Server closed connection, thread exiting.")
        _thread.interrupt_main()
        break

  def dataHandler(self,data):
    uData = struct.unpack("ff256s", data)
    a,b,t = uData
    print(a)

sh = SocketHandler()
sh.connect()

_thread.start_new_thread(sh.asyncRecv,())

sh.sendCommnad('status\n\0')


text: str = "test\n"
while len(text)<256:
  text = text + '\0'

sh.sendStruct(struct.pack("ff256s", random.uniform(1, 13), random.uniform(1,200), bytes(text, "ascii")))

while True:
  pass

sh.close()
