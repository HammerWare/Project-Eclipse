import os
import sys
import time
import traceback

import subprocess

import json

from tkinter import *
from tkinter import filedialog

from pathlib import Path

class JsonConfig():
    def __init__(self,dir="config.json"):
        self.Path = Path(dir)
        self.Reload()
    def Reload(self):
        self.Table = self.Decode()
    def Decode(self):
        return json.loads(self.Path.read_text())
    def Encode(self):
        return json.dumps(self.Table,indent=4)         
    def __getitem__(self, item):
        return self.Decode()[item]
    def __setitem__(self, item, value):
        self.Table[item] = value
    def Write(self):
        self.Path.write_text(self.Encode())       

SAVED = JsonConfig()

def Minecraft(change=False):
    minecraft = SAVED["minecraft"]
    file = "MinecraftLauncher.exe"
    valid = all([ 
        os.path.isfile(minecraft), 
        minecraft.endswith(file)
    ])
    if not valid or change: 
        options = {}
        options['initialdir'] = os.environ['ProgramFiles(x86)']
        options['title'] = 'Minecraft Folder'
        options['mustexist'] = True
        dir = (filedialog.askdirectory)(**options)
        minecraft = os.path.join(dir,file)
        SAVED["minecraft"] = minecraft  
    return minecraft

    
def Play(self):
    subprocess.Popen( [ Minecraft(), '--workDir', 'dawn' ], close_fds=True, shell=True )

window = Tk()
window.title('Dawn')
window.geometry('200x75')
window.play = Button(window, text='Play', width=15)
window.play.place(relx=0.5, rely=0.45, anchor=CENTER)
window.play.config(command=(lambda : Play(window.play)) )
window.navbar = Menu(window)

window.options = Menu((window.navbar), tearoff=0)
window.select = window.options.add_command(label='Edit Minecraft Location', command=(lambda : Minecraft(change=True)) )

window.navbar.add_cascade(label='Options', menu=(window.options))

window.config(menu=(window.navbar))
window.mainloop()
