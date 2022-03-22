import socket


class Server:

    def CreateServer(self, addr, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((addr, port))
        self.socket.listen()
        (self.connection, self.address) = self.socket.accept() 

    def Listen(self, chatWindow):
        while True:
            received = self.connection.recv(1024)
            if received ==' ':
                pass
            else:
                chatWindow.UpdateOutput(received.decode())