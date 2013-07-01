#!/usr/bin/python
import os
import portage
import sys
import re
import subprocess
import argparse
import glob



parser = argparse.ArgumentParser(description='build stage1',fromfile_prefix_chars='@')
if(len(sys.argv) == 1):
  parser.print_help()
  sys.exit(1)
  
  
parser.add_argument("-r","--root",dest='root',help='root dir to install stage1')
parser.add_argument("-c","--configroot",dest='configroot',help='configroot dir for stage1')
parser.add_argument("-p","--profile",dest='profile',help='select the profile to use for the build')
parser.add_argument("-a","--arch",dest='arch',help='select the Arch for the build')
parser.add_argument("-s","--subarch",dest='subarch',help='select the sub Arch for the build')
parser.add_argument("-k","--keywords",dest='keywords',help='set the ACCEPT_KEYWORDS flag')
args = parser.parse_args()

Root = os.path.abspath(str(args.root))
configRoot = os.path.abspath(str(args.configroot))
profile = str(args.profile) #"default/linux/amd64/10.0"
arch = str(args.arch) #"amd64"
subarch = str(args.subarch) #""
accept_keywords = str(args.keywords)# ~amd64
build_uuid = os.environ['build_uuid']
MAKEOPTS = "\"-j12\""


def cleanUp():
  os.system("cd / ; cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd / ; cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd / ; cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd / ; cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd / ; cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  os.system("cd / ; cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f >& /dev/null ; cd -")
  

def scan_profile(file):
  return portage.stack_lists( [portage.grabfile_package(os.path.join(x, file)) for x in portage.settings.profiles], incremental=1);

# loaded the stacked packages / packages.build files
pkgs = scan_profile("packages")
buildpkgs = scan_profile("packages.build")


# go through the packages list and strip off all the
# crap to get just the <category>/<package> ... then
# search the buildpkg list for it ... if it's found,
# we replace the buildpkg item with the one in the
# system profile (it may have <,>,=,etc... operators
# and version numbers)

try:
  for idx in range(0, len(pkgs)):
    try:
      bidx = buildpkgs.index(portage.dep.Atom.getkey(pkgs[idx]))
      buildpkgs[bidx] = pkgs[idx]
      if buildpkgs[bidx][0:1] == "*":
        buildpkgs[bidx] = buildpkgs[bidx][1:]
    except: pass
  
  
  
  
  
  
  for b in buildpkgs: print(b)
  




  os.environ["BOOTSTRAP_USE"] = subprocess.check_output(["/usr/bin/portageq","envvar","BOOTSTRAP_USE"])
  os.environ["USE"] = os.environ["BOOTSTRAP_USE"].rstrip().lstrip() + " threads python xml xattr tcl tk gudev kmod udev"
  
  os.environ["FEATURES"] = "nodoc noman noinfo"
  os.environ["ROOT"] = Root
  os.environ["CONFIG_ROOT"] = configRoot
  
  os.system("mkdir -p "+ os.path.join(configRoot, "proc"))
  os.system("mkdir -p "+ os.path.join(configRoot, "dev"))
  os.system("mkdir -p "+ os.path.join(configRoot, "usr/portage"))
  
  os.system("mount -t proc none "+ os.path.join(configRoot, "proc"))
  os.system("mount --rbind /dev "+ os.path.join(configRoot, "dev"))
  os.system("mount --rbind /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/cb_ports "+ os.path.join(configRoot, "usr/portage"))
  os.system("mkdir -p "+ os.path.join(configRoot, "usr/portage/distfiles"))
  os.system("mkdir -p "+ os.path.join(configRoot, "usr/portage/packages"))
  os.system("mount --rbind /BACKUP/clickbeetleDistfiles.DO_NO_DELETE/distfiles "+ os.path.join(configRoot, "usr/portage/distfiles"))
  os.system("mkdir -p /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ build_uuid +"/packages")
  os.system("mount --rbind /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/"+ build_uuid +"/packages "+ os.path.join(configRoot, "usr/portage/packages"))
  os.system("rm -frv "+ os.path.join(configRoot, "etc/portage/make.profile"))
  os.system("ln -s ../../usr/portage/profiles/"+ profile +" "+ os.path.join(configRoot, "etc/portage/make.profile"))
  
  make_conf = os.path.join(configRoot, "etc/portage/make.conf")
  package_keywords = os.path.join(configRoot, "etc/portage/package.keywords/")
  os.system("cp -av "+ os.path.join(configRoot, "usr/portage/profiles/default/linux/make.defaults.build") +" "+ make_conf)
  os.system("rsync -av "+ os.path.join(configRoot, "usr/portage/profiles/default/linux/package.keywords/") +" "+ package_keywords)
  
  stage1Cmd1 = "USE=\"-* "+ os.environ['USE'] +" build\" emerge --deep --usepkg=y --buildpkg=y --oneshot --noreplace  --quiet-build=y --root="+ Root +" --with-bdeps=y --config-root="+ configRoot +" sys-apps/baselayout dev-lang/python:2.7 dev-lang/python:3.2 dev-lang/python:3.3"
  stage1Cmd2 = "USE=\"-* "+ os.environ['USE'] +" build\" emerge --usepkg=y --buildpkg=y --oneshot --quiet-build=y --root="+ Root +" --with-bdeps=y --config-root="+ configRoot +" sys-apps/portage"
  stage1Cmd3 = "USE=\"-* "+ os.environ['USE'] +" build\" emerge --usepkg=y --buildpkg=y --oneshot --quiet-build=y --root="+ Root +" --with-bdeps=n --config-root="+ configRoot +" dev-util/ccache"
  stage1Cmd4 = "USE=\"-* "+ os.environ['USE'] +" build\" emerge --deep --usepkg=y --buildpkg=y --with-bdeps=y --quiet-build=y --root="+ Root +" --config-root="+ configRoot +" "+ " ".join(buildpkgs)

  print("running : "+ stage1Cmd1)
  if(os.system(stage1Cmd1) != 0):
    cleanUp()
    sys.exit(1)
  print("running : "+ stage1Cmd2)
  if(os.system(stage1Cmd2) != 0):
    cleanUp()
    sys.exit(2)
  print("running : "+ stage1Cmd3)
  if(os.system(stage1Cmd3) != 0):
    cleanUp()
    sys.exit(3)
  print("running : "+ stage1Cmd4)
  if(os.system(stage1Cmd4) != 0):
    cleanUp()
    sys.exit(4)
    
  os.system("rsync -av "+ os.path.join(configRoot, "etc/portage/") +" "+ os.path.join(Root, "etc/portage/"))
  
  os.system("./makeDevNodes.sh")
  cleanUp()
  sys.exit(0)
  
  
  
  
except SystemExit, e:
  sys.exit(e)
except:
  err = str(sys.exc_info())
  cleanUp()
  sys.exit(5)
  
  
  
