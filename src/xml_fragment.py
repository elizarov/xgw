"""XML Fragment class"""

class Fragment(list):
    def __init__(self, content=None, raw_text=False):
        if content:
            list.__init__(self, content)
        self.raw_text = raw_text
    
    def __str__(self):
        from xml_generator import Generator
        return str(Generator(self, raw_text=self.raw_text))

    def __int__(self):
        return int(self.__str__())
   