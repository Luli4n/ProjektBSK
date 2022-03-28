from enum import Enum


class Frame:

    def __init__(self, data, frame_type, file_extension = ""):
        self.data = data
        self.file_extension = file_extension
        self.frame_type = frame_type



class FrameType(Enum):
    PUBLIC_KEY = 1
    SESSION_KEY = 2
    TEXT = 3
    FILE = 4
    ACK = 5
    SIZE = 6