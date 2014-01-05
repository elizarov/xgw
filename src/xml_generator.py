"""XML Fragment generator converts XML fragments (lists of elements and strings) to strings"""

import types
from cStringIO import StringIO
from xml_element import Element

class Generator:
    def __init__(self, content=[], raw_text=False):
        self.out = StringIO()
        self.raw_text = raw_text
        for i in content:
            self.append(i)

    def __str__(self):
        return self.out.getvalue()

    def append(self, data):
        # fast path to append primitives
        if isinstance(data, (basestring, int, long, float)):
            s = str(data)
            if not self.raw_text:
                s = xml_quote(s)
            self.out.write(s)
        elif isinstance(data, Element):
            name = data.name
            attrs = data.attrs
            out = self.out
            out.write("<")
            out.write(name)
            if attrs:
                for k, v in attrs.iteritems():
                    out.write(" ")
                    out.write(k)
                    out.write("='")
                    out.write(xml_quote(v).replace("'", "&apos;"))
                    out.write("'")
            if len(data) == 0:
                out.write("/>")
            else:
                out.write(">")   
                for i in data:
                    self.append(i)
                out.write("</")
                out.write(name)
                out.write(">")
        else: 
            # works for all lists, including xml_fragment.Fragment
            for i in data:
                self.append(i)

def xml_quote(s):
    return (s.replace('&', '&amp;')
             .replace('<', '&lt;')
             .replace('>', '&gt;'))
    