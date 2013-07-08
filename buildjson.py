import os.path
import sys
import json

from parser import Parser


if len(sys.argv) < 2:
    raise Exception('A directory name is required.')

output = {}

for root, _, files in os.walk(sys.argv[1]):
    for f in files:
        if not f.endswith('.rst'):
            continue

        print 'parsing %s...' % f
        fd = open(os.path.join(root, f), 'r')
        parser = Parser(fd.read())
        parser.parse()
        output[f[:-4]] = parser.get_array()

with open('out.json', 'w') as fd:
    fd.write(json.dumps(output))
