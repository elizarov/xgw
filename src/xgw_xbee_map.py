"""XBee names to address mapping for xgw"""

import zigbee

#---- Constant defs ----

CACHE_FILE = "WEB/python/xgw_xbee_cache.py"
TIMEOUT = 2 # seconds
RETRY = 3 # times 
BROADCAST = "[00:00:00:00:00:00:ff:ff]!"

#---- Mapping dictionaries ----

addr_to_name = {}
name_to_addr = {}

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
    
def map(name, addr):
    u1 = update(addr_to_name, addr, name)
    u2 = update(name_to_addr, name, addr) 
    return u1 or u2

def map_write(name, addr):
    if map(name, addr):
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
    
def to_addr(name):
    """Resolves an address or name string into an address."""
    if is_addr(name):
        return name
    if not name:
        return BROADCAST
    if name in name_to_addr:
        return name_to_addr[name]
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
        
def to_name_lazy(addr):
    """Returns a name for a give name or address string."""
    if not is_addr(addr):
        return addr
    if addr in addr_to_name:
        return addr_to_name[addr]
    return addr
        
def to_name(addr):
    """Returns a name for a give name or address string, quering it if needed."""
    if not is_addr(addr):
        return addr
    if addr in addr_to_name:
        return addr_to_name[addr]
    name = ""
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
    map_write(name, addr)
    return name

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
addr_to_name = dict([(a, n) for (n, a) in name_to_addr.items()])

print "xgw: Updating node list"
map_node_list()
        