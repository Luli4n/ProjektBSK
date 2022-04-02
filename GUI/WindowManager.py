from this import d
import threading
import PySimpleGUI as gui
from GUI.Views.ChatWindow import ChatWindow
from GUI.Views.ConnectionEstablishWindow import ConnectionEstablishWindow
from GUI.Views.ConnectionWindow import ConnectionWindow
from GUI.Views.LoginWindow import LoginWindow
from Logic.Chat.Client import Client
from Logic.Chat.Frame import Frame, FrameType
from Logic.Chat.Server import Server

class WindowManager:

    def MainLoop(self):
        gui.SetOptions(font='Arial 18 normal')
        self.LoginService()

        if self.ConnectionToBeEstablished():
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
        self.chatWindow = ChatWindow('Chat')  

        self.serverThread = threading.Thread(target = self.CreateServer, args = [self.chatWindow])
        self.serverThread.start()
        self.ClientConnect()
        self.server.Set_Client(self.client)

        self.SendPublicKey()
        self.WaitForStrangerKey()

        self.chatWindow.CreateWindow()
        self.chatWindow.WindowLoop(self.client)
        self.chatWindow.DestroyWindow()

        self.server.Set_Exit(True)
        self.client.Send(Frame('',FrameType.EXIT))

        self.listenThread.join()
        self.serverThread.join()

        self.DestroyServer()
    
    def CreateServer(self, chatWindow):
        self.server = Server(self.privateRSA)
        self.server.CreateServer('',8083)
        self.listenThread = threading.Thread(target = self.server.Listen, args = ([chatWindow]))
        self.listenThread.start()

    def ClientConnect(self):
        self.client = Client(self.chatWindow)
        self.connectionWait = ConnectionEstablishWindow('Oczekiwanie na rozmowce',self.connectionString,self.client)
        self.connectionWait.CreateWindow()
        self.connectionWait.WindowLoop('',8082)
        self.connectionWait.DestroyWindow()

    def SendPublicKey(self):
        frame = Frame(self.publicRSA,FrameType.PUBLIC_KEY)
        self.client.Send(frame)
    
    def WaitForStrangerKey(self):
        self.strangerRSA = self.server.Get_RSA_Received()
        self.client.Set_Stranger_RSA(self.strangerRSA)

    def DestroyServer(self):
        self.serverThread.join()
        self.listenThread.join()