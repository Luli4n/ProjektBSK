import threading
import PySimpleGUI as gui
from GUI.Views.ChatWindow import ChatWindow
from GUI.Views.ConnectionWindow import ConnectionWindow
from GUI.Views.LoginWindow import LoginWindow
from Logic.Chat.Server import Server

class WindowManager:

    def MainLoop(self):
        gui.SetOptions(font='Arial 18 normal')
        self.LoginService()

        while self.ConnectionToBeEstablished():
            self.ChatService()

    def LoginService(self):
        loginWindow = LoginWindow('Login')

        loginWindow.CreateWindow()
        self.publicRSA, self.privateRSA = loginWindow.WindowLoop()
        loginWindow.DestroyWindow()

    def ConnectionToBeEstablished(self):
        connectionWindow = ConnectionWindow('Connection')

        connectionWindow.CreateWindow()
        self.connectionString = connectionWindow.WindowLoop()
        connectionWindow.DestroyWindow()

        return False if self.connectionString == '-EXIT-' else True

    def ChatService(self):
        chatWindow = ChatWindow('Chat')

        chatWindow.CreateWindow()

        self.serverThread = threading.Thread(target = self.CreateServer, args = [chatWindow])
        self.serverThread.start()

        chatWindow.WindowLoop()
        chatWindow.DestroyWindow()

        self.DestroyServer()
    
    def CreateServer(self, chatWindow):
        self.server = Server()
        self.server.CreateServer('',11111)
        self.listenThread = threading.Thread(target = self.server.Listen, args = ([chatWindow]))
        self.listenThread.start()

    def DestroyServer(self):
        self.serverThread.join()
        self.listenThread.join()