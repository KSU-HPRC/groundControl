import struct
from digi.xbee.devices import XBeeDevice
from utility import getOpts, floatToHex,hexToFloat

#File IO

fin=None

while fin==None:
	try:
		fname = input("File name to read from: ")
		fin = open(fname, 'r')
		print("Opened file: ", fname)
	except IOError:
		print("Could not open file: ", fname)
		fin=None

dataEntries = []
j = 1
for line in fin:
	print(j, ": ")
	for i in range (0,80,8):
		print(line[i:i+8], end=' ')
	print('\n')
	if line=='\n':
		continue
	line[:-2]
	tempFloats=[]
	i = 0
	for i in range (0,80,8):
		print(line[i:i+8])
		tempFloats.append(round(hexToFloat(line[i:i+8]), 2))
	tempFloats.append(int(line[i:i+8], 16))
	i += 8
	tempFloats.append(bytes.fromhex(line[i:i+4]).decode('ascii'))
	print(tempFloats)
	dataEntries.append(tempFloats)
	j += 1

#print(dataEntries)
