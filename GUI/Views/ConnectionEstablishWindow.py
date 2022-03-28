from time import sleep
import ctypes
import threading
from GUI.Views.DefaultWindow import DefaultWindow
import PySimpleGUI as gui



class ConnectionEstablishWindow(DefaultWindow):
    def __init__(self,name, useraddr, client):
        super().__init__(name)
        self.client = client
        self.useraddr = useraddr

    def CreateWindow(self):
        self.window = gui.Window(self.name, self.GetLayout(),element_justification='c')



    def GetLayout(self):
        return [
            [gui.Text("Waiting for " + self.useraddr + " to connect")],     
        ]

    def WindowLoop(self,addr,port):
        threading.Thread(target=self.ClientConnect, daemon=True,args = ([addr,port])).start()
        while True:
            event, values = self.window.read()
            
            if event == "Exit" or event == gui.WIN_CLOSED:
                break


    def ClientConnect(self, addr, port):
        self.client.CreateClient(addr,port)
        sleep(1)
        self.window.write_event_value("Exit", None)
