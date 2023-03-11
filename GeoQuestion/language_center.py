from .variables import *
import random

class Finder:
    def __init__(self):
        self.founded_id = -1

    def find_by_name(self,array,name):
        for i in range(0,len(array)):
            if array[i].name == name:
                self.founded_id = i
                return True
    
    def find_by_name_plane(self,plane,name,obj_type):
        object_id = plane.find_object_by_name_(name,obj_type)
        if object_id != None:
            self.founded_id = object_id
            return True
        return False


class GeometricLanguager:
    def __init__(self, project_name):
        self.project_name = project_name
        self.plane = Plane()
        self.constant1 = (-10,10)
        self.constant2 = (-10,10)
        self.rereads = dict()

        self.finder = Finder()
        self.variables = dict()
    
    def to_dict(self,string : str):
        variables = string.split(",")
        result = dict()
        for variable in variables:
            name, value = tuple(variable.split(":"))
            result[name] = value.split(";")
            result[name] = result[name][0] if len(result[name]) == 1 else result[name]
        return result

    def convert_lyritic(self,string : str):
        string = string.lstrip().split(" ")
        belong_to  = False
        priv_value = False
        priv_segment = False
        commands = False
        if "'s" in string[0][-2:]:
            belong_to = string[0][0:-2]
            if len(string) > 1:
                priv_value = string[1]
            if len(string) > 2:
                priv_segment = string[2]
        else:
            commands = string
        return {"belong_to":belong_to,"priv_value":priv_value,"priv_segment":priv_segment,"commands":commands}


    
    def read_file(self,file_path):
        with open(file_path) as fp:
            Lines = fp.readlines()
            print("Reading File:",file_path)
        
        for line in Lines:
            if line[0:4] != "next" and line[0:3] != "end":
                line = line.replace("\n","").split("->")
                var_data = self.to_dict(line[1].replace(" ",""))
                #print(line)
                #print(var_data)
                if line[0].replace(" ","") == "line":
                    if "name" not in var_data:
                        print("If you defining a line, you should define with a name in it!")
                    elif len(line) == 3:
                        prop = line[2].lstrip().split(" ")
                        if "'s" in prop[0]:
                            print("calculating ", prop[0].replace("'s","")+"'s ",prop[1]," for ",prop[2])
                            object_name = prop[0].replace("'s","")
                            object_id = self.plane.find_object_by_name_( object_name,Polygon )
                            object = None
                            if object_id != None: object = self.plane.polygons[object_id]
                            if object == None:
                                print("There is not a polygon named "+object_name," can you check it?")
                            elif prop[1] == "median":
                                self.plane.add_object(object.median_line(object.getdotid(prop[2]),var_data["name"]),var_data["name"])
                            elif prop[1] == "prependicular":
                                self.plane.add_object(object.prependicular_line(object.getdotid(prop[2]),var_data["name"]),var_data["name"])
                            elif prop[1] == "bisector":
                                d2id = object.polygonStyleOrdered_ids.index(object.getdotid(prop[2]))
                                d1 = object.polygonStyleOrdered_ids[(d2id-1)%len(object.dots)]
                                d2 = object.polygonStyleOrdered_ids[d2id]
                                d3 = object.polygonStyleOrdered_ids[(d2id+1)%len(object.dots)]

                                self.plane.add_object(object.bisector(d1,d2,d3,var_data["name"]),var_data["name"])
                    else :
                        k = random.random()*(self.constant2[1]-self.constant2[0]) + self.constant2[0]
                        c = random.random()*(self.constant1[1]-self.constant1[0]) + self.constant1[0]
                        if "parallel" in var_data:
                            k = self.plane.lines[self.plane.find_object_by_name_(var_data["parallel"],Function)].const[1]
                        if "c" in var_data:
                            c = float(var_data["c"])
                        self.plane.add_object(Function([c,k],var_data["name"]))
                elif line[0].replace(" ","") == "dot":
                    if "name" not in var_data:
                        print("If you are defining a dot, you should define with a name in it!")
                    elif "cut" not in var_data or len(var_data["cut"]) != 2:
                        print("If you are defining a dot, you should define with 2 cuts in it!")
                    else:
                        f1 = self.plane.find_object_by_name_(var_data["cut"][0],Function)
                        f2 = self.plane.find_object_by_name_(var_data["cut"][1],Function)
                        self.plane.intersect_and_set(f1,f2,var_data["name"])
                elif line[0].replace(" ","") == "triangle":
                    if "name" not in var_data:
                        print("If you are defining a triangle, you should define with a name in it!")
                    elif "dots" not in var_data or len(var_data["dots"]) != 3:
                        print("If you are defining a triangle, you should define with 3 dots in it!")
                    else:
                        self.plane.define_polygon_(var_data["name"],True,*var_data["dots"])
                elif line[0].replace(" ","") == "variable":
                    lyritic = self.convert_lyritic(line[2])
                    if lyritic["belong_to"]:
                        if lyritic["priv_value"] and lyritic["priv_value"] == "area":
                            if self.finder.find_by_name_plane(self.plane,lyritic["belong_to"],Polygon):
                                self.variables[var_data["name"]] = self.plane.polygons[self.finder.founded_id].area()
                    elif lyritic["commands"]:
                        if lyritic["commands"][0] == "lengthof":
                            d_ids = [-1,-1]
                            for i in range(0,2):
                                if self.finder.find_by_name_plane(self.plane,lyritic["commands"][i+1],Dot):
                                    d_ids[i] = self.finder.founded_id
                            if -1 not in d_ids:
                                self.variables[var_data["name"]] = Dot.distance_of_points(self.plane.dots[d_ids[0]],self.plane.dots[d_ids[1]])



            else:
                line = line.replace("\n","").split(" ")
                if line[0] == "next":
                    if line[1] == "to":
                        self.read_file(line[2])
                    if line[1] == "is":
                        if line[2] == "reread":
                            if line[3] not in self.rereads: 
                                self.rereads[line[3]] = int(line[4])
                        elif line[2] == "graphing":
                            self.show_result()
                        elif line[2] == "clear":
                            self.plane.clear()
                        elif line[2] == "log":
                            print("LOG:\n",self.plane)
                            print("Variables:")
                            for var in self.variables:
                                print(var,":",self.variables[var])

        if file_path in self.rereads and self.rereads[file_path] != 0:
            self.rereads[file_path] = self.rereads[file_path] - 1
            print("I seen, I should continue to reading my destiny... And I should do it ",self.rereads[file_path]," times at ",file_path,"...")
            self.read_file(file_path)
                        
    
    def show_result(self):
        self.plane.to_graph()
                            
        
        
