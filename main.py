import os
import sys
import subprocess
import traceback

import update
from playsound import playsound

try:
    update.GitSync()
    playsound('startup.mp3')    
except Exception as e:
    print(traceback.format_exc())
    input( "Please Press Enter To Continue: " )
    pass
finally:
    subprocess.Popen([update.Minecraft(),"--workDir","dawn"])
    sys.exit()
    
