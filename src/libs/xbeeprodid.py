###############################################################################
#                                                                             #
#                 Digi Device Type Introduction (DD and #D)                   #
#                                                                             #
###############################################################################
#                                                                             #
# A Digi Device Type field is being supported to indicate what product a      #
# given wireless device is operating on.                                      #
# The Digi Device Type field is a 4 byte value.                               #
# The top 2 bytes specify the wireless module type and are not adjustable.    #
# The lower 2 bytes specify the end product type and are settable.            #
# The 4-byte Digi Device Type value can always be read with the DD command.   #
#                                                                             #
###############################################################################
#                                                                             #
# Module Types                                                                #
#                                                                             #
# The module type field is indicated in the high 2 bytes of the DD value.     #
#     Module Type         DD High Bytes                                       #
#     Unspecified         0x0000                                              #
#     XBee Series 1       0x0001                                              #
#     XBee Series 2       0x0002                                              #
#     XBee ZB             0x0003                                              #
#     XBeeDigiMesh        0x0004                                              #
###############################################################################
#                                                                             #
# Product Types                                                               #
#                                                                             #
# The product type field is indicated in the low 2 bytes of the DD value.     #
# Note that for some products, DD will have to be written to the module after #
# it is installed. For other products, DD will be preconfigured when the      #
# firmware is loaded into the module.                                         #
#                                                                             #
#     Product Type                    DD Low Bytes                            #
#     Unspecified                     0x0000                                  #
#     X8 Gateway                      0x0001                                  #
#     X4 Gateway                      0x0002                                  #
#     X2 Gateway                      0x0003                                  #
#     Commissioning Tool              0x0004                                  #
#     RS-232 Adapter                  0x0005                                  #
#     RS-485 Adapter                  0x0006                                  #
#     XBee Sensor (1-wire) Adapter    0x0007                                  #
#     Wall Router                     0x0008                                  #
#     RS-232 Power Harvester Adapter  0x0009                                  #
#     Digital IO Adapter              0x000A                                  #
#     Analog IO Adapter               0x000B                                  #
#     X-Stick                         0x000C                                  #
#     XBee Sensor /L/T/H Adapter      0x000D                                  #
#     XBee Sensor /L/T Adapter        0x000E                                  #
#     XBee Smart Plug Adapter         0x000F                                  #
#     XBee USB Dongle                 0x0010                                  #
#     XBee Massa M3                   0x0201                                  #
###############################################################################

XBeeUnspecified                = 0x0000
XBeeSeries1                    = 0x0001
XBeeSeries2                    = 0x0002
XBeeZB                         = 0x0003
XBeeDigiMesh                   = 0x0004
XBeeDigiMesh24                 = 0x0005
XBee868                        = 0x0006
XBeeDP900                      = 0x0007


XBeeX8Gateway                  = 0x0001
XBeeX4Gateway                  = 0x0002
XBeeX2Gateway                  = 0x0003
XBeeCommissioningTool          = 0x0004
XBeeRS232Adapter               = 0x0005
XBeeRS485Adapter               = 0x0006
XBeeSensorAdapter              = 0x0007
XBeeWallRouter                 = 0x0008
XBeeRS232PowerHarvesterAdapter = 0x0009
XBeeDigitalIOAdapter           = 0x000A
XBeeAnalogIOAdapter            = 0x000B
XBeeXStick                     = 0x000C
XBeeSensorLTHAdapter           = 0x000D
XBeeSensorLTAdapter            = 0x000E
XBeeSmartPlugAdapter           = 0x000F
XBeeUSBDongle                  = 0x0010
XBeeMassaM3                    = 0x0201

XBeeUnspecifiedName                = "Unspecified"
XBeeSeries1Name                    = "XBee Series 1"
XBeeSeries2Name                    = "XBee Series 2"
XBeeZBName                         = "XBee ZB"
XBeeDigiMeshName                   = "XBee Digi Mesh 900"
XBeeDigiMesh24Name                 = "XBee Digi Mesh 2.4"
XBee868Name                        = "XBee 868"
XBeeDP900Name                      = "XBee DP 900"

