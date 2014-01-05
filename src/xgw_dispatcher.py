"""Parser for xml-based command streams"""

from xml_parser import Parser
from xml_generator import Generator
from xml_element import Element

class Dispatcher:
    def __init__(self, controller):
        self._controller = controller
        self._methods = vars(controller.__class__) 
        
    def _invoke(self, cmd):
        error = ""
        result = ""
        cmd_attrs = {}
        # convert unicode to regular strings
        for (k, v) in cmd.attrs.iteritems():
            cmd_attrs[str(k)] = str(v) 
        # find and invoke method
        if cmd.name in self._methods:
            m = self._methods[cmd.name]
            try:
                if len(cmd) > 0: 
                    result = m(self._controller, str(Generator(cmd)), **cmd_attrs)
                else:
                    result = m(self._controller, **cmd_attrs)
            except Exception, e:
                error = str(e)
        else:
            error = "Method is not found"
        # prepare attrs for result/error
        result_attrs = dict(cmd.attrs)
        result_attrs["for"] = cmd.name 
        # return result/error
        if error:
            return Element("error", result_attrs, error)
        else:
            return Element("result", result_attrs, result)
        
    def callback(self, commands):
        print "xgw: Dispatching commands"
        result = ["\n"]
        for cmd in Parser(commands).fragment:
            if isinstance(cmd, Element):
                print "xgw: Invoking ", cmd
                cmd_res = self._invoke(cmd)
                print "xgw: Outcome ", cmd_res.name # print error or result
                result.append(cmd_res)
                result.append("\n")
        return str(Generator(result))
             