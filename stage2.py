#!/usr/bin/python
import os
import portage
import sys
import re
import subprocess
import argparse
import glob



parser = argparse.ArgumentParser(description='build stage2',fromfile_prefix_chars='@')
if(len(sys.argv) == 1):
  parser.print_help()
  sys.exit(1)
  
  
parser.add_argument("-r","--root",dest='root',help='root dir to use from stage1')
args = parser.parse_args()

Root = os.path.abspath(str(args.root))

def cleanUp():
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f ; cd -")

cleanUp()
 
  # stage 2 
  
try:  
  os.system("mount -t proc none "+ os.path.join(Root, "proc"))
  os.system("mount --rbind /dev "+ os.path.join(Root, "dev"))
  os.system("mkdir -p "+ os.path.join(Root, "usr/portage"))
  os.system("mount --rbind /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/cb_ports "+ os.path.join(Root, "usr/portage"))
  os.system("mkdir -p "+ os.path.join(Root, "usr/portage/distfiles"))
  os.system("mkdir -p "+ os.path.join(Root, "usr/portage/packages"))
  os.system("mount --rbind /BACKUP/clickbeetleDistfiles.DO_NO_DELETE/distfiles "+ os.path.join(Root, "usr/portage/distfiles"))
  os.system("mount --rbind /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/packages "+ os.path.join(Root, "usr/portage/packages"))
  #os.system("rm -frv "+ os.path.join(Root, "etc/portage/make.profile"))
  #os.system("ln -s ../../usr/portage/profiles/"+ profile +" "+ os.path.join(Root, "etc/portage/make.profile"))
  os.system("cp -v /etc/resolv.conf "+ os.path.join(Root, "etc/"))
  os.system("cp -v bootstrap.py "+ os.path.join(Root, "tmp/"))
  os.system("cp -v chrootrun_stage2.sh "+ os.path.join(Root, "tmp/"))
  os.system("chroot "+ Root +" /tmp/chrootrun_stage2.sh")
  cleanUp()
  sys.exit(0)
except:
  print(str(sys.exc_info()))
  cleanUp()
  sys.exit(1)
  
  
  
