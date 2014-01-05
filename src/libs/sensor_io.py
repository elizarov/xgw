import struct

def parseIS(data):

    ## We need to differentiate between series 1 and series 2 formats
    ## The series 1 format should always return a 'odd' byte count eg 7, 9, 11 or 13 bytes
    ## The series 2 format should always return a 'even' byte count eg, 8, 10, 12 or 14 bytes
    ## So we mod 2 the length, 0 is series 2, 1 is series 1.  Simple right?
    
    if len(data) % 2 == 0:
        sets, datamask, analogmask = struct.unpack("!BHB", data[:4])
        data = data[4:]
        
    else:        
        sets, mask = struct.unpack("!BH", data[:3])
        data = data[3:]
        datamask = mask % 512 # Move the first 9 bits into a seperate mask
        analogmask  = mask >> 9 #Move the last 7 bits into a seperate mask
        
    retdir = {}

    if datamask:
        datavals = struct.unpack("!H", data[:2])[0]
        data = data[2:]

        currentDI = 0
        while datamask:
            if datamask & 1:
                retdir["DIO%d" % currentDI] = datavals & 1
            datamask >>= 1
            datavals >>= 1
            currentDI += 1

    currentAI = 0
    while analogmask:
        if analogmask & 1:
            aval = struct.unpack("!H", data[:2])[0]
            data = data[2:]

            retdir["AI%d" % currentAI] = aval
        analogmask >>= 1
        currentAI += 1

    return retdir

if __name__ == "__main__":
    d = parseIS("\x01=\xd0\x0f\x18@\x00\x01\x00\x11\x00\x01\x00\x11")
    print d
    
