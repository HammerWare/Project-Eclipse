import os
import sys

import subprocess

from tkinter import *

import update

def Play(self):
    subprocess.Popen([ update.Minecraft(), '--workDir', os.path.join(os.getcwd(),'dawn') ],creationflags=0x00000010)

window = Tk()
window.title('Dawn')
window.geometry('200x75')
window.play = Button(window, text='Play', width=15)
window.play.place(relx=0.5, rely=0.45, anchor=CENTER)
window.play.config(command=(lambda : Play(window.play)) )
window.navbar = Menu(window)

window.options = Menu((window.navbar), tearoff=0)
window.update = window.options.add_command(label='Check For Updates', command=( lambda : update.GitManager().Sync() ))

window.navbar.add_cascade(label='Options', menu=(window.options))

window.config(menu=(window.navbar))
window.mainloop()
