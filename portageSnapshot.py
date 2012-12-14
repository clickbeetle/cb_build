#!/usr/bin/python
import os
import portage
import sys
import re
import subprocess



os.system("cd /BACKUP/clickbeetleCook.DO_NO_DELETE/cb_build/ ;rm -frv cb_ports ; git clone --depth=1 https://github.com/clickbeetle/cb_ports ; cd cb_ports ; rm -frv ../portage_latest.tar; rm -frv ../portage_latest.tar.xz ; tar -cvphf ../portage_latest.tar ./ ; cd ../; xz -9 portage_latest.tar")
