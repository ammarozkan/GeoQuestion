import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import math

class Coordinate:
    def __init__(self,coordinates):
        self.x,self.y = coordinates[0],coordinates[1]
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
    def distance_by(self,another_coordinate):
        return math.sqrt((another_coordinate.x-self.x)**2+(another_coordinate.y-self.y)**2)
    def getArr(self):
        return [self.x,self.y]

class Dot:
    def __init__(self,coordinate,name):
        self.coord = Coordinate(coordinate)
        self.name = name
    
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
        return ("{"+self.name+":"+str(self.coord.getArr())+"}")
    
    def distance_by(self,another_dot):
        return self.coord.distance_by(another_dot.coord)

    def put_me_to_there(self,ax,coordinate_pass):
        draw_coordinate = self.coord + coordinate_pass

class Triangle:
    def __init__(self, dots,angles,angle_lookings):
        self.dots,self.angles = dots,angles
        self.angle_lookings = angle_lookings # a vector for writing a bit side, an array. each element for each angle
    def get_angle(self,dotId):
        dotarray  = [0,1,2].remove(dotId)
        a = self.dots[dotId].distance_by(self.dots[dotarray[0]])
        c = self.dots[dotId].distance_by(self.dots[dotarray[1]])
        b = self.dots[dotarray[0]].distance_by(self.dots[dotarray[1]])
        return math.acos((a**2+c**2-b**2)/(2*a*c))

class Angle:
    def __init__(self, dots, angle, angle_looking):
        self.dots, self.angle, self.angle_looking = dots, angle, angle_looking

VAR_DISTANCE,VAR_ANGLE = 0,1
class Variable:
    def __init__(self,var_type,data):
        self.var_type, self.data = var_type, data
 
def needity_function(xv):
    return np.cos(np.power(np.abs(xv/10),1/5))+1

def get_function(min,max,function=lambda x : x,g=50, no = []):
    xv = np.linspace(min, max, g) # Generates 30 points between 0 and 4
    yv = function(xv)  # Vector evaluation, sqrt() is applied to each point in xv

    plt.plot(xv, yv, 'b--')
    plt.show()

def get_functions(min,max, functions = [lambda x : x],g=1, no = [],names = []):
    fig, ax = plt.subplots()
    xv = np.arange(min,max,g)
    for func in functions: ax.plot(xv,func(xv))
    if names != [] : ax.set_title(names)

def getRS3():
    return math.tan((rnd.random()*(math.pi)))

def maxmin_from_coordinates(coords):
    max = [coords[0][0],coords[0][1]]
    min = [coords[0][0],coords[0][1]]
    for coord in coords:
        if coord[0] > max[0]: max[0] = coord[0]
        if coord[1] > max[1]: max[1] = coord[1]
        if coord[0] < min[0]: min[0] = coord[0]
        if coord[1] < min[1]: min[1] = coord[1]
        #print(coord)
    class maxmin:
        def __init__(self,max_a,min_a):
            class value:
                def __init__(self,max_a,min_a):
                    self.max, self.min = max_a, min_a
            self.x,self.y = value(max_a[0],min_a[0]),value(max_a[1],min_a[1])
    return maxmin(max,min)

def maxmin_from_dots(dots):
    if len(dots) > 0:
        max = Coordinate([dots[0].coord.x,dots[0].coord.y])
        min = Coordinate([dots[0].coord.x,dots[0].coord.y])
    else:
        max = Coordinate([5,5])
        min = Coordinate([-5,-5])
    for dot in dots:
        if dot.coord.x > max.x:max.x=dot.coord.x
        if dot.coord.y > max.y:max.y=dot.coord.y
        if dot.coord.x < min.x:min.x = dot.coord.x
        if dot.coord.y < min.y:min.y = dot.coord.y
    class maxmin:
        def __init__(self,max_a,min_a):
            class value:
                def __init__(self,max_a,min_a):
                    self.max, self.min = max_a, min_a
            self.x,self.y = value(max_a.x,min_a.x),value(max_a.y,min_a.y)
    return maxmin(max,min)


