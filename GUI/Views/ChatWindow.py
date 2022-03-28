from cgitb import enable
from multiprocessing import BoundedSemaphore
from GUI.Views.DefaultWindow import DefaultWindow
import PySimpleGUI as gui
from Logic.Chat.Frame import Frame, FrameType

from Logic.Login.LoginPolicy import LoginPolicy


class ChatWindow(DefaultWindow):
    def __init__(self,name):
        super().__init__(name)
        self.semaphore = BoundedSemaphore(value=1)

    def CreateWindow(self):
        self.window = gui.Window(self.name, self.GetLayout(), default_button_element_size=(20,2), use_default_focus=False, finalize=True)
        self.window.Element('-OUT-').bind("<FocusIn>", '+FOCUS_IN+')
        self.window.Element('-OUT-').bind("<FocusOut>", '+FOCUS_OUT+')
        self.window['-IN-'].bind("<Return>", "_ENTER")

    def GetLayout(self):
        return [
          [gui.Multiline(size=(97, 20), font=('Helvetica 14'), key='-OUT-', enter_submits=False)],
          [gui.Text('', size=(70, 1), key='-ALERTS-')],
          [gui.Text('', size=(70, 1), key='-PROGRESS-')],
          [gui.Multiline(size=(70, 5), enter_submits=False, key='-IN-',enable_events=True),
           gui.Button('SEND', button_color=(gui.YELLOWS[0], gui.BLUES[0]), bind_return_key=True),
           gui.Button('EXIT', button_color=(gui.YELLOWS[0], gui.GREENS[0]))]
           ]

    def WindowLoop(self,client):
        while True:
            event, values = self.window.read()
            
            if len(str(values['-IN-'])) > 5000:
                self.window.Element('-IN-').Update(values['-IN-'][0:5000])

            if event == "Exit" or event == gui.WIN_CLOSED:
                return '-EXIT-'

            if event == "SEND" or event == '-IN-_ENTER':
                frame = Frame(values['-IN-'],FrameType.TEXT)
                client.Send(frame)
                self.window.Element('-IN-').Update('')

            if event == '-OUT-+FOCUS_IN+':
                widget = self.window['-OUT-'].Widget
                widget.bind("<1>", widget.focus_set())
                self.window['-OUT-'].update(disabled=True)
            elif event == '-OUT-+FOCUS_OUT+':
                self.window['-OUT-'].Widget.unbind("<1>")
                self.window['-OUT-'].update(disabled=False)

    def UpdateOutput(self,text):
        with self.semaphore:
            output = self.window['-OUT-']
            output.print(text)