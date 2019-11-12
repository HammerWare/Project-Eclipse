import os
import sys

import json
import wget
import time
import datetime

from urllib.request import urlopen
from pathlib import Path

import traceback

def notify(text,delay=2):
    print(text)
    time.sleep(delay)
    return

def config(save,key=None,value=None):
    file = Path("config.json")
    decode = json.loads(file.read_text())
    if save:
        decode[key] = value            
        encode = json.dumps(decode,indent=4)
        file.write_text(encode)
        decode = encode
    return decode

def Minecraft(minecraft=""):
    minecraft = config(False)["minecraft"]        
    if not os.path.isfile(minecraft):
        minecraft = input("Enter Minecraft Launcher: ")
    return Minecraft(minecraft)

def GitDiff():    
    repo = config(False)["repo"]
    api = ( "https://api.github.com/repos" +repo ) 
    fetch = (api +"branches/master")  
    new = json.load(urlopen(fetch))["commit"]["sha"]
    old = config(False)["commit"]
    if old == "":
        old = new
    elif( old == new ):
        return ( old, None, new )
    fetch = ( api +"compare/" +old +"..." +new )
    return ( old, json.load(urlopen(fetch))["files"], new )
    
def GitSync(backup=False):
    notify( "Verification Starting")
    current = Minecraft()    
    old, diff, new = GitDiff()
    if diff:
        exclude = config(False)["exclude"]
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
        
    config(True, "minecraft", current )
    config(True, "commit", new )
    notify( "Verification Complete!" )
