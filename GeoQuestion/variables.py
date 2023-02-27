import math
from .primary_functions import easyatan,order_dots_by_OutAngleRule,select_from_
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

class Coordinate:
    def __init__(self,coordinates):
        self.x,self.y = coordinates
    def __add__(self,U):
        return Coordinate((self.x+U.x,self.y+U.y))
    def __sub__(self,U):
        return Coordinate((self.x-U.x,self.y-U.y))
    def __mul__(self, other : float):
        return Coordinate((self.x*other,self.y*other))
    def __rmul__(self, other : float):
        return Coordinate((self.x*other,self.y*other))
    def __truediv__(self,other: float):
        return Coordinate((self.x/other,self.y/other))
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"
    def slope(self):
        return self.y/self.x
    def getArrayLike(self):
        return [self.x,self.y]
    
    def rotate(self,angle_in_rad : float,center_point=None):
        if center_point == None: center_point = Coordinate((0,0))
        x = center_point.x - self.x
        y = center_point.y - self.y
        A = math.sqrt(x**2 + y**2)
        alpha = easyatan(y/x)
        return Coordinate((A*math.sin(alpha+angle_in_rad),A*math.sin(alpha+angle_in_rad)))
    
    @staticmethod
    def average_of_coordinates(points):
        sumofcoord = Coordinate((0,0))
        c = 0
        for point in points:
            sumofcoord = point+sumofcoord
        return sumofcoord/len(points)

class Dot:
    def __init__(self,coordinate,name):
        if type(coordinate) == Coordinate:
            self.coord = coordinate
        elif type(coordinate) == tuple:
            self.coord = Coordinate(coordinate)
        self.name = name
    
    def rotate(self,angle_in_rad : float, center_point = Coordinate((0,0))):
        return Dot((self.coord.rotate(angle_in_rad,center_point)),self.name+"'")
    
    def __add__(self,u): # u should be coord
        coord_ = (u.coord + self.coord)
        return Dot((coord_.x,coord_.y),self.name+"MIXED"+u.name)
    def __mul__(self,k : float):
        coord_ = self.coord*k
        return Dot((coord_.x,coord_.y),self.name+"MIXED")
    def __rmul__(self,k : float):
        coord_ = self.coord*k
        return Dot((coord_.x,coord_.y),self.name+"MIXED")
    def __truediv__(self,k : float):
        coord_ = self.coord/k
        return Dot((coord_.x,coord_.y),self.name+"MIXED")
    
    def __str__(self):
        return ("{"+self.name+":"+str(self.coord.getArrayLike())+"}")
    
    @staticmethod
    def average_of_points(points):
        sumofcoord = Dot((0,0),"")
        c = 0
        for point in points:
            sumofcoord = point+sumofcoord
        return sumofcoord/len(points)
    

class Function:
    def __init__(self,constants,name): # constants = [k0, k1, k2, k3...] => f(x) = k0 + k1*x + k2*x**2 + k3*x**3...
        self.const = constants
        self.name = name
    
    def f(self,x):
        r = self.const[0]
        for c in range(1,len(self.const)):
            r += self.const[c]*(x**c)
        return r
    
    def f_numpy(self,xr):
        r = self.const[0]*np.ones(len(xr))
        for c in range(1,len(self.const)):
            r = r + self.const[c]*(xr**c)
        return r
    
    def fcoord(self,x):
        return Coordinate((x,self.f(x)))
    
    def dx_by_vectorsize(self,size):
        if len(self.const) == 2: 
            return math.sqrt((size**2)/(self.const[1]**2+1))
    
    def deriative(self):
        return self.__init__([self.const[i]*i for i in range(1,len(self.const))])
    
    @staticmethod
    def dotsToLine(coord1 : Coordinate,coord2 : Coordinate):
        basic_line = coord2-coord1
        k = basic_line.y/basic_line.x
        c = coord1.y-k*coord1.x
        return Function([c,k])
    
    @staticmethod
    def dotAndSlope(dot : Dot,slope):
        c = dot.coord.y-slope*dot.coord.x
        return Function([c,slope])
    
    @staticmethod
    def intersect(f1,f2):
        x = (f2.const[0]-f1.const[0])/(f1.const[1]-f2.const[1])
        y = (f2.const[1]*f1.const[0]-f1.const[1]*f2.const[0])/(f2.const[1]-f1.const[1])
        return Coordinate((x,y))
    
    @staticmethod
    def rotate_line(line,angle_in_rad : float, center_point = Coordinate((0,0))):
        a1,a2 = line.fcoord(0).rotate(angle_in_rad,center_point),line.fcoord(1).rotate(angle_in_rad,center_point)
        return Function.dotsToLine(a1,a2)



