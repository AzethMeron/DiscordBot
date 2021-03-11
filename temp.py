
import os
import os.path
import shutil

# by Jakub Grzana

tempdir = ".tmp"

def GetTempDirPath():
    if not os.path.isdir(tempdir):
        os.mkdir(tempdir)
    return tempdir + '/'

def PurgeTempDir():
    if os.path.isdir(tempdir):
        shutil.rmtree(tempdir)