import os
import sys
import subprocess
import traceback

from tkinter import *
from tkinter import filedialog

import playsound
from playsound import playsound
playsound('startup.mp3')

import update

import importlib
importlib.reload(update)

def Play(self):
    update.GitSync()
    started = subprocess.Popen([update.Minecraft(), '--workDir', 'dawn'])
    if started:
        self.config(state='disabled')
    return started

window = Tk()
window.title('Dawn')
window.geometry('200x75')
window.geometry('+%d+%d' % window.winfo_pointerxy())
window.play = Button(window, text='Play', width=15)
window.play.place(relx=0.5, rely=0.45, anchor=CENTER)
window.play.config(command=(lambda : Play(window.play)))
window.navbar = Menu(window)
window.options = Menu((window.navbar), tearoff=0)
window.select = window.options.add_command(label='Edit Minecraft Location', command=(lambda : update.Minecraft(-1)) )
window.navbar.add_cascade(label='Options', menu=(window.options))
window.config(menu=(window.navbar))
window.mainloop()
