from GUI.Views.DefaultWindow import DefaultWindow
import PySimpleGUI as gui

from Logic.Login.LoginPolicy import LoginPolicy


class LoginWindow(DefaultWindow):
    def __init__(self,name):
        super().__init__(name)

    def CreateWindow(self):
        self.window = gui.Window(self.name, self.GetLayout(),element_justification='c')

    def GetLayout(self):
        return [
            [gui.Text("Podaj hasło")],
            [gui.In(size=(25, 1), enable_events=True, key="-INPUT-",password_char='*')],
            [gui.Button('Submit',key="-SUBMIT-",visible=False, bind_return_key=True)]
        ],

    def WindowLoop(self):
        while True:
            event, values = self.window.read()
            
            if event == "Exit" or event == gui.WIN_CLOSED:
                break

            if event == "-SUBMIT-":
                login = LoginPolicy()
                return login.LoadKeysFromFiles(values['-INPUT-'])

