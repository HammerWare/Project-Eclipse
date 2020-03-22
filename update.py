import os
import sys
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
    subprocess.check_output("git.exe")
    sys.exit()
        
if not installed:
    subprocess.check_output("git init && git remote add origin " +repo +" && git fetch && git checkout")

os.system("git pull")

import menu
    
