import os
import sys
import logging
import json
sys.path.append(os.getcwd())

from pathlib import Path
from urllib.request import urlopen

from tkinter import *
from tkinter import filedialog

from pypresence import *
from pypresence import Presence

import main
