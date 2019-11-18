import os
import sys
import json
import wget
import time

from urllib.request import urlopen
from pathlib import Path

import logging

logging.basicConfig(filename='log.txt', format='%(asctime)s %(message)s', filemode='a+')
logs = logging.getLogger()
logs.setLevel(logging.NOTSET)

class JsonConfig:
    def __init__(self, dir='config.json'):
        self.Path = Path(dir)
        self.Table = self.Decode()
    def Decode(self):
        return json.loads(self.Path.read_text())
    def Encode(self):
        return json.dumps((self.Table), indent=4)
    def __getitem__(self, item):
        return self.Table[item]
    def __setitem__(self, item, value):
        self.Table[item] = value
        self.Save()
    def Reload(self):
        self.Table = self.Decode()
    def Save(self):
        self.Path.write_text(self.Encode())

class Git:
    def __init__(self, CONFIG):
        self.Repo = CONFIG['repo']
        self.Url = 'https://api.github.com/repos' + self.Repo
        self.Old = CONFIG['commit']
        self.New = self.latest()
        self.Verify()
    def Verify(self):
        if self.Old == '':
            self.Old = self.New
    def fetch(self, api):
        return json.load(urlopen(self.Url + api))
    def latest(self):
        return self.fetch('branches/master')['commit']['sha']
    def diff(self):
        return self.fetch('compare/' + self.Old + '...' + self.New)['files']

CONFIG = JsonConfig()
GIT = Git(CONFIG)

def GitSync():
    logs.info('Verification Starting')
    diff = GIT.diff()
    if diff:
        exclude = CONFIG['exclude']
        for file in diff:
            name = file['filename']
            path = Path(name)
            parent = path.parent
            raw = file['raw_url']
            status = file['status']
            if name in exclude:
                continue
            parent.mkdir(parents=True, exist_ok=True)
            if status == 'added' or status == 'modified':
                temp = Path(wget.download(raw))
                temp.replace(path)
            elif status == 'renamed':
                previous = Path(file['previous_filename'])
                if previous.is_file():
                    previous.replace(path)
                elif status == 'removed':
                    if path.is_file():
                        path.unlink()
            if parent.is_dir():
                empty = list(os.scandir(parent)) == 0
                if empty:
                    parent.rmdir()
                    
            logs.info( status +", " +name )

    if diff:
        logs.info( GIT.Old +" to " +GIT.New )
        
    logs.info('Verification Complete!')    
    CONFIG['commit'] = GIT.New
