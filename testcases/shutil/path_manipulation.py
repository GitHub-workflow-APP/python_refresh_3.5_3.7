import sys
import shutil

shutil.copyfile(sys.argv[1],sys.argv[2]) # CWEID 73
shutil.copy(sys.argv[1],sys.argv[2]) # CWEID 73
shutil.copy2(sys.argv[1],sys.argv[2]) # CWEID 73

shutil.chown(sys.argv[1],user='root',group=None) # CWEID 73
