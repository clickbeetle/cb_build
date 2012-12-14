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
args = parser.parse_args()

Root = os.path.abspath(str(args.root))
configRoot = os.path.abspath(str(args.configroot))
profile = str(args.profile) #"default/linux/amd64/10.0"
arch = str(args.arch) #"amd64"
subarch = str(args.subarch) #""

MAKEOPTS = "\"-j8\""


def cleanUp():
  os.system("cd / ; cat /proc/mounts | gawk \'{print $2}\' | grep -i cb_build | sort -r | xargs umount -f ; cd -")

  

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
  
  
  buildpkgs.append("app-portage/eix")
  buildpkgs.append("dev-libs/mpc")
  
  
  
  for b in buildpkgs: print(b)
  




  os.environ["BOOTSTRAP_USE"] = subprocess.check_output(["/usr/bin/portageq","envvar","BOOTSTRAP_USE"])
  os.environ["USE"] = "-* "+ os.environ["BOOTSTRAP_USE"].rstrip().lstrip() + " bindist threads xml ssl openmp"
  
  os.environ["FEATURES"] = "nodoc noman noinfo ccache mini-manifest -collision-protect"
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
  os.system("mount --rbind /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/packages "+ os.path.join(configRoot, "usr/portage/packages"))
  os.system("rm -frv "+ os.path.join(configRoot, "etc/portage/make.profile"))
  os.system("ln -s ../../usr/portage/profiles/"+ profile +" "+ os.path.join(configRoot, "etc/portage/make.profile"))
  
  if(os.path.exists(os.path.join(configRoot, "usr/portage/profiles/arch/"+ arch +"/"+ subarch))):
    make_defaults = os.path.join(configRoot, "usr/portage/profiles/arch/"+ arch +"/"+ subarch +"/make.defaults")
    make_conf = os.path.join(configRoot, "etc/portage/make.conf")
    md = open(make_defaults,"r")
    mc = open(make_conf,"w")
    for xmd in md.readlines():
      if(re.match(r'^\s*$', xmd)):
        continue
      if(xmd.find("#") == 0):
        continue
      if(re.match(r'^ARCH=',xmd)):
        mc.writelines(xmd +"\n")
      if(re.match(r'^ACCEPT_KEYWORDS=',xmd)):
        mc.writelines(xmd +"\n")
      if(re.match(r'^CHOST=',xmd)):
        mc.writelines(xmd +"\n")
      if(re.match(r'^USE=',xmd)):
        mc.writelines(xmd +"\n")
      if(re.match(r'^CFLAGS=',xmd)):
        mc.writelines(xmd +"\n")
      if(re.match(r'^CXXFLAGS=',xmd)):
        mc.writelines(xmd +"\n")
    mc.writelines("MAKEOPTS=\""+ MAKEOPTS +"\"\n\n")
    #mc.writelines("FEATURES=\""+ os.environ["FEATURES"] +"\"")
    mc.close()
  else:
    print("ARCH/SUBARCH DOES NOT EXIST :"+ os.path.join(configRoot, "usr/portage/profiles/arch/"+ arch +"/"+ subarch))
    cleanUp()
    sys.exit(512)
    
  
  
  stage1Cmd1 = "USE=\"$USE build\" emerge --usepkg=y --buildpkg=y --oneshot --noreplace  --quiet-build=y --root="+ Root +" --with-bdeps=n --nodeps --config-root="+ configRoot +" sys-apps/baselayout"
  stage1Cmd2 = "USE=\"$USE build\" emerge --usepkg=y --buildpkg=y --oneshot --quiet-build=y --root="+ Root +" --with-bdeps=n --config-root="+ configRoot +" sys-apps/portage"
  stage1Cmd3 = "USE=\"$USE build\" emerge --usepkg=y --buildpkg=y --oneshot --quiet-build=y --root="+ Root +" --with-bdeps=n --config-root="+ configRoot +" dev-util/ccache"
  stage1Cmd4 = "emerge --deep --usepkg=y --buildpkg=y --quiet-build=y --root="+ Root +" --config-root="+ configRoot +" "+ " ".join(buildpkgs)


  if(os.system(stage1Cmd1) != 0):
    cleanUp()
    sys.exit(1)
  if(os.system(stage1Cmd2) != 0):
    cleanUp()
    sys.exit(2)
  if(os.system(stage1Cmd3) != 0):
    cleanUp()
    sys.exit(3)
  if(os.system(stage1Cmd4) != 0):
    cleanUp()
    sys.exit(4)
    
  os.system("rsync -av "+ os.path.join(configRoot, "etc/portage/") +" "+ os.path.join(Root, "etc/portage/"))
  
  os.system("./makeDevNodes.sh")
  cleanUp()
  
  
  
  
except:
  print(str(sys.exc_info()))
  cleanUp()
  
  
  
