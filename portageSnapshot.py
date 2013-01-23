#!/usr/bin/python
import os
import portage
import sys
import re
import subprocess
uuid = sys.argv[1]


if(os.system("cd /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/ ;rm -frv cb_ports ; git clone --depth=1 https://github.com/clickbeetle/cb_ports ; cd cb_ports ; rm -frv ../portage_latest.tar; rm -frv ../portage-"+ str(uuid) +".tar.xz ; tar -cvphf ../portage-"+ str(uuid) +".tar ./ ; cd ../; xz -9 portage-"+ str(uuid) +".tar") == 0):
  print("portage snapshot succesful")
  sys.exit(0)
else:
  print("portage snapshot failed")
  sys.exit(1)
  
