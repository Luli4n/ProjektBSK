from enum import Enum
import pickle


class Frame:

    def __init__(self, data, frame_type, file_extension = "", encrypt_type = 'NO'):
        self.data = data
        self.file_extension = file_extension
        self.frame_type = frame_type
        self.encrypt_type = encrypt_type


class FrameType(Enum):
    PUBLIC_KEY = 1
    SESSION_KEY = 2
    TEXT = 3
    FILE = 4
    ACK = 5
    SIZE = 6
    EXIT = 7