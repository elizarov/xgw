"""xgw main logic module."""

import rci
from xgw_xbee import XBee
from xgw_controller import Controller
from xgw_xml_parser import Parser

RCI_CALLBACK_NAME = "xgw"

print "xgw: Creating XBee connection"
xbee = XBee()

print "xgw: Creating controller"
controller = Controller(xbee)

print "xgw: Creating parser"
parser = Parser(controller)

print "xgw: Starting XBee thread"
xbee.start()

print "xgw: Registering RCI callback ", RCI_CALLBACK_NAME
rci.add_rci_callback(RCI_CALLBACK_NAME, parser.parse)
controller.quit() # if terminating

