import os
import sys

import json
import wget
import time

from urllib.request import urlopen
from pathlib import Path

class Config():
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
        
CONFIG = Config()

def notify(text,delay=2):
    print(text)
    time.sleep(delay)
    return

def Minecraft(minecraft=None):
    if minecraft is None:
        minecraft = CONFIG["minecraft"]
    if not os.path.isfile(minecraft):
        minecraft = input("Enter Minecraft Launcher: ") 
        CONFIG["minecraft"] = minecraft
    return minecraft

def GitDiff():    
    repo = CONFIG["repo"]
    api = ( "https://api.github.com/repos" +repo ) 
    fetch = (api +"branches/master")  
    new = json.load(urlopen(fetch))["commit"]["sha"]
    old = CONFIG["commit"]
    if old == "":
        old = new
    elif( old == new ):
        return ( old, None, new )
    fetch = ( api +"compare/" +old +"..." +new )
    return ( old, json.load(urlopen(fetch))["files"], new )
    
def GitSync(backup=False):
    notify( "Verification Starting")
    old, diff, new = GitDiff()
    if diff:
        exclude = CONFIG["exclude"]
        for file in diff:
            name = file["filename"]
            path = Path(name)
            parent = path.parent         
            raw = file["raw_url"]
            status = file["status"]
            if name in exclude:
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
    CONFIG["commit"] = new    
    CONFIG.Close()
