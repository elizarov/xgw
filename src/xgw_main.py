"""xgw main logic module."""

import rci
from xgw_xbee_map import Resolver
from xgw_xbee import XBee
from xgw_controller import Controller
from xgw_dispatcher import Dispatcher
from xgw_uploader import Uploader

RCI_CALLBACK_NAME = "xgw"

print "xgw: Creating XBee name resolver"
resolver = Resolver()

print "xgw: Creating XBee connection"
xbee = XBee(resolver)

print "xgw: Creating HTTP uploader"
uploader = Uploader(xbee)

print "xgw: Creating controller"
controller = Controller(xbee, uploader)

print "xgw: Creating dispatcher"
dispatcher = Dispatcher(controller)

print "xgw: Starting XBee name resolver thread"
resolver.start()

print "xgw: Starting XBee conection thread"
xbee.start()

print "xgw: Starting HTTP uploader thread"
uploader.start()

print "xgw: Registering RCI callback ", RCI_CALLBACK_NAME
rci.add_rci_callback(RCI_CALLBACK_NAME, dispatcher.callback)
controller.quit() # if terminating
