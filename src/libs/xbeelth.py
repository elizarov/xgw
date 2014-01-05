############################################################################
#                                                                          #
# Functions:                                                               #
#                                                                          #
#    raw_sample()                                                          #
#                                                                          #
#        Returns a dictionary of raw analog sample data                    #
#                                                                          #
#        The dictionary will contain the following keys:                   #
#            1) 'temperature'                                              #
#            2) 'light'                                                    #
#            3) 'humidity'                                                 #
#                                                                          #
#                                                                          #
#    sample()                                                              #
#                                                                          #
#        Returns a dictionary of data scaled into actual usable values.    #
#                                                                          #
#        The dictionary will contain the following keys:                   #
#            1) 'temperature' - Degrees in Celcius.                        #
#            2) 'light' - value in lux.                                    #
#            3) 'humidity' - value in %rh                                  #
#                                                                          #
############################################################################

import zigbee
from sensor_io import parseIS

def raw_sample(io_sample):
    """raw_sample(channel) => A/D reading
    Returns raw unscaled A/D light, temperature and humidity sample data"""
    
    light = parseIS(io_sample)["AI1"]
    temp  = parseIS(io_sample)["AI2"]
    hum   = parseIS(io_sample)["AI3"]

    item = {'t': temp, 'l': light, 'h': hum}
    return item

def sample(io_sample):
    """sample() => Converts raw sensor data into actual usable values."""

    item = raw_sample(io_sample)
    mVanalog = (float(item['t'])  / 1023.0) * 1200.0
    temp_C = (mVanalog - 500.0)/ 10.0 # -4.0
    ##NOTE:  Removed self heating correction of -4.0 celsius. 
    ##       Device is intended to be battery powered, which produces minimal 
    ##       self heating.  - MK 3/04/09

    lux = (float(item['l'])  / 1023.0) * 1200.0

    mVanalog = (float(item['h']) / 1023.0) * 1200.0
    hum = (((mVanalog * 108.2 / 33.2) / 5000 - 0.16) / 0.0062)

    item = { 't': round(temp_C, 1), 'l': round(lux), 'h': round(hum) }
    return item
