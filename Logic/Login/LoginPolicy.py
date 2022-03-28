import hashlib
from os.path import exists

from Logic.Crypto.RSAKeysManagement import RSAKeysManagement

class LoginPolicy:
    publicKeyPath = 'Keys/Public/key'
    privateKeyPath = 'Keys/Private/key'

    def __init__(self):
        self.rsaManager = RSAKeysManagement()

    def LoadKeysFromFiles(self,password):
        hash = hashlib.blake2s(bytes(password,'utf-8'),digest_size=32).digest()

        if not exists(self.publicKeyPath) or not exists(self.privateKeyPath):
            public, private = self.rsaManager.CreateRSAKeys() # RSA Class
            self.rsaManager.SaveKeyToFile(self.publicKeyPath, public, hash)
            self.rsaManager.SaveKeyToFile(self.privateKeyPath, private, hash)
            return public, private
        else:
            try:
                public = self.rsaManager.GetKeyFromFile(self.publicKeyPath, hash) # Also RSA Class ?
            except:
                public, _ = self.rsaManager.CreateRSAKeys()
            try:
                private = self.rsaManager.GetKeyFromFile(self.privateKeyPath, hash)
            except:
                _,private = self.rsaManager.CreateRSAKeys() 

            return public, private 

