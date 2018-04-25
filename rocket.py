from vector import Vector, normalize,getPerpComponent
from quaternion import Quaternion
from math import asin, acos,sqrt,pi,sin
from utility import hexToFloat, hexToInt

class Flight:
    north=Vector((0,0,0))
    up=Vector((0,0,0))

    goodRef=False

    pointing=Vector((1,0,0))
    rollRef=Vector((0,0,1))
    last=None

    def __init__(self,line):
        nums = []
        self.lastLocation=None

        if not Flight.goodRef:
            Flight.makeRefrence(line)
            Flight.goodRef=True
        for i in range(0,56,8):
            nums.append(hexToFloat(line[i:i+8]))

        self.q=Quaternion(Vector((nums[0],nums[1],nums[2])),nums[3]);
        self.a=Vector((nums[4],nums[5],nums[6]))
        self.rho=0
        self.flightEvent=0
        self.t=hexToInt(line[56:])/1000


        self.previous=Flight.last
        Flight.last=self

    def getV(self):
        return self._getRandV()[0]

    def getSpeed(self):
        return abs(self.getV())

    def getPos(self):
        return self._getRandV()[1]

    def getPitch(self,degrees=False):
        return asin(self._getPointing().dot(Flight.up))*(180/pi if degrees else 1)

    def getRoll(self,degrees=False):
        ref=None
        if self.getPitch()>pi/2-0.01:
            ref=self._getRawRollRef()
        elif self.getPitch()<0.01-pi/2:
            self._getRawRollRef()*-1
        else:
            Q=Quaternion()
            Q.fromTwoVectors(self._getPointing(),Flight.up)

            ref=normalize(Q.rotateVector(self.q.rotateVector(self._getRawRollRef()))*(1 if self.getPitch()>0 else -1))

        return (acos(not Flight.north.dot(ref))+(pi if Flight.east().dot(ref)<=0 else 0))*(180/pi if degrees else 1)

    def getRollRate(self,degrees=False):
        oldRoll=self.previous.getRoll()
        currentRoll=self.getRoll()
        deltaT=self.t-self.previous.t
        rate=None
        if oldRoll>7/4*pi and currentRoll < 1/4*pi:
            rate=(currentRoll-oldRoll+2*pi)/deltaT
        elif oldRoll <1/4*pi and currentRoll>7/4*pi:
            rate=(currentRoll-oldRoll-2*pi)/deltaT
        else:
            rate (currentRoll-oldRoll)/deltaT

        return rate*(180/pi if degrees else 1)

    def getAltitude(self):
        return self.getPos().dot(Flight.up)

    def getDownRange(self):
        return sqrt(abs(self.getPos())**2 - self.getAltitude()**2)

    def getApogee(self):
        canidate=self.previous.getApogee() if self.previous!=None else 0
        if self.getAltitude()>canidate:
            return self.getAltitude()
        else:
            return canidate

    def getMaxSpeed(self):
        canidate=self.previous.getMaxSpeed() if self.previous!=None else 0
        if self.getSpeed()>canidate:
            return self.getSpeed()
        else:
            return canidate

    def _getRandV(self):
        self.lastVal=(Vector((0,0,0)),Vector((0,0,0))) if self.previous==None else self.previous.lastVal
        v0=self.lastVal[0]
        r0=self.lastVal[1]
        deltaT=self.t-(self.previous.t if self.previous!=None else 0)

        return (v0+self.a*deltaT,r0+v0*deltaT+(self.a*deltaT**2)/2)

    def _getPointing(self):
        return normalize(self.q.rotateVector(Flight.pointing))

    def _getRawRollRef(self):
        return normalize(self.q.rotateVector(Flight.rollRef))


    def __str__(self):
        result = "At t="+str(self.t)+", the rocket was at altitude "+str(self.getAltitude())+"m and speed "+str(self.getSpeed())+"m s^-2\m\n"
        result = result +"q="+str(self.q)+", a="+str(self.a)+"\n"
        result = result +"pitch was "+str(self.getPitch())+", roll was "+str(self.getRoll())+"\n"
        return   result+"============\n"

    @classmethod
    def east(cls):
        return normalize(cls.north.cross(cls.up))


    @classmethod
    def makeRefrence(cls,line):
        nums = []
        for i in range(0, 48, 8):
            nums.append(hexToFloat(line[i:i + 8]))

        g = Vector((nums[0], nums[1], nums[2]))
        m = Vector((nums[3], nums[4], nums[5]))

        cls.up = normalize(g) * -1
        cls.north = normalize(m - Flight.up*m.dot(Flight.up))