import hashlib
import os
import sys

def cleanup(main_dir):
    hashList = []
    fileList = []

    keepHash = []
    keepFile = []

    totalSizeSaved = 0

    #Get all files and their hashes
    for subdir, dirs, files in os.walk(main_dir):
        if files:
            for i in files:
                with open(subdir+"\\"+i, 'rb') as f:
                    data = f.read()
                    if not data:
                        break
                    md5 = hashlib.md5()
                    md5.update(data)
                    hashList.append(md5.hexdigest())
                    fileList.append(subdir+"\\"+i)
        print(subdir)
    dupes = set([x for x in hashList if hashList.count(x) > 1])

    #Get list of items to keep
    for i in range(len(hashList)):
        if hashList[i] not in keepHash:
            keepHash.append(hashList[i])
            keepFile.append(fileList[i])

    #Delete files that aren't in the keep list
    for i in fileList:
        if i not in keepFile:
            #Delete
            totalSizeSaved = totalSizeSaved + os.path.getsize(i)
            os.remove(i)
    print()
    print(str(totalSizeSaved*0.000001))

if __name__ == '__main__':
    cleanup(sys.argv[1])
