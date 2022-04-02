from cgitb import enable
from multiprocessing import BoundedSemaphore
import threading
from GUI.Views.DefaultWindow import DefaultWindow
import PySimpleGUI as gui
from Logic.Chat.FileLoader import FileLoader
from Logic.Chat.Frame import Frame, FrameType

from Logic.Login.LoginPolicy import LoginPolicy


class ChatWindow(DefaultWindow):
    def __init__(self,name):
        super().__init__(name)
        self.semaphore = BoundedSemaphore(value=1)
        self.ExitSemaphore = BoundedSemaphore(value=1)

        self.exitFlag = False
        self.encrypt_type = '-CBC-'

    def CreateWindow(self):
        self.window = gui.Window(self.name, self.GetLayout(), default_button_element_size=(20,2), use_default_focus=False, finalize=True)
        self.window.Element('-OUT-').bind("<FocusIn>", '+FOCUS_IN+')
        self.window.Element('-OUT-').bind("<FocusOut>", '+FOCUS_OUT+')
        self.window['-IN-'].bind("<Return>", "_ENTER")

    def GetLayout(self):
        return [
          [gui.In(size=(50,1), disabled=True), gui.FileBrowse(key='-FILE-'), gui.Button('Send_File')],
          [gui.Text('', font=('Courier 12'),size=(50, 1), key='-PROGRESS-')],
          [gui.Multiline(size=(50, 20), key='-OUT-', enter_submits=False),gui.Radio('ECB', "RADIO1", default=False, key="-ECB-",enable_events=True), gui.Radio('CBC', "RADIO1", default=True,key="-CBC-",enable_events=True)],
          [gui.Text('', size=(50, 1), key='-ALERTS-')],
          [gui.Multiline(size=(50, 5), enter_submits=False, key='-IN-',enable_events=True),
           gui.Button('Send', button_color=(gui.YELLOWS[0], gui.BLUES[0]), bind_return_key=True)]
           ]

    def WindowLoop(self,client):
        while True:

            with self.ExitSemaphore:
                if self.exitFlag:
                    break

            event, values = self.window.read(timeout=100)

            if event == gui.WIN_CLOSED:
                return '-EXIT-'

            if event == '-CBC-' or event == '-ECB-':
                self.encrypt_type = event

            if len(str(values['-IN-'])) > 5000:
                self.window.Element('-IN-').Update(values['-IN-'][0:5000])

            if event == "Send" or event == '-IN-_ENTER':
                frame = Frame(values['-IN-'],FrameType.TEXT,encrypt_type=self.encrypt_type)
                client.Send(frame)
                self.window.Element('-IN-').Update('')
            
            if event == "Send_File":
                fl = FileLoader(self)
                self.flThread = threading.Thread(target = fl.SendFile, args = [values['-FILE-'],client,self.encrypt_type])
                self.flThread.start()

                

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

    def UpdateBar(self,bar):
        bar_control = self.window['-PROGRESS-']
        bar_control.update(bar)
    
    def SetExitFlag(self,value):
        self.exitFlag = value