class Polygon:
    def __init__(self, dots : list[Dot],lines_of_intersecteds,name): # if constants_of_intersecteds = [(Function([1,0]), Function([0,1]))] => dots[0] occurs from intersection of f(x) = 1 with f(x) = x
        self.dots,lines_of_intersecteds = order_dots_by_OutAngleRule(dots,lines_of_intersecteds)
        angles = [0 for c in range(0,len(self.dots))]
        angle_vision = [Coordinate((0,0)) for c in range(0,len(self.dots))]
        for x in range(0,len(self.dots)):
            angles[x] = abs( easyatan(lines_of_intersecteds[x][0].const[1]) - easyatan(lines_of_intersecteds[x][1].const[1]) )
            if x != 0 and x != len(self.dots)-1: angles[x] = math.pi-angles[x]

            bisector_line = self.bisector_by_lines(self.dots[x],lines_of_intersecteds[x],x)
            dx = bisector_line.dx_by_vectorsize(1)
            if (Dot.average_of_points(dots)).coord.x < self.dots[x].coord.x or (Dot.average_of_points(dots)).coord.y < self.dots[x].coord.y: dx = dx*-1
            angle_vision[x] = Coordinate((dx,dx*bisector_line.const[1]))
        
        self.angles = angles
        self.angle_vision = angle_vision
        self.name = name
    
    def bisector(self,dot1_id, angle_dot_id, dot2_id):
        dot_id = self.dots.index(self.dots[angle_dot_id])
        angle_of_bisector = (easyatan((self.dots[dot1_id].coord-self.dots[angle_dot_id].coord).slope()) + easyatan((self.dots[dot2_id].coord-self.dots[angle_dot_id].coord).slope()))/2
        k1 = math.tan(angle_of_bisector)

        if dot_id != 0 and dot_id != len(self.dots)-1: k1 = -1/k1

        k0 = self.dots[angle_dot_id].coord.y-k1*self.dots[angle_dot_id].coord.x

        return Function([k0,k1],self.name+"'sBisectorOf "+self.dots[angle_dot_id].name)

    def bisector_by_lines(self, dot, lines_of_intersect, dot_id):
        angle_of_bisector = (easyatan(lines_of_intersect[0].const[1]) + easyatan(lines_of_intersect[1].const[1]))/2
        k1 = math.tan(angle_of_bisector)
        if dot_id != 0 and dot_id != len(self.dots)-1: k1 = -1/k1

        k0 = dot.coord.y-k1*dot.coord.x
        return Function([k0,k1],"bisectorOf"+str(dot.name))
    
    def __getitem__(self,dot_name):
        for dot in self.dots:
            if dot.name == dot_name: return dot
        return Dot((0,0),"NULL")



class Triangle(Polygon):
    def __init__(self, dots : list[Dot],lines_of_intersecteds,name):
        if len(dots) != 3 : print("For defining a Triangle, you should set 3 dots on there... I'm defining an polygon for you but be careful.")
        Polygon.__init__(self,dots,lines_of_intersecteds,name)
    
    def incenter_coordinate(self):
        self.angle_vision[0]
        self.dots[0]
        line1, line2 = Function.dotsToLine(self.dots[0],self.angle_vision[0]),Function.dotsToLine(self.dots[1],self.angle_vision[1])
        return Function.intersect(line1,line2)
    
    def median_line(self,dot_id):
        other_dots = [0,1,2].remove(dot_id)
        median_coord = (self.dots[other_dots[0]].coord+self.dots[other_dots[1]].coord)/2
        return Function.dotsToLine(self.dots[dot_id],median_coord)
    
    def prependicular_line(self,dot_id):
        other_dots = [0,1,2].remove(dot_id)
        k = (self.dots[other_dots[0]].coord-self.dots[other_dots[1]].coord).slope
        k = 1/k # for being prependicular
        c = self.dots[dot_id].coord.y-k*self.dots[dot_id].coord.x

        return Function([c,k])
        
