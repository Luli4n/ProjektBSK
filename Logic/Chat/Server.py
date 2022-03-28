from multiprocessing import BoundedSemaphore
import select
import socket, pickle
from struct import Struct
import struct
from time import sleep

from Logic.Chat.Frame import FrameType

HEADER = Struct("!L")

class Server:

    
    
    def __init__(self):
        self.semaphore = BoundedSemaphore(value=1)
        with self.semaphore:
            self.RSA_Received = False
        

    def CreateServer(self, addr, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((addr, port))
        self.socket.listen()
        (self.connection, self.address) = self.socket.accept() 

    def Set_RSA_Received(self,frame):
        with self.semaphore:
            self.strangerRSA = frame.data
            self.RSA_Received = True

    def Get_RSA_Received(self):
        while True:
            sleep(0.5)
            with self.semaphore:
                if self.RSA_Received == True:
                    break
        
        with self.semaphore:
            return self.strangerRSA

    def Listen(self, chatWindow):

        size = 4096
        while True:

            data = self.connection.recv(size)
    
            frame = pickle.loads(data)
            size = 4096
            if frame == b"":
                pass
            elif frame.frame_type == FrameType.SIZE:
                size = struct.unpack('I', frame.data)
                size = size[0]
            elif frame.frame_type == FrameType.PUBLIC_KEY:
                self.Set_RSA_Received(frame)
            elif frame.frame_type == FrameType.TEXT:
                chatWindow.UpdateOutput("Stranger: " + frame.data)

