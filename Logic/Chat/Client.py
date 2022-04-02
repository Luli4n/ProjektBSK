import ctypes
from multiprocessing import BoundedSemaphore
import socket
import struct
import threading
import pickle

from Logic.Chat.Frame import Frame, FrameType
from Logic.Crypto.AESLogic import AESLogic
from Logic.Crypto.SessionKey import SessionKey


class Client:

    def __init__(self,chatWindow):
        self.chatWindow = chatWindow
        self.sessionKeySemaphore = BoundedSemaphore(value=1)
        self.sendAccessSemaphore = BoundedSemaphore(value=1)

    def CreateClient(self,addr, port):

        connected = False
        while not connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((addr,port))
                connected = True
            except Exception as e:
                self.socket.close()
                pass #Do nothing, just try again

    def Set_Stranger_RSA(self,RSAKey):
        with self.sessionKeySemaphore:
            self.strangerRSA = RSAKey

    def Send(self,frame):
        with self.sendAccessSemaphore:
            if frame.frame_type == FrameType.TEXT and frame.data == '':
                return

            if frame.frame_type == FrameType.TEXT:
                self.chatWindow.UpdateOutput("Me: " + frame.data)

            if frame.frame_type != FrameType.PUBLIC_KEY:
                
                session_key = SessionKey.Generate(32)
                with self.sessionKeySemaphore:
                    sessionKeyFrame = SessionKey.PrepareSessionKeyFrame(self.strangerRSA,session_key)
                session_string = pickle.dumps(sessionKeyFrame)
                self.SendSizeFrame(len(session_string))
                frame.data = AESLogic.Encrypt(frame.data,session_key[0:16],session_key[16:32],frame.encrypt_type)
                self.socket.sendall(session_string)

            data_string = pickle.dumps(frame)
            self.SendSizeFrame(len(data_string))
            self.socket.sendall(data_string)


    def SendSizeFrame(self, size):
        size_in_4_bytes = struct.pack('I', size)
        self.socket.sendall(pickle.dumps(Frame(size_in_4_bytes,FrameType.SIZE)))

