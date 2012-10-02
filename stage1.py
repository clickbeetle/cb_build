#!/usr/bin/python
import os
import portage
import sys
import re

# --config-root
configRoot = sys.argv[1]

# --root
Root = sys.argv[2]

# 
profile = default/linux/amd64/10.0

arch = amd64

subarch = ""
# this loads files from the profiles ...
# wrap it here to take care of the different
# ways portage handles stacked profiles

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

for idx in range(0, len(pkgs)):
  try:
    bidx = buildpkgs.index(portage.dep.Atom.getkey(pkgs[idx]))
    buildpkgs[bidx] = pkgs[idx]
    if buildpkgs[bidx][0:1] == "*":
      buildpkgs[bidx] = buildpkgs[bidx][1:]
  except: pass

for b in buildpkgs: print(b)





#export BOOTSTRAP_USE="$(portageq envvar BOOTSTRAP_USE)"
os.environ["BOOTSTRAP_USE"] = subprocess.check_output(["/usr/bin/portageq","envvar","BOOTSTRAP_USE"])
#export USE="-* bindist build xml ${BOOTSTRAP_USE} ssl threads"
os.environ["USE"] = "-* bindist build ${BOOTSTRAP_USE} threads"
#export FEATURES="$FEATURES nodoc noman noinfo ccache mini-manifest"
os.environ["FEATURES"] = "$FEATURES nodoc noman noinfo ccache mini-manifest"

os.system("mkdir -p "+ os.path.join(configRoot, "proc"))
os.system("mkdir -p "+ os.path.join(configRoot, "dev"))
os.system("mkdir -p "+ os.path.join(configRoot, "usr/portage"))

os.system("mount -t proc none "+ os.path.join(configRoot, "proc"))
os.system("mount --rbind /dev "+ os.path.join(configRoot, "dev"))
os.system("mount --rbind /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports "+ os.path.join(configRoot, "usr/portage"))
os.system("mount --rbind /BACKUP/clickbeetleDistfiles.DO_NO_DELETE/distfiles "+ os.path.join(configRoot, "usr/portage/distfiles"))
os.system("rm -frv "+ os.path.join(configRoot, "etc/portage/make.profile"))

if(os.path.exists(os.path.join(configRoot,"usr/portage/profile/"+ profile))):
  os.system("ln -s ../../usr/portage/profile/"+ profile +" "+ os.path.join(configRoot, "etc/portage/make.profile"))
else:
  print("PROFILE DOES NOT EXIST")
  cleanUp()
  sys.exit(512)

if(os.path.exists(os.path.join(configRoot, "usr/portage/profile/arch/"+ arch +"/"+ subarch))):
  make_defaults = os.path.join(configRoot, "usr/portage/profile/arch/"+ arch +"/"+ subarch +"/make.default")
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
else:
  print("ARCH/SUBARCH DOES NOT EXIST")
  cleanUp()
  sys.exit(512)
   
  
  
stage1Cmd1 = "emerge --usepkg=y --buildpkg=y --oneshot --noreplace  --quiet-build=y --root="+ Root +" --with-bdeps=n --nodeps --config-root="+ configRoot +" sys-apps/baselayout"
stage1Cmd2 = "emerge --usepkg=y --buildpkg=y --oneshot --quiet-build=y --root="+ Root +" --with-bdeps=n --config-root="+ configRoot +" sys-apps/portage"
stage1Cmd3 = "emerge --usepkg=y --buildpkg=y --oneshot --quiet-build=y --root="+ Root +" --with-bdeps=n --config-root="+ configRoot +" dev-util/ccache"
stage1Cmd4 = "emerge --usepkg=y --buildpkg=y --quiet-build=y --root="+ Root +" --config-root="+ configRoot +" "+ " ".join(buildpkgs)


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


def cleanUp():
  os.system("cat /proc/mounts | gawk '{print $2}' | grep -i "+ configRoot +" | sort -r | xargs umount -f ")
  os.system("cat /proc/mounts | gawk '{print $2}' | grep -i "+ Root +" | sort -r | xargs umount -f ")