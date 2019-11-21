import os
import sys

import json
import wget
import time
import traceback

import winreg

from tkinter import *
from tkinter import filedialog

from urllib.request import urlopen
from pathlib import Path

def GetInfo():
    ret = lambda: None
    ret.IsDev = ( "--dev" in sys.argv )
    ret.IsBundle = hasattr(sys, '_MEIPASS')
    ret.Location = os.getcwd()
    if ret.IsBundle:
        ret.Location = sys._MEIPASS
    return ret

class Registry():
    def __init__(self,path,user=winreg.HKEY_CURRENT_USER):
        self.User = user
        self.Path = path
        self.Main = self.load()
    def load(self):
        try:
            self.Valid = True
            return winreg.OpenKey(self.User,self.Path,0,winreg.KEY_ALL_ACCESS)
        except:
            self.Valid = False
            return winreg.CreateKey(self.User,self.Path)
    def __setitem__(self,item,value):
        winreg.SetValueEx(self.Main,item,0,winreg.REG_SZ,value)
    def __getitem__(self,item=''):
        try:
            return winreg.QueryValueEx(self.Main,item)[0]
        except:
            pass
        return False

class Git():
    def __init__(self,CONFIG):
        self.Repo = CONFIG["repo"]
        self.Url = ( "https://api.github.com/repos" +self.Repo )
        self.Old = CONFIG["commit"]
        self.New = self.latest()
    def contents(self,dir=""):
        return self.fetch("contents/" +dir)
    def fetch(self,api):
        try:
            return json.load(urlopen(self.Url+api))
        except URLError as e:
            print('URL ERROR:', e.reason, e.code)
            return None
    def latest(self):
        return self.fetch("branches/master")["commit"]["sha"]
    def diff(self):
        if self.Old == "0":
            self.Old = self.New
        if self.Old == self.New:
            return None
        return self.fetch( "compare/" +self.Old +"..." +self.New )["files"]

def GitSync():
    if not SELF.IsBundle:
        return None
    
    print( "Verification Started" )
    diff = GIT.diff()
    if diff:
        for file in diff:
            name = file["filename"]
            path = Path( name )         
            parent = path.parent         
            raw = file["raw_url"]
            status = file["status"]
            parent.mkdir(parents=True, exist_ok=True)
            if len(path.parents) <= 1:
                continue
            if status == "added" or status == "modified":
                temp = Path(wget.download(raw))
                temp.replace(path)
            elif status == "renamed":
                previous = Path(file["previous_filename"])   
                if previous.is_file():
                    previous.unlink()
                temp = Path(wget.download(raw))
                temp.replace(path)                    
            elif status == "removed":
                if path.is_file():
                    path.unlink()
                if parent.is_dir():
                    empty = list(os.scandir(parent)) == 0
                    if empty:
                        parent.rmdir()
                
            print( status, name )
            
    CONFIG["commit"] = GIT.New  
    print( "Verification Complete" )
    return True

def Minecraft(change=False):
    minecraft = CONFIG["minecraft"]
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
        CONFIG["minecraft"] = minecraft  
    return minecraft

###########GLOBAL#############

SELF = GetInfo()
CONFIG = Registry("SOFTWARE\Dawn")
if not CONFIG.Valid:
    CONFIG["minecraft"] = "C:/Program Files (x86)/Minecraft/MinecraftLauncher.exe"
    CONFIG["repo"] = "/TheMerkyShadow/Project-Dawn/"
    CONFIG["commit"] = "0"
GIT = Git(CONFIG)

###########GLOBAL#############

def start():
    if SELF.IsBundle:
        sys.path.append(SELF.Location)
        
        for file in GIT.contents():
            name = file["name"]
            obj = file["type"]
            url = file["download_url"]
            mount = os.path.join(SELF.Location,name)
            if name.endswith(".py"):
                wget.download(url,mount)              
        
    import main
    
if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        input(traceback.format_exc())
        pass
