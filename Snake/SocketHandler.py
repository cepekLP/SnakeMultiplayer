import socket
import struct
import random
import _thread
import traceback
import time
#import numpy as np



class SocketHandler:

  HOST = "127.0.0.1"  # The server's hostname or IP address
  PORT = 5000  # The port used by the server
  command = ""

  def connect(self):
    self.socketh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socketh.connect((self.HOST, self.PORT))

  def sendStruct(self, message):  
    self.socketh.sendall(message)

  def sendCommnad(self, command):
    text: str = command + "\0"
    while len(text) < 20:
      text = text + '\0'
    self.socketh.sendall(bytes(text,'ascii'))

  def close(self):
    self.socketh.close()

  def asyncRecv(self):
    while True:
      try:
        recv_data = self.socketh.recv(10)
        decode_data = ""
        #recv_data = self.decodeNullTerminated(recv_data)
        try:
          decode_data = str(recv_data,'ascii')
          #convert null terminated string from c to python string
          decode_data = decode_data.split("\0")[0]
        except:
          # printing stack trace
          traceback.print_exc()
        
        print(len(decode_data))

        if decode_data == "pingcrc":
          print(recv_data)
          recv_data = self.socketh.recv(4096)
          self.command = "pingcrc"
          self.dataHandler(recv_data)
 
      except:
        print("Server closed connection, thread exiting.")
        _thread.interrupt_main()
        break

  def dataHandler(self,data):
    print("Data handler")
    if self.command == "pingcrc":
      crc = struct.unpack("i", data)
      print(crc)

    #uData = struct.unpack("ff256s", data)print(len(recv_data))
    data = str(data, 'ascii')
    data, b = data.split("\0", 1)
    return data

sh = SocketHandler()
sh.connect()

_thread.start_new_thread(sh.asyncRecv,())

sh.sendCommnad('status')


text: str = "test"
while len(text)<256:
  text = text + '\0'

sh.sendStruct(struct.pack("ff256s", random.uniform(1, 13), random.uniform(1,200), bytes(text, "ascii")))

sh.sendCommnad('pingcrc')
time.sleep(0.01)
sh.sendStruct(struct.pack("i", 69420))

while True:
  pass

sh.close()
