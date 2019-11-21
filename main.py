import os
import sys
import subprocess
import traceback
import time

from tkinter import *
from tkinter import filedialog

import update
update.GitSync()

def Play(self):
    subprocess.Popen([update.Minecraft(), '--workDir', 'dawn'],stdout=subprocess.DEVNULL)

def Discord():
    print("discord")
    pass

window = Tk()
window.title('Dawn')
window.geometry('200x75')
window.play = Button(window, text='Play', width=15)
window.play.place(relx=0.5, rely=0.45, anchor=CENTER)
window.play.config(command=(lambda : Play(window.play)) )
window.navbar = Menu(window)

window.options = Menu((window.navbar), tearoff=0)
window.select = window.options.add_command(label='Edit Minecraft Location', command=(lambda : update.Minecraft(-1)) )
window.select = window.options.add_command(label='Toggle Discord Status', command=(lambda : Discord()) )

window.navbar.add_cascade(label='Options', menu=(window.options))

window.config(menu=(window.navbar))
window.mainloop()
