from .variables import *
import random


class GeometricLanguager:
    def __init__(self, project_name):
        self.project_name = project_name
        self.plane = Plane()
        self.constant1 = (-10,10)
        self.constant2 = (-10,10)
        self.rereads = dict()
    
    def to_dict(self,string : str):
        variables = string.split(",")
        result = dict()
        for variable in variables:
            name, value = tuple(variable.split(":"))
            result[name] = value.split(";")
            result[name] = result[name][0] if len(result[name]) == 1 else result[name]
        return result
    
    def read_file(self,file_path):
        with open(file_path) as fp:
            Lines = fp.readlines()
        
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
                        print("you're doin' crazy things")
                        prop = line[2].split(" ")
                        if "'s" in prop[0]:
                            name = prop[0].replace("'s","")
                            #self.plane.find_object_by_name_(name,Triangle)
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

        if file_path in self.rereads and self.rereads[file_path] != 0:
            self.rereads[file_path] = self.rereads[file_path] - 1
            print("I seen, I should continue to reading my destiny... And I should do it ",self.rereads[file_path]," times at ",file_path,"...")
            self.read_file(file_path)
                        
    
    def show_result(self):
        self.plane.to_graph()
                            
        
        