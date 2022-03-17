import hashlib
from os.path import exists

class LoginPolicy:
    publicKeyPath = './Keys/Public/key'
    privateKeyPath = './Keys/Private/key'

    def LoadKeysFromFiles(self,password):
        hash = hashlib.blake2s(digest_size=32).update(bytes(password,'utf-8')).hexdigest()

        if not exists(self.publicKeyPath) or not exists(self.privateKeyPath):
            public, private = CreateRSAKeys(hash) # RSA Class
            return public, private
        else:
            
            public = GetKeyFromFile(path, hash) # Also RSA Class ?
            private = GetKeyFromFile(path, hash)

            return public, private 

