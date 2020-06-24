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

import urllib
from urllib.request import urlopen

from pathlib import Path

def Notify(msg):
    return messagebox.showinfo(title=None, message=msg)

class SavedConfig:
    def __init__(self, dir='config.json'):
        self.Path = Path(dir)
        self.Reload()
    def Reload(self):
        self.Table = self.Decode()
    def Decode(self):
        return json.loads(self.Path.read_text())
    def Encode(self):
        return json.dumps((self.Table), indent=4)
    def __getitem__(self, item):
        return self.Decode()[item]
    def __setitem__(self, item, value):
        self.Table[item] = value
        self.Write()
    def Write(self):
        self.Path.write_text(self.Encode())

class GitManager:
    def __init__(self, branch='master'):
        self.Config = SavedConfig()
        self.Repo = self.Config['repo']
        self.Url = 'https://api.github.com/repos' + self.Repo
        self.Branch = branch
        self.Old = self.Config['commit']
        self.New = self.latest()
        self.Diff = self.diff()
    def fetch(self, api, exact=False):
        try:
            if exact:
                return urlopen(api).read().decode('utf-8')
            return json.load(urlopen(self.Url + api))
        except urllib.error.URLError as e:
            Notify('\n' + str(e))
            sys.exit()
    def download(self, path):
        url = 'https://raw.githubusercontent.com'
        url += self.Repo + self.Branch + '/' + path
        temp = Path(wget.download(url))
        temp.replace(path)
        return temp
    def latest(self):
        return self.fetch('branches/' + self.Branch)['commit']['sha']
    def diff(self):
        if self.Old == '0':
            self.Old = self.New
            return
        if self.Old == self.New:
            return
        return self.fetch('compare/' + self.Old + '...' + self.New)['files']
    def sync(self):
        Notify( "Verification Started" )    
        if self.Diff:
            for file in self.Diff:
                name = file["filename"]
                path = Path( name )         
                parent = path.parent         
                raw = file["raw_url"]
                status = file["status"]
                parent.mkdir(parents=True, exist_ok=True)

                exclude = [ "dawn.exe" ]
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
                
                print( status, name )
            
        Notify("Verification Complete" )     
        self.Config["commit"] = self.latest()
        sys.exit()
        
def Minecraft(modify=False):
    config = SavedConfig()
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
        git = GitManager()
        git.download('update.py')
        git.download('menu.py')
