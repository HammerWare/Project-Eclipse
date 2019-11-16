import os
import sys
import subprocess
import traceback

try:
    import update
    update.GitSync()   
except Exception as e:
    print(traceback.format_exc())
    input( "Please Press Enter To Continue: " )
finally:
    subprocess.Popen([update.Minecraft(),"--workDir","dawn"])
    sys.exit()
    