def getGeometry(k,c,cuts,cut_names,triangles,angle_objects):
    # random things
    #print(k)

    #print("cuts in ",len(cuts)," place at ",cuts)

    # drawing triangle
    maxmin = maxmin_from_dots(cuts)
    fig, ax = plt.subplots()
    xv  = np.arange(maxmin.x.min-1, maxmin.x.max+1, 0.1)
    yv = [k[x]*xv+c[x] for x in range(0,len(k))]
    for x in range(0,len(k)) : ax.plot(xv,yv[x],(["r","g","b","c","m","y","k"][x] if x < 7 else "p")+"-")
    for i in range(0,len(cuts)) : 
        ax.annotate(cuts[i].name,[ cuts[i].coord.x, cuts[i].coord.y ])
        ax.plot(cuts[i].coord.x, cuts[i].coord.y ,"r.")
    for triangle in triangles : 
        for i in range(0,len(triangle.dots)):
            ax.annotate(str(float('%.2f' % (triangle.angles[i]*180/math.pi))),[ triangle.dots[i].coord.x + triangle.angle_lookings[i].x, triangle.dots[i].coord.y + triangle.angle_lookings[i].y ])
    for angle in angle_objects:
        ax.annotate(str(float('%.2f' % (angle.angle*180/math.pi))),[ angle.dots[1].coord.x + angle.angle_looking.x, angle.dots[1].coord.y + angle.angle_looking.y ])

    #print([str(cuts[x]) for x in range(0,len(cuts))])
    plt.show()

def orderDotsByTriangle(dots):
    global upright,downleft,middle
    upright = dots[0]
    downleft = dots[0]
    middle = dots[0]
    for dot in dots:
        if dot.coord.y > upright.coord.y or (dot.coord.y == upright.coord.y and dot.coord.x > upright.coord.x): 
            middle = upright
            upright = dot
        elif dot.coord.y < downleft.coord.y or (dot.coord.y == downleft.coord.y and dot.coord.x < downleft.coord.x): 
            middle = downleft
            downleft = dot
        else: middle = dot
    return [upright,middle,downleft]

def findAName(pubName,names):
    counter = 1
    while pubName+str(counter) in names: counter+=1
    return pubName+str(counter)

intersect_lines = lambda k1,c1,k2,c2, dot_name : Dot( ( (c1-c2)/(k2-k1),(k2*c1-k1*c2)/(k2-k1) ), dot_name)

