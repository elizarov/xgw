"""XBee names to address mapping for xgw"""

import zigbee
from Queue import Queue, Empty, Full
from threading import Thread
from libs.xbeeprodid import GetXBeeDeviceType, XBeeUnspecified

#---- Constant defs ----

CACHE_FILE = "WEB/python/xgw_xbee_cache.py"
TIMEOUT = 2 # seconds
RETRY = 3 # times 
BROADCAST = "[00:00:00:00:00:00:ff:ff]!"

MAX_QUEUE = 30 # max resolve queue

#---- Mapping dictionaries ----

addr_to_name = {} # maps address string to name string
name_to_addr = {} # maps name string or to (addr,device_type,product_type) tuple

#---- Function defs ----

def write_cache():
    print "xgw: Writing new ", CACHE_FILE
    f = open(CACHE_FILE, 'w')
    f.write("name_to_addr = " + repr(name_to_addr))
    f.close()
    
def update(map, k, v):
    if k not in map or map[k] != v:
        map[k] = v
        return True
    return False
    
def map(name, addr, device_type=XBeeUnspecified, product_type=XBeeUnspecified):
    u1 = update(addr_to_name, addr, name)
    if device_type != XBeeUnspecified or product_type != XBeeUnspecified:
        addr = (addr, device_type, product_type)
    else:
        if name in name_to_addr:
            old = name_to_addr[name]
            if type(old) == tuple:
                addr = (addr, old[1], old[2])
    u2 = update(name_to_addr, name, addr)
    if u1 or u2:
        print "xgw: Updated mapping for ", name, " to ", repr(addr)
        return True 
    return False

def map_write(name, addr, device_type=XBeeUnspecified, product_type=XBeeUnspecified):
    if map(name, addr, device_type, product_type):
        write_cache()

def map_node_list():
    list = zigbee.get_node_list();
    u = False
    for node in list:
        if node.label:
            if map(node.label, node.addr_extended):
                u = True
    if u:
        write_cache()

def is_addr(addr):
    return addr.endswith("!")

def get_addr_from_tuple(addr):
    if type(addr) == tuple:
        return addr[0]
    return addr
    
def to_addr(name):
    """Resolves an address or name string into an address."""
    if is_addr(name):
        return name
    if not name:
        return BROADCAST
    if name in name_to_addr:
        return get_addr_from_tuple(name_to_addr[name])
    a = ""
    for i in range(RETRY):
        print "xgw: Discovering node ", name, " (", i + 1, " of ", RETRY, ")"
        try:
            a = zigbee.ddo_command(BROADCAST, "DN", name, TIMEOUT)
        except Exception, e:
            print "xgw: Discovery failed ", e
        else:
            break
    if not a:
        return name
    addr = "[" + ":".join([hex(ord(ch)).replace('0x', '').zfill(2) 
                           for ch in a[2:]]) + "]!"
    print "xgw: Discovered ", addr, " for ", name
    map_write(name, addr)
    return addr     
        
def to_name(addr, get_device_type=False):
    """Returns a name for a give name or address string, quering it if needed."""
    if not is_addr(addr):
        return addr
    has_name = addr in addr_to_name 
    if has_name and (not get_device_type or type(name_to_addr[addr_to_name[addr]]) == tuple):
        return addr_to_name[addr]
    name = ""
    if has_name:
        name = addr_to_name[addr]
    else:
        for i in range(RETRY):
            print "xgw: Quering name for ", addr, " (", i + 1, " of ", RETRY, ")"
            try:
                name = zigbee.ddo_get_param(addr, "NI", TIMEOUT)
            except Exception, e:
                print "xgw: Query failed ", e
            else:
                break
        if not name:
            return addr
        print "xgw: Found name ", name, " for ", addr
    device_type, product_type = XBeeUnspecified, XBeeUnspecified
    if get_device_type:
        print "xgw: Getting device type for ", addr, " ", name
        device_type, product_type = GetXBeeDeviceType(addr)
        print "xgw: Found device type (", hex(device_type), ",", hex(product_type), ") for ", addr, " ", name
    map_write(name, addr, device_type, product_type)
    return name

#---- Background lazy resolver thread

class Resolver(Thread):
    def __init__(self):
        Thread.__init__(self, name="Resolver")
        self._closed = False
        self._resolve_name = set()
        self._resolve_device_type = set()
        self._queue = Queue(MAX_QUEUE)
        
    def close(self):
        self._closed = True
        self.join()
        
    def run(self):
        while not self._closed:
            try: 
                addr = self._queue.get(True, 1) # block for at most 1 sec for ability to close it
                get_device_type = addr in self._resolve_device_type
                to_name(addr, get_device_type)
                self._resolve_name.remove(addr)
                if get_device_type:
                    self._resolve_device_type.remove(addr)
            except Empty:
                pass # loop
        
    def to_name_non_blocking(self, addr, get_device_type=False):    
        """Returns a name for a given name or address string (non-blocking)."""
        if not is_addr(addr):
            return addr
        # addr is really an address
        if addr in addr_to_name and (not get_device_type or type(name_to_addr[addr_to_name[addr]]) == tuple):
            return addr_to_name[addr]
        enqueue = False
        if addr not in self._resolve_name:
            self._resolve_name.add(addr)
            enqueue = True
        if get_device_type and addr not in self._resolve_device_type:
            self._resolve_device_type.add(addr)
            enqueue = True
        if enqueue:        
            try:
                self._queue.put_nowait(addr)
            except Full:
                # ignore failure
                self._resolve_name.remove(addr) 
                self._resolve_device_type.remove(addr)
        return addr
    
    def to_product_type_non_blocking(self, addr):
        if addr in addr_to_name:
            name = addr_to_name[addr]
            t = name_to_addr[name]
            if type(t) == tuple:
                return t[1], t[2]
        return XBeeUnspecified, XBeeUnspecified
     
#---- Load cache file on startup ----

print "xgw: Checking ", CACHE_FILE
try:
    f = open(CACHE_FILE)
except IOError:
    write_cache()
else:
    f.close()
    
import xgw_xbee_cache

name_to_addr = xgw_xbee_cache.name_to_addr
addr_to_name = dict([(get_addr_from_tuple(a), n) for (n, a) in name_to_addr.items()])

print "xgw: Updating node list"
map_node_list()
            