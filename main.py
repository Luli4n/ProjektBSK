from GUI.Views.DefaultWindow import DefaultWindow
from GUI.Views.LoginWindow import LoginWindow
import PySimpleGUI as gui
import hashlib

pwd_hash = hashlib.sha512()
pwd_hash.update(b"password")

gui.SetOptions(font='Arial 18 normal')
lw = LoginWindow(pwd_hash.digest())
lw.CreateWindow()
lw.WindowLoop()
lw.DestroyWindow()