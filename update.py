import os
import sys
sys.path.insert(0,os.getcwd())

import json
import wget
import time
import traceback

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from urllib.request import urlopen
from pathlib import Path

def Notify(msg,log=False):
    if log:
        print( msg, file=log )
    messagebox.showinfo(title=None,message=msg)
    
class SavedConfig():
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
        self.Write()
    def Write(self):
        self.Path.write_text(self.Encode())       

class GitStatus():
    def __init__(self,config=SavedConfig()):
        self.Repo = config["repo"]
        self.Url = ( "https://api.github.com/repos" +self.Repo )
        self.Old = config["commit"]
        self.New = self.latest()
    def contents(self,dir=""):
        return self.fetch("contents/" +dir)
    def fetch(self,api):
        try:
            return json.load(urlopen(self.Url+api))
        except URLError as e:
            print('URL ERROR:',str(e))
            return None
    def latest(self):
        return self.fetch("branches/master")["commit"]["sha"]
    def diff(self):
        if self.Old == "0":
            self.Old = self.New
            return None
        elif self.Old == self.New:
            return None
        return self.fetch( "compare/" +self.Old +"..." +self.New )["files"]

def GitSync():
    with open("log", "w+" ) as log:
        exclude = [ "dawn.exe" ]
        config = SavedConfig()
        git = GitStatus()
        Notify( "Verification Started", log )
        diff = git.diff()
        if diff:
            for file in diff:
                name = file["filename"]
                path = Path( name )         
                parent = path.parent         
                raw = file["raw_url"]
                status = file["status"]
                parent.mkdir(parents=True, exist_ok=True)
            
                if name in exclude:
                    continue
                elif status == "added" or status == "modified":
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
                
                print( status, name, file = log )
            
        config["commit"] = git.latest()
        Notify("Verification Complete", log )
    sys.exit()

def Minecraft(config=SavedConfig(),modify=False):
    minecraft = config["minecraft"]
    file = "MinecraftLauncher.exe"
    valid = all([ 
        os.path.isfile(minecraft), 
        minecraft.endswith(file)
    ])
    if not valid or modify: 
        options = {}
        options['initialdir'] = os.environ['ProgramFiles(x86)']
        options['title'] = 'Minecraft Folder'
        options['mustexist'] = True
        dir = (filedialog.askdirectory)(**options)
        minecraft = os.path.join(dir,file)
        config["minecraft"] = minecraft  
    return minecraft

if __name__ == '__main__':
    try:
        import menu
    except Exception as e:
        Notify(traceback.format_exc())
