import PySimpleGUI as gui

class DefaultWindow:
    def __init__(self,name):
        self.name = name

    def CreateWindow(self):
        self.window = gui.Window(self.name, self.GetLayout(),element_justification='c')
    
    def GetLayout(self):
        return [gui.Text("Default window layout")]

    def WindowLoop(self):
        while True:
            event, values = self.window.read()

            if event == "Exit" or event == gui.WIN_CLOSED:
                break
            
    def DestroyWindow(self):
        self.window.close()