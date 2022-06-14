import socket
import struct
import random
import _thread
import traceback
import time
import array
from constants import *
#import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from Game import Game

class SocketHandler:

  HOST = "127.0.0.1"  # The server's hostname or IP address
  PORT = 5000  # The port used by the server
  game: 'Game'

  def connect(self):
    self.socketh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socketh.connect((self.HOST, self.PORT))

  def start(self, game):
    self.connect()
    _thread.start_new_thread(self.asyncRecv,())
    self.game = game
    #self.sh.game = self

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

        if decode_data == "init":
          print("[INIT]", PlayerState.getSize())
          recv_data = self.socketh.recv(PlayerState.getSize())
          self.dataHandler(decode_data, recv_data)
        
        if decode_data == "game":
          recv_data = self.socketh.recv(2)
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

      if command == "init":
        print("[INITIALIZE] Unpacked")
        ps = PlayerState.unpack(data)
        self.game.init_player(ps)
        print(ps.position_x[0], ps.position_y[0], ps.length)

      if command == "game":
        print("[GAME] Unpacked")
        print(len(data))
        activePlayers = struct.unpack('H', data)
        activePlayers = activePlayers[0]
        print("Active players: ", activePlayers)

        psArray = []

        for i in range(activePlayers):
          data = self.socketh.recv(PlayerState.getSize())
          cPlayer = PlayerState.unpack(data)
          psArray.append(cPlayer)
        
        self.game.pass_snake(psArray)

        appleX = self.socketh.recv(2)
        appleX = int.from_bytes(appleX, "little")       
        appleY = self.socketh.recv(2)
        appleY = int.from_bytes(appleY, "little")       

        self.game.pass_apple(Point(appleX, appleY))

    except:
      traceback.print_exc()
