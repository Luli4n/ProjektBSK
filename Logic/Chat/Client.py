import ctypes
import socket
import struct
import threading
import pickle

from Logic.Chat.Frame import Frame, FrameType


class Client:

    def __init__(self,chatWindow):
        self.chatWindow = chatWindow

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

    def Send(self,frame):
        data_string = pickle.dumps(frame)
        # tutaj szyfrowanie
        if frame.frame_type != FrameType.PUBLIC_KEY:
            size = len(data_string)
            size_in_4_bytes = struct.pack('I', size)
            self.socket.sendall(pickle.dumps(Frame(size_in_4_bytes,FrameType.SIZE)))

        self.socket.sendall(data_string)

        if frame.frame_type == FrameType.TEXT:
            self.chatWindow.UpdateOutput("Me: " + frame.data)