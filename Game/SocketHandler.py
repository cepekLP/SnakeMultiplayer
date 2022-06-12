import socket
import struct
import random
import _thread
import traceback
import time
import array
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

  def sendCommand(self, command):
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
          decode_data = str(recv_data, 'ascii')
          #convert null terminated string from c to python string
          decode_data = decode_data.split("\0")[0]
        except:
          # printing stack trace
          traceback.print_exc()
        
        print(len(decode_data), decode_data)

        if decode_data == "pingcrc":
          recv_data = self.socketh.recv(4)
          self.dataHandler(decode_data, recv_data)
        
        if decode_data == "game":
          recv_data = self.socketh.recv(208)
          self.dataHandler(decode_data, recv_data)
 
      except:
        print("Server closed connection, thread exiting.")
        _thread.interrupt_main()
        break

  def dataHandler(self,command, data):
    try:
      print("[HANDLER]")

      if command == "pingcrc":
        print("[PING] Unpacked")
        crc = struct.unpack("i", data)
        print(crc)

      if command == "game":
        print("[GAME] Unpacked")
        print(len(data))
        gamedata = struct.unpack('IHH50H50H', data)
        timestamp = gamedata[0]
        length = gamedata[1]
        direction = gamedata[2]
        posX = gamedata[3:53]
        posY = gamedata[53:103]
        print(timestamp, length, direction, posX, posY)
    
    except:
      traceback.print_exc()

sh = SocketHandler()
sh.connect()

_thread.start_new_thread(sh.asyncRecv,())

sh.sendCommand('status')


text: str = "test"
while len(text)<256:
  text = text + '\0'

sh.sendStruct(struct.pack("ff256s", random.uniform(1, 13), random.uniform(1,200), bytes(text, "ascii")))

sh.sendCommand('pingcrc')
time.sleep(0.01)
sh.sendStruct(struct.pack("i", 69420))


sh.sendCommand('game')

posX = array.array('H')
posY = array.array('H')

for i in range(0,50):
  posX.append(i)
  posY.append(i + 3)

buf = struct.pack('IHH50H50H', 4097 , 33, 1 ,*posX, *posY)

sh.sendStruct(buf)


while True:
  pass

sh.close()