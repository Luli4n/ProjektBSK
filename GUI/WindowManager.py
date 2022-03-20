import PySimpleGUI as gui
from GUI.Views.ChatWindow import ChatWindow
from GUI.Views.ConnectionWindow import ConnectionWindow
from GUI.Views.LoginWindow import LoginWindow

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
        chatWindow.WindowLoop()
        chatWindow.DestroyWindow()