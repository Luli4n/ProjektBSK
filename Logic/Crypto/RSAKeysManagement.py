from Crypto.PublicKey import RSA

from Logic.Crypto.AESLogic import AESLogic

class RSAKeysManagement:

    def CreateRSAKeys(self):
        key = RSA.generate(2048)

        private_key = key.export_key()
        public_key = key.publickey().export_key()

        return public_key,private_key

    def SaveKeyToFile(self, path, value, hash):
        aes_key = hash[0:16]
        aes_iv = hash[16:32]
        aesLogic = AESLogic()

        encrypted = aesLogic.Encrypt(value,aes_key,aes_iv)

        f = open(path, 'w+b')
        f.write(encrypted)
        f.close()

    def GetKeyFromFile(self,path,hash):
        return 0