def read(filepath):
    with open(filepath) as f:
        lines = [line for line in f]
    k = []
    c = []
    line_name = []
    def FLBN(name): # find line by name
        for x in range(0,len(line_name)):
            if line_name[x] == name: return x
        print("Not found '",name,"'")
        return -1
    cut_names = [] #[l1,l2,name]
    def FPBN(name): # find point by name
        for x in range(0,len(cut_names)):
            if cut_names[x][2] == name: return x
        print("Not found '",name,"'")
        return -1
    work = []

    cuts = []
    def getCutByName(name):
        for cut in cuts:
            if cut.name == name: return cut
        else: return Dot((0,0),"NULL")
    cutted_lines = []
    def getCuttedLinesByDotName(name):
        for x in range(0,len(cuts)):
            if cuts[x].name == name: return cutted_lines[x]
        else: return [-1,-1]
    def compose():
        for a in range(0,len(line_name)):
            for b in range(0,len(line_name)):
                if a == b or (a,b) in cutted_lines or (b,a) in cutted_lines: continue
                else: 
                    #cuts.append( ( (c[a]-c[b])/(k[b]-k[a]),(k[b]*c[a]-k[a]*c[b])/(k[b]-k[a]) ) )
                    for cut_name in cut_names:
                        if (cut_name[0] == a and cut_name[1] == b) or (cut_name[0] == b and cut_name[1] == a) : 
                            dot_name = cut_name[2]
                            if k[a] != k[b]:cuts.append(intersect_lines(k[a],c[a],k[b],c[b],dot_name))
                            cutted_lines.append((a,b))

    triangles = []
    angle_objects = []
    def getTriangleByName(name):
        pass
    
    variables = []
    def calculateVariable(line):
        equalityParse = line.split('=')


    counter = 0
    while counter < len(lines):
        line = lines[counter][:len(lines[counter])-1].split(' ')
        #print("R:",line," Counter:",counter)
        if line[0] == "line":
            if len(line) == 2 : 
                k.append(getRS3())
                c.append(rnd.randint(-10,10))
                line_name.append(line[1])
            elif len(line) == 4 :
                if line[2] == "parallel": 
                    k.append(k[FLBN(line[3])])
                    c.append(rnd.randint(-10,10))
                    line_name.append(line[1])
                elif line[2] == "k":
                    k.append(float(line[3]))
                    c.append(rnd.randint(-10,10))
                    line_name.append(line[1])
        elif line[0] == "compose": 
            compose()
        elif line[0] == "figure":
            getGeometry(k,c,cuts,cut_names,triangles,angle_objects)
        elif line[0] == "rerandom":
            counter=0
            line_name=[]
            k=[]
            c=[]
            cut_names=[]
            cuts=[]
            cutted_lines=[]
            triangles=[]
            continue
        else:
            if line[1] == "cut":
                cut_names.append([FLBN(line[0]),FLBN(line[2]), line[3]])
            elif "=" in lines[counter][:len(lines[counter])-1]:
                calculateVariable(lines[counter][:len(lines[counter])-1])
            elif len(line) == 2 and line[1] == "triangle":
                triangle_dots = line[0].split(",")
                #triangle_dots = [ getCutByName(triangle_dots[x]) for x in range(0,len(triangle_dots)) ] --->>>
                triangle_dots = orderDotsByTriangle( [ getCutByName(triangle_dots[x]) for x in range(0,len(triangle_dots)) ] ) # [en ust - en sag, orta, en alt - en sol]
                #print("upright:",triangle_dots[0],"middle:",triangle_dots[1],"downleft:",triangle_dots[2])
                triangle_lines = [getCuttedLinesByDotName(triangle_dots[x].name) for x in range(0,len(triangle_dots))]

                
                easyatan = lambda kk : math.pi-math.atan(kk*-1) if kk < 0 else math.atan(kk)

                angles = [0,0,0]
                for x in range(0,len(triangle_lines)):
                    angles[x] = abs( easyatan( k[triangle_lines[x][0]] ) - easyatan( k[triangle_lines[x][1]] ) )
                    if x == 1: angles[x] = math.pi-angles[1]
                def nameit(dots):
                    t = ""
                    for dot in dots: t+=dot.name
                    return t
                print("Triangle Defined:"+nameit(triangle_dots)+", Angles in Rad:"+str(angles))
                
                d1 = triangle_dots[0].distance_by(triangle_dots[1])
                d2 = triangle_dots[0].distance_by(triangle_dots[2])
                alf = angles[0]
                area_of_triangle = d1*d2*math.sin(alf)*0.5

                # incenter calculation for angle looking requirement
                bisector_angle = lambda angleId : (math.pi/2 if angleId == 1 else 0)+(easyatan(k[triangle_lines[angleId][0]])+easyatan(k[triangle_lines[angleId][1]]))/2
                k1, k2 = math.tan(bisector_angle(0)),math.tan(bisector_angle(1))
                c1, c2 = triangle_dots[0].coord.y-k1*triangle_dots[0].coord.x,triangle_dots[1].coord.y-k2*triangle_dots[1].coord.x
                incenter_point = intersect_lines(k1,c1,k2,c2,"IncenterOf"+nameit(triangle_dots))
                cuts.append(incenter_point)
                
                def getALooking2(angleId):
                    return Coordinate(((incenter_point.coord.x-triangle_dots[angleId].coord.x)/3,(incenter_point.coord.y-triangle_dots[angleId].coord.y)/3))
                
                triangleObject = Triangle( triangle_dots, angles, angle_lookings=[getALooking2(0),getALooking2(1),getALooking2(2)] ) # angle lookings should be setted up by line crossing
                triangles.append(triangleObject)

            elif len(line) == 2 and line[1] == "angle":
                angle_dots = line[0].split(",")
                angle_dots = [ getCutByName(angle_dots[x]) for x in range(0,len(angle_dots)) ]
                order =  orderDotsByTriangle( angle_dots ).index(angle_dots[1])
                #print("upright:",triangle_dots[0],"middle:",triangle_dots[1],"downleft:",triangle_dots[2])
                angle_lines = getCuttedLinesByDotName(angle_dots[1].name)

                
                easyatan = lambda kk : math.pi-math.atan(kk*-1) if kk < 0 else math.atan(kk)

                angle = abs( easyatan( k[angle_lines[0]] ) - easyatan( k[angle_lines[1]] ) )
                if order == 1:angle = math.pi-angle
                def nameit(dots):
                    t = ""
                    for dot in dots: t+=dot.name
                    return t
                print("Angle Defined:"+nameit(angle_dots)+", Angle in Rad:"+str(angle))

                # incenter calculation for angle looking requirement

                looking = ((angle_dots[0].coord+angle_dots[2].coord)/2)-angle_dots[1].coord
                angle_objects.append(Angle(angle_dots,angle,(looking)/3))

                
                



                
        counter+=1






def function_test():
    fig, ax = plt.subplots()
    xv  = np.arange(-10, 10, 0.1)
    yv = 1/(np.power(np.cos(xv),2))
    y2v = np.tan(xv)
    ax.plot(xv,yv,xv,y2v,"b-")
    plt.show()

def test():
    read("language.txt")
    #getGeometry()
    #function_test()

