import os
import sys
import time
import traceback

import subprocess

import json

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from pathlib import Path

try:
    import update
except:
    import __main__ as update
    
def Play(self):
    subprocess.Popen( [ update.Minecraft(), '--workDir', 'dawn' ], close_fds=True, shell=True )

window = Tk()
window.title('Dawn')
window.geometry('200x75')
window.play = Button(window, text='Play', width=15)
window.play.place(relx=0.5, rely=0.45, anchor=CENTER)
window.play.config(command=(lambda : Play(window.play)) )
window.navbar = Menu(window)

window.options = Menu((window.navbar), tearoff=0)
window.update = window.options.add_command(label='Check For Updates', command=( lambda : update.GitSync() ))
window.select = window.options.add_command(label='Edit Minecraft Location', command=( lambda : update.Minecraft(modify=True) ))

window.navbar.add_cascade(label='Options', menu=(window.options))

window.config(menu=(window.navbar))
window.mainloop()
