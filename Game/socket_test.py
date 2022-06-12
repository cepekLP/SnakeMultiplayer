import socket
import struct
import random
#import numpy as np

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")
    text: str = "test\n"
    while len(text)<256:
        text = text + '\0'
        
      #  lst = []
      #  word = 'Sample'
      #  lst.extend(word)
    
    #data = s.recv(2000)
    bina = bytes(text, "utf-8")
    #lst = np.array[256]
    #for i in len(text):
     #   lst[i] = text[i]
    #for i in range(len(bina))
      #  print(bina[i])
    s.sendall(struct.pack("ff256s", random.uniform(1, 13), 13.0, bytes(text, "ascii")))  
    while True:
      pass
      
#print(f"Received {data!r}")
