import os
import sys
import subprocess
import traceback

import extra
import update

try:
    update.GitSync()
except Exception as e:
    input(traceback.format_exc())
finally:
    subprocess.Popen([update.Minecraft(),"--workDir","dawn"])
    sys.exit()
    
