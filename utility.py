import sys
import struct

def getOpts():
    opts={}
    args=sys.argv
    lastKey='nokey'
    opts[lastKey]=[]

    while(args):
        if args[0][0]=='-':
            lastKey=args[0]
            opts[lastKey]=[]
        else:
            try:
                opts[lastKey].append(args[0])
            except:
                break
        args=args[1:]

    return opts

def floatToHex(float):
    return hex(struct.unpack('<I', struct.pack('<f', float))[0])

def hexToFloat(hex):
    #print(len(hex))
    return struct.unpack('<f',bytes.fromhex(hex))[0]

def hexToInt(hex):
    return struct.unpack('<I',bytes.fromhex(hex))[0]