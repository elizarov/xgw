"""Parser for xml-based command streams"""

from xml.parsers.expat import ParserCreate

class Parser:
    def __init__(self, controller):
        self._controller = controller
        self._methods = vars(controller.__class__) 
        
    def start_element(self, name, attrs):
        self._level += 1
        self._stack.append((attrs, ""))
    
    def end_element(self, name):
        self._level -= 1
        attrs, content = self._stack.pop()
        if self._level == 1:
            # str here to get rid of unicode
            self.invoke(
                str(name), 
                dict([(str(k), str(v)) for (k, v) in attrs.items()]),                                
                str(content))
            
    def invoke(self, name, attrs, content):
        print "xgw: Invoking %s %s %s" % (name, attrs, repr(content))
        result = ""
        error = ""
        if name in self._methods:
            m = self._methods[name]
            try:
                if content: 
                    result = m(self._controller, content, **attrs)
                else:
                    result = m(self._controller, **attrs)
            except Exception, e:
                error = str(e)
        else:
            error = "Method is not found" 
        ats = ""
        for (k, v) in attrs.items():
            ats += " " + k + "=" + repr(v)
        if error:
            result = "<error for='%s'%s>%s</error>" % (name, ats, error)
        else:
            result = "<result for='%s'%s>%s</result>" % (name, ats, result)
        print "xgw: Outcome " + repr(result)
        self._result.append(result); 
        
    def character_data(self, data):
        attrs, content = self._stack.pop()
        self._stack.append((attrs, content + data))
        
    def parse(self, commands):
        print "xgw: Parsing commands"
        self._level = 0
        self._stack = []
        self._result = []
        p = ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.character_data
        p.Parse("<c>" + commands + "</c>")
        return "\n".join(self._result)
             