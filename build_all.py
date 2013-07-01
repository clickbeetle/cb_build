#!/usr/bin/python
import os
import subprocess
import sys

uuid = subprocess.check_output("uuidgen").rstrip().lstrip()
try:
  uuid = sys.argv[1]
except:
  print("no system argv given")
  
os.environ['build_uuid'] = uuid
print(uuid)
os.system("echo \""+ str(uuid) +"\" > /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/lastUUID")
#if(os.system("/home/shrinidhi/bin/gitHub/cb_build/portageSnapshot.py "+ str(uuid)) != 0):
  #sys.exit(1)
if(os.system("mkdir -p /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid)) != 0):
  print("making build dir failed : /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid))


stat1 = os.system("/home/shrinidhi/bin/gitHub/cb_build/stage1.py --root=/BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid) +"/amd64/" +" --configroot=/home/shrinidhi/bin/gitHub/cb_build/configRoot/ --profile=default/linux/amd64/10.0 --arch=amd64 --subarch=\"\" --keywords=~amd64")
if(stat1 != 0):
  print("failed stage 1")
  print(uuid)
  sys.exit(1)
  

print("STAGE 1 done")

stat2 = os.system("/home/shrinidhi/bin/gitHub/cb_build/stage2.py --root=/BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid) +"/amd64/")
if(stat2 != 0):
  print("failed stage 2")
  print(uuid)
  sys.exit(2)
  

print("STAGE 2 done")
stat3 = os.system("/home/shrinidhi/bin/gitHub/cb_build/stage3.py --root=/BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid) +"/amd64/" +" --pkgs app-portage/gentoolkit,sys-apps/gptfdisk,app-portage/eix,app-admin/sudo,sys-process/time,net-misc/bridge-utils,sys-apps/usermode-utilities,net-misc/keychain")
if(stat3 != 0):
  print("failed stage 3")
  print(uuid)
  sys.exit(3)
  

print("STAGE 3 done :/BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ str(uuid) +"/amd64/")
