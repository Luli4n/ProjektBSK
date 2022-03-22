import socket


class Client:

    def CreateClient(self,addr, port):

        connected = False
        while not connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((addr,port))
                connected = True
            except Exception as e:
                self.socket.close()
                pass #Do nothing, just try again