import os
import sys
import subprocess
import traceback

import extra

try:
    import update
    update.GitSync()
except Exception as e:
    input(traceback.format_exc())
finally:
    subprocess.Popen([update.Minecraft(),"--workDir","dawn"])
    sys.exit()
    
