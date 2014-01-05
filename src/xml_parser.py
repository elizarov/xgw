"""XML Fragment parser converts string to XML fragments -- lists of strings and Elements"""

from xml.parsers.expat import ParserCreate
from xml_element import Element
from xml_fragment import Fragment

class Parser:
    def __init__(self, data=None):
        self.parser = ParserCreate()
        self.parser.Parse("<d>", 0) # dummy document element
        self.parser.StartElementHandler = self._start_element
        self.parser.EndElementHandler = self._end_element
        self.parser.CharacterDataHandler = self._character_data
        self.fragment = Fragment()
        self._stack = []
        if data:
            self.parser.Parse(data, 0)
        
    def parse(self, data):
        self.parser.Parse(data, 0)
        
    def _start_element(self, name, attrs):
        self._stack.append(self.fragment)
        self.fragment = Element(name, attrs)
    
    def _end_element(self, name):
        element = self.fragment
        self.fragment = self._stack.pop()
        self.fragment.append(element)
    
    def _character_data(self, data):
        self.fragment.append(data)
    