import os
import json
import os.path
import string
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SPEC_FILE_PATH = os.path.join(os.path.sep, BASE, "mhn_spec.json")

new_spec = {}
with open(SPEC_FILE_PATH) as data_file:
     new_spec=json.load(data_file)

os.system('ifconfig eth1 ' + new_spec['honeypotIp'] + ' netmask 255.255.255.0 up')


