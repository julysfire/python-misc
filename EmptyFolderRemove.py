import os
import sys

def removeEmpty(main_dir):
    counter = 0
    
    for dirpath, dirnames, filenames in os.walk(main_dir):
        if not dirnames and not filenames:
            os.rmdir(dirpath)
            counter += 1
    
    print(str(counter) + " empty folders removed.")

if __name__ == '__main__':
    removeEmpty(sys.argv[1])