class Angle:
    def bisector(self,dot1_id, angle_dot_id, dot2_id):
        dot_id = self.dots.index(self.dots[angle_dot_id])
        angle_of_bisector = (easyatan((self.dots[dot1_id].coord-self.dots[angle_dot_id].coord).slope()) + easyatan((self.dots[dot2_id].coord-self.dots[angle_dot_id].coord).slope()))/2
        k1 = math.tan(angle_of_bisector)

        if dot_id != 0 and dot_id != len(self.dots)-1: k1 = -1/k1

        k0 = self.dots[angle_dot_id].coord.y-k1*self.dots[angle_dot_id].coord.x

        return Function([k0,k1])
    
    def __init__(self, dots : list[Dot],lines_of_intersected : list[Function],name):
        self.dots,lines_of_intersected = order_dots_by_OutAngleRule(dots,lines_of_intersected)
        angle_id = self.dots.index(dots)
        other_dots = [0,1,2].remove(angle_id)
        angle = abs( easyatan( (dots[angle_id].coord-dots[other_dots[0]].coord).slope() ) - easyatan( (dots[angle_id].coord-dots[other_dots[1]].coord).slope() ) )
        if angle_id != 0 and angle_id != len(self.dots)-1: angle = math.pi-angle

        bisector_line = self.bisector(other_dots[0],angle_id,other_dots[1])
        dx = bisector_line.dx_by_vectorsize(1)
        angle_vision = Coordinate(dx,dx*bisector_line.const[1])

        self.angle = angle
        self.angle_vision = angle_vision
        self.name = name



class Plane:
    @staticmethod
    def minimumRange(dots : list[Dot]):
        from .support import maxminCoordinates
        minCoord, maxCoord = Coordinate(dots[0].coord.getArrayLike()), Coordinate(dots[0].coord.getArrayLike())
        for dot in dots:
            if dot.coord.x < minCoord.x: minCoord.x = dot.coord.x
            if dot.coord.y < minCoord.y : minCoord.y = dot.coord.y
            if dot.coord.x > maxCoord.x : maxCoord.x = dot.coord.x
            if dot.coord.y > maxCoord.y : maxCoord.y = dot.coord.y
        return maxminCoordinates(minCoord,maxCoord)

    def __init__(self):
        self.dots,self.lines,self.angles,self.polygons = [],[],[],[] # dots, lines, angles, polygons
        self.intersect_lines = []
    
    def add_object(self,*new_objects):
        for new_object in new_objects:
            if type(new_object) == Dot: 
                self.dots.append(new_object)
                self.intersect_lines.append(None)
            elif type(new_object) == Function: self.lines.append(new_object)
            elif type(new_object) == Angle: self.angles.append(new_object)
            elif type(new_object) == Polygon: self.polygons.append(new_object)
    
    def find_object_by_name_(self, name, object_type):
        if object_type == Function:
            for c in range(0,len(self.lines)):
                if self.lines[c].name == name: return c
        elif object_type == Dot:
            for c in range(0,len(self.dots)):
                if self.dots[c].name == name: return c
        elif object_type == Polygon:
            for c in range(0,len(self.polygons)):
                if self.polygons[c].name == name: return c
        
        return None
    
    def intersect_and_set(self,line_id1,line_id2,name):
        if type(line_id1) == str: line_id1 = self.find_object_by_name_(line_id1,Function)
        if type(line_id2) == str: line_id2 = self.find_object_by_name_(line_id2,Function)

        coord = Function.intersect(self.lines[line_id1],self.lines[line_id2])
        self.dots.append(Dot(coord,name))
        self.intersect_lines.append([line_id1,line_id2])
    
    def define_polygon_(self, polygon_name, *dotnames):
        intersected_lines = []
        dots = []
        for dotname in dotnames:
            dot_id = self.find_object_by_name_(dotname, Dot)
            if dot_id == None: 
                print("Dot not found.") ; return
            intersection = self.intersect_lines[dot_id]
            print(intersection)
            if intersection == None:
                print("Intersected lines required.") ; return
            intersected_lines.append((self.lines[intersection[0]],self.lines[intersection[1]]))
            dots.append(self.dots[dot_id])
        self.polygons.append(Polygon(dots,intersected_lines,polygon_name))
    
    def to_graph(self,graph_step = 0.1):
        maxminRange = Plane.minimumRange(self.dots)
        
        fig,ax = plt.subplots()
        xr = np.arange(maxminRange.x.min-graph_step,maxminRange.x.max+graph_step,graph_step)
        for line in self.lines : 
            ax.plot(xr,line.f_numpy(xr))
            print(line.name)
        
        for dot in self.dots : 
            ax.annotate(dot.name,dot.coord.getArrayLike())
            ax.plot(dot.coord.x,dot.coord.y, "r.")
        
        for polygon in self.polygons:
            for i in range(0,len(polygon.dots)):
                ax.annotate( str(float('%.2f' % (polygon.angles[i]*180/math.pi))),(polygon.dots[i].coord + polygon.angle_vision[i]).getArrayLike() )
        
        for angle in self.angles:
            ax.annotate( str(float('%.2f' % (angle.angle*180/math.pi))),(angle.dots[1].coord + angle.angle_vision).getArrayLike() )
        
        plt.show()
