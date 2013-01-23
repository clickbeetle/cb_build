#!/usr/bin/python
import os
import subprocess
import sys

uuid = subprocess.check_output("uuidgen").rstrip().lstrip()
print uuid
os.system("echo \""+ str(uuid) +"\" > /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/lastUUID")
if(os.system("/home/shrinidhi/bin/gitHub/cb_build/portageSnapshot.py "+ str(uuid)) != 0):
  sys.exit(1)
if(os.system("mkdir -p /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid)) != 0):
  print("making build dir failed : /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid))
os.system("/home/shrinidhi/bin/gitHub/cb_build/stage1.py --root=/BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid) +" --configroot=/home/shrinidhi/bin/gitHub/cb_build/configRoot/ --profile=default/linux/amd64/10.0 --arch=amd64 --subarch=\"\" --keywords=~amd64")
os.system("/home/shrinidhi/bin/gitHub/cb_build/stage2.py --root=/BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid))
os.system("/home/shrinidhi/bin/gitHub/cb_build/stage3.py --root=/BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid) +" --pkgs app-portage/gentoolkit,sys-apps/gptfdisk")
print uuid