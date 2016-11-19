
from collections import deque
from xml_element import Element
from time import time
from time_util import fmt_time

TAG_PREFIX = "D"

STATE_OUT              = 0
STATE_MAIN_TAG         = 1
STATE_VALUE_OR_TAG_0   = 2
STATE_VALUE_OR_TAG     = 3
STATE_VALUE_LEAD_SPACE = 4
STATE_TAG_OVER         = 5
STATE_VALUE_0          = 6
STATE_VALUE            = 7
STATE_VALUE_FRAC       = 8
STATE_0D               = 9

class Current:
    def __init__(self):
        self.data = {}
        self.messages = deque()
        self.urgent = False
        self.urgent_data = {}
        self._next_message_index = 1
        
    def next_message_index(self):
        result = self._next_message_index
        self._next_message_index += 1
        return result
            
CURRENT = Current()

MAX_MESSAGES = 30
PARSER = None

def updateDataLine(node, data, time=time()):
    global PARSER
    if not PARSER:
        PARSER = Parser()
    PARSER.parse(node, data, time)
    
def updateDataItems(node, items, time=time()):
    for (k, v) in items.iteritems():
        tag = node + k
        CURRENT.data[tag] = Data(tag, v, time, node) 

def isValueTagChar(c):
    return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')    

def isMainTagChar(c):
    return isValueTagChar(c) or (c >= '0' and c <= '9')
            
class Parser(object):
    def _reset_value_tag(self, c=""):
        self._value_tag = c
        self._value_index = 0
    
    def _reset_value(self, s=1):
        self._value_sign = s
        self._value_num = 0
        self._value_den = 1
        self._has_value = False
    
    def _reset(self, state=STATE_OUT):
        self._state = state
        self._main_tag = TAG_PREFIX
        self._parsed = {}
        self._reset_value_tag()
        self._reset_value()
        
    def _update_value(self, c):
        self._value_num = self._value_num * 10 + (ord(c) - ord('0'))
        self._has_value = True
           
    def _update_value_frac(self, c):
        self._update_value(c)
        self._value_den *= 10.0
    
    def __init__(self):
        self._reset()
        
    def parse(self, node, data, time):
        self._node = node  
        self._time = time
        self._reset()
        message_data = {}
        message_start = 0
        message_text = ""
        prev = ' '
        urgent = False
        for i in xrange(0, len(data)):
            c = data[i]
            # out-of-bounds characters reset state always
            if c == '[':
                self._reset(STATE_MAIN_TAG)
            elif c == ']':
                self._process_tag_over(c)
                message_data.update(self._parsed)
                self._reset()
            elif c == '\r':
                urgent = prev == '*' # urgent when '*' is before '\r'
                if urgent:
                    message_text = data[message_start:i-1]
                self._reset(STATE_0D)
                message_start = i+1
            elif c == '\n':
                if self._state == STATE_0D:
                    # message is over with '\r\n'
                    if urgent:
                        CURRENT.messages.append(Message(message_text, self._time, self._node, CURRENT.next_message_index()))
                        if len(CURRENT.messages) > MAX_MESSAGES:
                            CURRENT.messages.popleft()
                        message_text = ""
                        CURRENT.urgent_data.update(message_data)
                    CURRENT.data.update(message_data)
                    message_data = {}
                    if urgent and not CURRENT.urgent:
                        CURRENT.urgent = True
                self._reset()
                message_start = i+1
                
            # otherwise - switch by state
            elif self._state == STATE_0D:
                message_data = {}
                self._reset() # something else after \r seen    
                message_start = i+1
            elif self._state == STATE_MAIN_TAG:
                if c == ':':
                    self._state = STATE_VALUE_OR_TAG_0
                elif isMainTagChar(c):
                    self._main_tag += c
                else:
                    self._reset()    
            elif self._state == STATE_VALUE_OR_TAG_0:
                if isValueTagChar(c):
                    self._value_tag += c
                else:
                    self._process_tag_over(c, STATE_VALUE_OR_TAG_0)
            elif self._state == STATE_VALUE_OR_TAG:
                if isValueTagChar(c):
                    self._value_tag += c
                elif (len(self._value_tag) > 0 and c == ' '):
                    self._state = STATE_VALUE_LEAD_SPACE
                else:
                    self._process_tag_over(c)
            elif self._state == STATE_VALUE_LEAD_SPACE:
                if (c == ' '):
                    pass # skipping more leading spaces
                else:        
                    self._process_tag_over(c, STATE_VALUE_OR_TAG_0)
            elif self._state == STATE_TAG_OVER:
                self._process_tag_over(c)
            elif self._state == STATE_VALUE_0:
                if (c >= '0' and c <= '9'):
                    self._state = STATE_VALUE
                    self._update_value(c)
                else:
                    self._process_tag_over(c)
            elif self._state == STATE_VALUE:
                if (c >= '0' and c <= '9'):
                    self._update_value(c)
                elif (c == '.'):
                    self._state = STATE_VALUE_FRAC
                else:
                    self._process_tag_over(c)
            elif self._state == STATE_VALUE_FRAC:
                if (c >= '0' and c <= '9'):
                    self._update_value_frac(c)
                else:
                    self._process_tag_over(c)
            # keep prev char
            prev = c        
                    
    def _process_tag_over(self, c, state=STATE_TAG_OVER):
        # flush value if needed
        if self._has_value:
            tag = self._main_tag + self._value_tag
            if self._value_index > 0:
                tag += str(self._value_index)
            value = self._value_sign * self._value_num / self._value_den
            #print tag, '=', value    
            self._parsed[tag] = Data(tag, value, self._time, self._node)
            self._reset_value()
            self._value_index += 1
        # process char    
        if isValueTagChar(c):
            self._state = STATE_VALUE_OR_TAG
            self._reset_value_tag(c)
        elif (c == '-'):
            self._state = STATE_VALUE_0
            self._reset_value(-1)   
        elif (c == '+'):
            self._state = STATE_VALUE_0
            self._reset_value()   
        elif (c >= '0' and c <= '9'):
            self._state = STATE_VALUE
            self._reset_value()   
            self._update_value(c)
        else:
            self._state = state
            if state == STATE_TAG_OVER and self._value_index == 0:
                self._value_index = 1
                
class Data(object):
    def __init__(self, tag, value, time, node):
        self.tag = tag
        self.value = value
        self.time = time
        self.node = node
        self.sent = False
        
    def __str__(self):
        return self.tag + "," + str(self.value) + "," + fmt_time(self.time) + "," + self.node    

    def __repr__(self):
        return "Data(" + str(self) + ")"    

    def element(self):
        return Element("d", dict(tag=self.tag, time=fmt_time(self.time), node=self.node), [self.value])
    
    def csv(self, now):
        return self.tag + "," + str(self.value) + "," + str(int(self.time - now)) + "s"

class Message(object):
    def __init__(self, message, time, node, index):
        self.message = message
        self.time = time
        self.node = node
        self.index = index
        self.sent = False
        
    def __str__(self):
        return self.message + "," + fmt_time(self.time) + "," + self.node    

    def __repr__(self):
        return "Message(" + str(self) + ")"    

    def element(self):
        return Element("m", dict(time=fmt_time(self.time), node=self.node), [self.message])
    
    def csv(self, now):
        return "1," + self.message + "," + str(int(self.time - now)) + "s," + str(self.index)
