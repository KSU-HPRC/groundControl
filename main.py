from digi.xbee.devices import XBeeDevice
from utility import getOpts, floatToHex,hexToFloat
from rocket import Flight

logFile=open("Launch1Log.TXT")

lines=[]
for line in logFile:
    lines.append(line[:64])

for line in lines:
    #print(line)
    snapShot=Flight(line)
    print(snapShot)