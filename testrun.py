from parser import Parser

p = Parser(open('comm.rst', 'r').read())
print p.parse().get_json()
