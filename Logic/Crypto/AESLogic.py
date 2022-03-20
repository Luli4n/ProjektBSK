from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESLogic:

    def Encrypt(self, value, key, iv):
        cipher = AES.new(bytes(key), AES.MODE_CBC,bytes(iv))
        return cipher.encrypt(pad(value, AES.block_size))

    def Decrypt(self, ciphertext, key, iv):
        cipher = AES.new(bytes(key), AES.MODE_CBC, bytes(iv))
        return unpad(cipher.decrypt(ciphertext), AES.block_size)