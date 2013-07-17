import json
import os.path
import sys

from parser import Parser


media = os.path.join(os.path.dirname(__file__), '..', 'hearth', 'media')

if len(sys.argv) < 2:
    raise Exception('A directory name is required.')

output = []

for root, _, files in os.walk(sys.argv[1]):
    for f in files:
        if not f.endswith('.rst'):
            continue

        print 'parsing %s...' % f
        fd = open(os.path.join(root, f), 'r')
        parser = Parser(fd.read())
        parser.parse()
        output.append({'api_name': f[:-4], 'endpoints': parser.get_array()})

with open(os.path.join(media, 'out.json'), 'w') as fd:
    fd.write(json.dumps({'api_list': output}))
