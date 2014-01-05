"""Tests for XML modules"""

from xml_generator import Generator
from xml_element import Element
from xml_parser import Parser

print Generator([Element("test", dict(a='1', b='2'), [12345])])
assert "<test a='1' b='2'>12345</test>" == str(Generator([Element("test", dict(a='1', b='2'), [12345])]))

print Parser("<send dest='FIO1'>!RR\\r\\n</send><recv src='FIO1' wait='1'/>").fragment
assert "<send dest='FIO1'>!RR\\r\\n</send><recv src='FIO1' wait='1'/>" == str(Parser("<send dest='FIO1'>!RR\\r\\n</send><recv src='FIO1' wait='1'/>").fragment)

print Parser("<send dest='FIO1'>!RR\\r\\n</send>   <recv src='FIO1' wait='1'/>").fragment
for a in Parser("<send dest='FIO1'>!RR\\r\\n</send>   <recv src='FIO1' wait='1'/>").fragment:
    print a.__class__, len(a), str(a)
    