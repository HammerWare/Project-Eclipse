import os
import sys
sys.path.append(os.getcwd())

if __name__ == '__main__':
    try:
        import update
    except Exception as e:
        print(traceback.format_exc())
