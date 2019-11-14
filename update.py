import os
import sys

import json
import wget
import time

from urllib.request import urlopen
from pathlib import Path

def notify(text,delay=2):
    print(text)
    time.sleep(delay)
    return

class JsonConfig():
    def __init__(self,dir="config.json"):
        self.Path = Path(dir)    
        self.Table = self.Decode()
    def Decode(self):
        return json.loads(self.Path.read_text())
    def Encode(self):
        return json.dumps(self.Table,indent=4)         
    def __getitem__(self, item):
        return self.Table[item] 
    def __setitem__(self, item, value):
        self.Table[item] = value
    def Close(self):
        self.Path.write_text( self.Encode() )
    def Reload(self):
        return self.Decode()        

class Git():
    def __init__(self,CONFIG):
        self.Repo = CONFIG["repo"]     
        self.Url = ( "https://api.github.com/repos" +self.Repo )
        self.Old = CONFIG["commit"]
        self.New = self.latest()
    def fetch(self,api):
        return json.load(urlopen(self.Url+api))
    def latest(self):
        return self.fetch("branches/master")["commit"]["sha"]
    def diff(self):
        if self.Old == "" or self.Old == self.New:
            return None
        return self.fetch( "compare/" +self.Old +"..." +self.New )["files"]
    
CONFIG = JsonConfig()
GIT = Git( CONFIG )

def Minecraft(minecraft=None):
    if minecraft is None:
        minecraft = CONFIG["minecraft"]
    if not os.path.isfile(minecraft):
        minecraft = input("Enter Minecraft Launcher: ") 
        CONFIG["minecraft"] = minecraft
    return minecraft

def GitSync():
    notify( "Verification Starting")
    diff = GIT.diff()
    if diff:
        for file in diff:
            name = file["filename"]
            path = Path(name)
            parent = path.parent         
            raw = file["raw_url"]
            status = file["status"]
            if name == exclude:
                continue                
            parent.mkdir(parents=True, exist_ok=True)
            if status == "added" or status == "modified":              
                temp = Path(wget.download(raw))
                temp.replace(path)
            elif status == "renamed":
                previous = Path(file["previous_filename"])
                if previous.is_file():
                    previous.replace(path)
                elif status == "removed":
                    if path.is_file():
                        path.unlink()
                    if parent.is_dir():
                        empty = list(os.scandir(parent)) == 0
                        if empty:
                            parent.rmdir()
                            
            print( status, name )

    notify( "Verification Complete!" )
    CONFIG["commit"] = GIT.New
    CONFIG.Close()