XBeeX8GatewayName                  = "X8 Gateway"
XBeeX4GatewayName                  = "X4 Gateway"
XBeeX2GatewayName                  = "X2 Gateway"
XBeeCommissioningToolName          = "Commissioning Tool"
XBeeRS232AdapterName               = "RS-232 Adapter"
XBeeRS485AdapterName               = "RS-485 Adapter"
XBeeSensorAdapterName              = "XBee Sensor Adapter"
XBeeWallRouterName                 = "Wall Router"
XBeeRS232PowerHarvesterAdapterName = "RS-232 Power Harvester Adapter"
XBeeDigitalIOAdapterName           = "Digital IO Adapter"
XBeeAnalogIOAdapterName            = "Analog IO Adapter"
XBeeXStickName                     = "X-Stick"
XBeeSensorLTHAdapterName           = "XBee Sensor /L/T/H Adapter"
XBeeSensorLTAdapterName            = "XBee Sensor /L/T Adapter"
XBeeSmartPlugAdapterName           = "XBee Smart Plug Adapter"
XBeeUSBDongleName                  = "XBee USB Dongle"
XBeeMassaM3Name                    = "XBee Massa M3"

# For the Sensor Adapter, there are many sensor types that can be used.
# Define a list of all known/supported sensor types below.

WatchportUnspecified      = 0x0            # Unspecified WatchPort sensor
WatchPortHSensor          = 0x1            # Humidity/Temperature sensor
WatchPortTSensor          = 0x2            # Temperature sensor
WatchPortDSensor          = 0x3            # Distance/Proximity sensor
WatchPortWSensor          = 0x4            # Water Detector sensor
WatchPortASensor          = 0x5            # Accelerometer sensor

WatchPortSensorMax        = 0x5            # Current Max number of Sensors we support.

WatchportUnspecifiedName  = "Unknown Watchport Sensor"
WatchPortHSensorName      = "Watchport/H Drop-in Networking Sensor - Humidity/Temperature sensor"
WatchPortTSensorName      = "Watchport/T Drop-in Networking Sensor - Temperature sensor"
WatchPortDSensorName      = "Watchport/D Drop-in Networking Sensor - Distance/Proximity sensor"
WatchPortWSensorName      = "Watchport/W Drop-in Networking Sensor - Water detector"
WatchPortASensorName      = "Watchport/A Drop-in Networking Sensor - Accelerometer"


###############################################################################

import zigbee
import struct

# GetXBeeDeviceType
#
# Probes device, and returns a device type and product type.
#
def GetXBeeDeviceType(address):
  
	# Attempt the "DD" command a couple times if it fails for some reason.
  for i in xrange(0, 5):
    try:
			device_type, product_type = struct.unpack('HH', zigbee.ddo_get_param(address, 'DD'))
    except:
			continue
    else:
      if (device_type != XBeeUnspecified) and (product_type != XBeeUnspecified):
        return device_type, product_type      

	# Perhaps we are on some older firmware that doesn't support the
	# "DD" command...
	# So lets try the older "VR" command instead.	
	
  for i in xrange(0, 5):
		try:
			version = struct.unpack('=H', zigbee.ddo_get_param(address, 'VR'))[0]
			hardware = struct.unpack('=H', zigbee.ddo_get_param(address, 'HV'))[0]			
		except:
			continue
		else:
			version = version & 0xFF00
			hardware = hardware & 0xFF00
			
			## WARNING! This gets a bit sticky.
			
			## We need to cross reference the Series of the radio which is determined
			## from the hardware version, to determine what the firmware version 
			## really means.  Please note that not ALL firmware versions are specified.  
			
			## Current cross referencing is due to how the 802.15.4 firmware is 
			## versioned.  It does not line up with the versioning on the Series 2 or
			## ZB firmware.  
			
			## In addition to the above, we can't be sure what hardware we have.
			## In the case of a coordinator API firmware, we can't differentiate
			## between a CPX8, CPX4, or CPX2.  And due to the multiple use of the
			## 0x1200 (Router AT) firmware, we cannot tell if its a wall router, 
			## rs-232 adapter, rs-485 adapter or XBee smart plug.
			
			## The 802.15.4 firmware which covers the gateway, rs-232 adapter, rs-485
			## adapter, wall router and smartplug is all one firmware version.  
			
			## In short, if the above identification via the 'DD' parameter fails,
			## we can only make guesses as to what we really are identifying!  			
			
			## 802.15.4: Regular = 0x1700, PRO = 0x1800
			if hardware == 0x1700 or hardware == 0x1800:
				series = XBeeSeries1
			
			## ZB/Znet 2.5 Regular = 0x1900, PRO = 0x1a00
			elif hardware == 0x1900 or hardware == 0x1a00:
				if (version & 0xF000) == 0x1000:
					series = XBeeSeries2
				elif (version & 0xF000) == 0x2000:
					series = XBeeZB
				else:
					return (XBeeUnspecified, XBeeUnspecified)
			else:
				return (XBeeUnspecified, XBeeUnspecified)
						
			if (version == 0x1200) and (series == XBeeSeries1):
				return (series, XBeeSensorAdapter)
			
			version = version & 0x0F00			
			
			if (version == 0x0000) and (series == XBeeSeries1):				
				return (series, XBeeX8Gateway) 
			elif (version == 0x0400) and ((series == XBeeSeries2) or (series == XBeeZB)):				
				return (series, XBeeSensorAdapter)
			elif version == 0x0500:				
				return (series, XBeeRS232PowerHarvesterAdapter)
			elif version == 0x0600:
				return (series, XBeeAnalogIOAdapter)
			elif version == 0x0700:
				return (series, XBeeDigitalIOAdapter)			
			else:
				return (series, XBeeUnspecified)
	
  return (XBeeUnspecified, XBeeUnspecified)
  
