import os
import sys
import subprocess
import time

from tkinter import *
from pypresence import *

from tkinter import filedialog
from pypresence import Presence

import update

def Minecraft(change=False):
    minecraft = update.CONFIG['minecraft']
    if not change and os.path.isfile(minecraft):
        return minecraft
    else:
        options = {}
        options['initialdir'] = os.environ['ProgramFiles(x86)']
        options['title'] = 'Minecraft'
        options['mustexist'] = True
        dir = filedialog.askdirectory(**options)
        minecraft = (dir +'/MinecraftLauncher.exe')

    update.CONFIG['minecraft'] = minecraft
    return minecraft

def DiscordUpdate():
    client_id = '644400056941936640'
    RPC = Presence(client_id)
    RPC.connect()
    update = {}
    update['state'] = 'A True Minecraft Experience'
    RPC.update(**update)
    return update

def Play(self):
    update.GitSync()
    started = subprocess.Popen([Minecraft(), '--workDir', 'dawn'])
    if started:
        DiscordUpdate()
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
window.select = window.options.add_command(label='Edit Minecraft Location', command=(lambda : Minecraft(change=True)))
window.navbar.add_cascade(label='Options', menu=(window.options))

window.config(menu=(window.navbar))
window.mainloop()
