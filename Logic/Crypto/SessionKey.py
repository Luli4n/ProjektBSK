from secrets import token_bytes

from Logic.Chat.Frame import Frame, FrameType
from Logic.Crypto.RSALogic import RSALogic

class SessionKey:

    @staticmethod
    def Generate(length):
        return token_bytes(length)

    @staticmethod
    def PrepareSessionKeyFrame(public_key,plain_session_key):

        enc_session_key = RSALogic.Encrypt(public_key,plain_session_key)

        return Frame(enc_session_key, FrameType.SESSION_KEY)
        