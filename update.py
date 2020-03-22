import os
import sys
import json
sys.path.append(os.getcwd())

import shutil
import subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

repo = "https://github.com/TheMerkyShadow/Project-Dawn"
git = shutil.which("git")
installed = os.path.isdir(".git")

if git is None:
    os.popen("git.exe")
    sys.exit()
    
if not installed:
    os.popen("git init && git remote add origin " +repo )
    sys.exit()

os.popen("git pull origin master").read()

import menu
    
