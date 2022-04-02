from multiprocessing import BoundedSemaphore
import select
import socket, pickle
from struct import Struct
import struct
from time import sleep

from Logic.Chat.Frame import Frame, FrameType
from Logic.Crypto.AESLogic import AESLogic
from Logic.Crypto.RSALogic import RSALogic

HEADER = Struct("!L")

class Server:

    
    
    def __init__(self, private_rsa):
        self.semaphore = BoundedSemaphore(value=1)
        self.exitSemaphore = BoundedSemaphore(value=1)
        self.private_rsa = private_rsa

        with self.semaphore:
            self.RSA_Received = False

        with self.exitSemaphore:
            self.Exit = False
        
        

    def CreateServer(self, addr, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((addr, port))
        self.socket.listen()
        (self.connection, self.address) = self.socket.accept() 

    def Set_Exit(self,value):
        self.Exit = value

    def Set_RSA_Received(self,frame):
        with self.semaphore:
            self.strangerRSA = frame.data
            self.RSA_Received = True

    def Set_Client(self, client):
        self.client = client

    def Get_RSA_Received(self):
        while True:
            sleep(0.5)
            with self.semaphore:
                if self.RSA_Received == True:
                    break
        
        with self.semaphore:
            return self.strangerRSA

    def Listen(self, chatWindow):

        SIZE_Frame_size = len(pickle.dumps(Frame(struct.pack('I', 420),FrameType.SIZE)))
        size = SIZE_Frame_size

        while True:

            data = self.connection.recv(size)
    
            frame = pickle.loads(data)
            size = SIZE_Frame_size
            if frame == b"":
                pass
            elif frame.frame_type == FrameType.SIZE:
                size = struct.unpack('I', frame.data)
                size = size[0]
            elif frame.frame_type == FrameType.PUBLIC_KEY:
                self.Set_RSA_Received(frame)
            elif frame.frame_type == FrameType.SESSION_KEY:
                enc_session_key = frame.data
                self.stranger_session_key = RSALogic.Decrypt(self.private_rsa,enc_session_key)
            elif frame.frame_type == FrameType.TEXT:
                try:
                    frame.data = AESLogic.Decrypt(frame.data,self.stranger_session_key[0:16],self.stranger_session_key[16:32],frame.encrypt_type).decode('utf-8')
                except:
                    frame.data = frame.data
                chatWindow.UpdateOutput("Stranger: " + str(frame.data))
            elif frame.frame_type == FrameType.EXIT:
                with self.exitSemaphore:
                    self.Exit = True

            with self.exitSemaphore:
                if self.Exit:
                    self.client.Send(Frame('',FrameType.EXIT))
                    chatWindow.SetExitFlag(True)
                    chatWindow.window.refresh()
                    break

