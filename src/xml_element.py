"""Trivial XML Element class"""

class Element(list):
    def __init__(self, name, attrs=None, content=None):
        self.name = name
        self.attrs = attrs
        if content:
            list.__init__(self, content)

    def __str__(self):
        from xml_generator import Generator
        return str(Generator([self]))
