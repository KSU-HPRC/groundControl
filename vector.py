from math import sqrt

class Vector:
    def __init__(self,tup=(0,0,0)):
        self.x=tup[0]
        self.y=tup[1]
        self.z=tup[2]
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)

    def __add__(self, other):
        return Vector((self.x+other.x,self.y+other.y,self.z+other.z))

    def __mul__(self, other):
        return Vector((self.x*other,self.y*other,self.z*other))

    def __sub__(self, other):
        return Vector((self.x-other.x,self.y-other.y,self.z-other.z))

    def dot(self,other):
        return self.x*other.x+self.y*other.y+self.z*other.z

    def cross(self,other):
        result=Vector()
        result.x=self.y*other.z-self.z*other.y
        result.y=self.z*other.x-self.x*other.z
        result.z=self.x*other.y-self.y*other.x
        return result

    def normalize(self):
        mag=abs(self)
        self.x/=mag
        self.y/=mag
        self.z/=mag


    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+','+str(self.z)+')'

def normalize(vec):
    mag=abs(vec)
    return Vector((vec.x/mag,vec.y/mag,vec.z/mag))