#!/usr/bin/python
#!/usr/bin/python
import portage,sys
pkgdict={}
alloweduse=["nls", "bindist", "nptl", "nptlonly", "multilib", "userlocales" ]
alloweduse_startswith = ["userland_"]

use=portage.settings["USE"].split()

myuse=portage.settings["BOOTSTRAP_USE"].split()

for x in use:
        if x in alloweduse:
                myuse.append(x)
        for y in alloweduse_startswith:
                if x.startswith(y):
                        myuse.append(x)
                        break

for dep in portage.settings.packages:
        if dep[0] == "*":
                dep = dep[1:]
        catpkg=portage.dep_getcpv(dep)
        split=portage.catpkgsplit(catpkg)
        if split != None:
                pkgdict[split[1]]=dep
        else:
                pkgdict[catpkg.split("/")[1]]=dep

pkglist = ["texinfo", "gettext", "binutils", "gcc", "glibc", "baselayout", "zlib", "shadow" ]

#, "perl", "python", "libtool" ]

# perl needs an interim remerge so it references the new CHOST in Config.pm, although this has been fixed in funtoo.
# python needs  a remerge so it references the new CHOST in its installed Makefile in /usr/lib/pythonx.y.
# libtool refernces the old CHOST so it seems like a good idea to remerge as well. This is all good stuff
# when we are using a non-native stage1. Not necessary when using a native stage1.

if "nls" not in use or "gettext" not in pkgdict.keys():
        pkglist.remove("gettext")

if not "linux-headers" in pkgdict:
        pkgdict["linux-headers"]="virtual/os-headers"
if sys.argv[1] == "--check":
        if "build" in use or "bootstrap" in use:
                print("Error: please do not specify \"build\" or \"bootstrap\" in USE. Exiting.")
                sys.exit(1)
        else:
                sys.exit(0)
elif sys.argv[1] == "--use":
        # TESTING NLS... not for production
        print("nls "+" ".join(myuse))
        sys.exit(0)
elif sys.argv[1] == "--pkglist":
        for x in pkglist:
                if x in pkgdict:
                        sys.stdout.write(pkgdict[x]+" ")
        sys.stdout.write("\n")
        sys.exit(0)
else:
        print(sys.argv[0]+": invalid arguments: "+" ".join(sys.argv[1:]))
        sys.exit(1)
