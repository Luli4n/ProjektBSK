import hashlib
from os.path import exists

from Logic.Crypto.RSALogic import RSALogic

class LoginPolicy:
    publicKeyPath = 'Keys/Public/key'
    privateKeyPath = 'Keys/Private/key'

    def LoadKeysFromFiles(self,password):
        hash = hashlib.blake2s(bytes(password,'utf-8'),digest_size=32).digest()

        if not exists(self.publicKeyPath) or not exists(self.privateKeyPath):
            public, private = RSALogic.CreateRSAKeys() # RSA Class
            RSALogic.SaveKeyToFile(self.publicKeyPath, public, hash)
            RSALogic.SaveKeyToFile(self.privateKeyPath, private, hash)
            return public, private
        else:
            try:
                public = RSALogic.GetKeyFromFile(self.publicKeyPath, hash) # Also RSA Class ?
            except:
                public, _ = RSALogic.CreateRSAKeys()
            try:
                private = RSALogic.GetKeyFromFile(self.privateKeyPath, hash)
            except:
                _,private = RSALogic.CreateRSAKeys() 

            return public, private 

