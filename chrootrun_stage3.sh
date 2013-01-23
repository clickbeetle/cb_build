env-update
source /etc/profile
emerge @preserved-rebuild
emerge --update --newuse --deep --usepkg=y --buildpkg=y --quiet-build=y world 

