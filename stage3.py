#!/usr/bin/python
import os
import portage
import sys
import re
import subprocess
import argparse
import glob

build_uuid = os.environ['build_uuid']

parser = argparse.ArgumentParser(description='build stage1',fromfile_prefix_chars='@')
if(len(sys.argv) == 1):
  parser.print_help()
  sys.exit(1)
  
  
parser.add_argument("-r","--root",dest='root',help='root dir to use from stage2')
parser.add_argument("-p","--pkgs",dest='pkgs',help='comma seperated list of full pkg names to install in stage3')

args = parser.parse_args()

Root = os.path.abspath(str(args.root))



# --config-root
#configRoot = sys.argv[1]

# --root

Pkgs = 0
try:
  Pkgs = str(args.pkgs)
except:
  print("pkgs list not given")

if(Pkgs):
  pkg_list = " ".join(Pkgs.split(","))
  os.system("cp -v chrootrun_stage3.sh /tmp/")
  os.system("echo \"emerge --deep --usepkg=y --buildpkg=y --quiet-build=y "+ str(pkg_list) +"\" >> /tmp/chrootrun_stage3.sh")
    

def cleanUp():
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd /;cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")

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
  os.system("mount --rbind /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ build_uuid +"/packages "+ os.path.join(Root, "usr/portage/packages"))
  #os.system("rm -frv "+ os.path.join(Root, "etc/portage/make.profile"))
  #os.system("ln -s ../../usr/portage/profiles/"+ profile +" "+ os.path.join(Root, "etc/portage/make.profile"))
  
  #os.system("cp -v bootstrap.py "+ Root)
  os.system("cp -v /tmp/chrootrun_stage3.sh "+ os.path.join(Root, "tmp/"))
  #os.system("cp -v chrootrun_stage2.sh /tmp/")
  os.system("chroot "+ Root +" /tmp/chrootrun_stage3.sh")
  cleanUp()
except SystemExit, e:
  sys.exit(e)
except:
  print(str(sys.exc_info()))
  cleanUp()
  
  
  
