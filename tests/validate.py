import sys,json
from openc2 import parse

#read in json file and attempt to parse

with open(sys.argv[1], 'r') as IN:
    msg = json.load(IN)

cmd = parse(msg)
print(cmd)
