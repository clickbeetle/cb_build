#!/bin/bash
export AUTOCLEAN="yes"
export CONFIG_PROTECT="-*"
export FEATURES="$FEATURES -collision-protect"
cat /proc/mounts | grep -iv rootfs > /etc/mtab
#cp -av bootstrap.py /tmp/bootstrap.py
python /tmp/bootstrap.py --check || exit 1
env-update && source /etc/profile



# USE="-* build bootstrap" emerge portage || exit 1
# 
# export USE="-* bootstrap `python /tmp/bootstrap.py --use`"
# # adding oneshot below so "libtool" doesn't get added to the world file... 
# # libtool should be in the system profile, but is not currently there it seems.
# echo "mark 1"
# emerge --oneshot `python /tmp/bootstrap.py --pkglist` || exit 1
# echo "mark 2"
# emerge --clean 
# emerge --prune sys-devel/gcc || exit 1
# 
# # Currently, a minimal, barely functional Python is installed. Upgrade to
# # a full-featured Python installation to avoid problems during the stage3
# # build:
# 
# unset USE

for atom in `portageq match / dev-lang/python`
do
        echo "emerging python $atom"
        emerge --usepkg=y --buildpkg=y --with-bdeps=y --quiet-build=y --deep --oneshot =$atom 
        emerge --usepkg=y --buildpkg=y --with-bdeps=y --quiet-build=y --deep --oneshot =$atom --resume
        emerge --usepkg=y --buildpkg=y --with-bdeps=y --quiet-build=y --deep --oneshot =$atom --resume|| exit 1
done


gcc-config $(gcc-config --get-current-profile)
eselect python set python2.7 
# now, we need to do some house-cleaning... we may have just changed
# CHOSTS, which means we have some cruft lying around that needs cleaning
# up...

for prof in /etc/env.d/05gcc*
do
        TESTPATH=$(unset PATH; source $prof; echo $PATH)
        if [ ! -e $TESTPATH ]
        then
                echo 
                echo ">>>"
                echo ">>> Found old CHOST stuff... cleaning up..."
                echo ">>>"
                # this is an old gcc profile, so we'll do some cleaning:
                TESTCHOST=`basename $prof`
                TESTCHOST="${TESTCHOST/05gcc-/}"
                # ok, now TESTCHOST refers to our bogus CHOST, so we can do this:
                # remove bogus /usr/bin entries:
                rm -f /usr/bin/$TESTCHOST*
                rm -rf /usr/$TESTCHOST
                rm -f $prof
                rm -rf /etc/env.d/gcc/config-$TESTCHOST
        fi
done
# remove any remaining cruft in cached files...
env-update