# GetXBeeProductName
#
# Returns an official product name, given a product type device id.
#
def GetXBeeProductName(product_type):	
	if product_type == XBeeX8Gateway:
		result = XBeeX8GatewayName
	elif product_type == XBeeX4Gateway:
		result = XBeeX4GatewayName
	elif product_type == XBeeX2Gateway:
		result = XBeeX2GatewayName
	elif product_type == XBeeCommissioningTool:
		result = XBeeCommissioningToolName
	elif product_type == XBeeRS232Adapter:
		result = XBeeRS232AdapterName
	elif product_type == XBeeRS485Adapter:
		result = XBeeRS485AdapterName
	elif product_type == XBeeSensorAdapter:
		result = XBeeSensorAdapterName
	elif product_type == XBeeWallRouter:
		result = XBeeWallRouterName
	elif product_type == XBeeRS232PowerHarvesterAdapter:
		result = XBeeRS232PowerHarvesterAdapterName
	elif product_type == XBeeDigitalIOAdapter:
		result = XBeeDigitalIOAdapterName
	elif product_type == XBeeAnalogIOAdapter:
		result = XBeeAnalogIOAdapterName
	elif product_type == XBeeXStick:
		result = XBeeXStickName
	elif product_type == XBeeSensorLTHAdapter:
		result = XBeeSensorLTHAdapterName
	elif product_type == XBeeSensorLTAdapter:
		result = XBeeSensorLTAdapterName
	elif product_type == XBeeSmartPlugAdapter:
		result = XBeeSmartPlugAdapterName
	elif product_type == XBeeUSBDongle:
		result = XBeeUSBDongleName
	elif product_type == XBeeMassaM3:
		result = XBeeMassaM3Name
	else:
		result = XBeeUnspecifiedName

	return result

# GetXBeeDeviceNodeIdentifier
#
# Probes device, and returns its Node Indentifier String
#
def GetXBeeDeviceNodeIdentifier(address):

	# Attempt the "NI" command a couple times if it fails for some reason.
	for i in range(0, 10):
		try:
			node_name = zigbee.ddo_get_param(address, 'NI')
		except:
			continue
		else:
			return node_name

	return None

# GetSensorProductName
#
# Returns an official sensor product name, given a sensor value.
#
def GetSensorProductName(product_type):
	if product_type == WatchPortHSensor:
		result = WatchPortHSensorName
	elif product_type == WatchPortTSensor:
		result = WatchPortTSensorName
	elif product_type == WatchPortDSensor:
		result = WatchPortDSensorName
	elif product_type == WatchPortWSensor:
		result = WatchPortWSensorName
	elif product_type == WatchPortASensor:
		result = WatchPortASensorName
	else:
		result = WatchPortUnspecifiedName

	return result

