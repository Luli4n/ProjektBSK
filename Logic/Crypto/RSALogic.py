from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from Logic.Crypto.AESLogic import AESLogic


class RSALogic:

    @staticmethod
    def CreateRSAKeys():
        key = RSA.generate(2048)

        private_key = key.export_key()
        public_key = key.publickey().export_key()

        return public_key,private_key

    @staticmethod
    def SaveKeyToFile(path, value, hash):
        aes_key = hash[0:16]
        aes_iv = hash[16:32]


        encrypted = AESLogic.Encrypt(value,aes_key,aes_iv)

        f = open(path, 'w+b')
        f.write(encrypted)
        f.close()

    @staticmethod
    def GetKeyFromFile(path,hash):
        aes_key = hash[0:16]
        aes_iv = hash[16:32]


        f = open(path,'rb')
        cipher = f.read()
        
        return AESLogic.Decrypt(cipher,aes_key,aes_iv)

    @staticmethod
    def Encrypt(public_key, data):
        key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_OAEP.new(key)
        return cipher_rsa.encrypt(data)

    @staticmethod
    def Decrypt(private_key, enc_data):
        import Logic.Crypto.SessionKey
        key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(key)
        try:
            value = cipher_rsa.decrypt(enc_data)
        except:
            value = Logic.Crypto.SessionKey.SessionKey.Generate(32)
            
        return value

