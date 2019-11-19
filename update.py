import os
import sys

import json
import wget
import time

from tkinter import *
from tkinter import filedialog

from urllib.request import urlopen
from pathlib import Path

import shutil
import tempfile

if getattr( sys, 'frozen', False ):
    location = sys._MEIPASS

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

class Git():
    def __init__(self,CONFIG):
        self.Repo = CONFIG["repo"]
        self.Url = ( "https://api.github.com/repos" +self.Repo )
        self.Old = CONFIG["commit"]
    def contents(self,dir=""):
        return self.fetch("contents/" +dir)
    def fetch(self,api):
        return json.load(urlopen(self.Url+api))
    def latest(self):
        return self.fetch("branches/master")["commit"]["sha"]
    def diff(self):
        self.New = self.latest()
        if self.Old == "" or self.Old == self.New:
            return None
        return self.fetch( "compare/" +self.Old +"..." +self.New )["files"]

CONFIG = JsonConfig()
GIT = Git(CONFIG)

def Minecraft(minecraft=""):
    if minecraft == "":
        return CONFIG["minecraft"]
    elif not os.path.isfile(minecraft):
        options = {}
        options['initialdir'] = os.environ['ProgramFiles(x86)']
        options['title'] = 'Minecraft'
        options['mustexist'] = True
        dir = (filedialog.askdirectory)(**options)
        minecraft = dir + '/MinecraftLauncher.exe'

    CONFIG["minecraft"] = minecraft  
    return minecraft

def GitSync():
    print( "Verification Starting")
    diff = GIT.diff()
    if diff:
        exclude = CONFIG["exclude"]
        for file in diff:
            name = file["filename"]
            path = Path( name )         
            parent = path.parent         
            raw = file["raw_url"]
            status = file["status"]
            if name in exclude or name.endswith(".py"):
                continue                
            parent.mkdir(parents=True, exist_ok=True)
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
                        
            if name == "config.json":
                CONFIG["exclude"] = CONFIG.Decode()["exclude"]
                
            print( status, name )

    print( "Verification Complete!" )
    CONFIG["commit"] = GIT.New
    CONFIG.Write()
    return True

if __name__ == '__main__':
    
    for file in GIT.contents():
        name = file["name"]
        url = file["download_url"]
        move = os.path.join(location,name)
        if ".py" in name:
            wget.download(url,move)

    sys.path.append(location)    
    import main

