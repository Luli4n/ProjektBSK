from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESLogic:
    
    @staticmethod
    def Encrypt(value, key, iv, mode='-CBC-'):
        if isinstance(value,str):
            value = bytes(value,encoding='utf-8')
        if mode == '-ECB-':
            key = b''.join([key,iv])
            cipher = AES.new(bytes(key), AES.MODE_ECB)
        else:
            cipher = AES.new(bytes(key), AES.MODE_CBC,bytes(iv))
        return cipher.encrypt(pad(value, AES.block_size))

    @staticmethod
    def Decrypt(ciphertext, key, iv, mode='-CBC-'):
        if mode == '-ECB-':
            key = b''.join([key,iv])
            cipher = AES.new(bytes(key), AES.MODE_ECB)
        else: 
            cipher = AES.new(bytes(key), AES.MODE_CBC, bytes(iv))
        return unpad(cipher.decrypt(ciphertext), AES.block_size)

    


