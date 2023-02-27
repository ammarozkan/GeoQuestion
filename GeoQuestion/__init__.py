import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random as rnd

from .variables import Coordinate, Triangle,order_dots_by_OutAngleRule,Dot,Polygon,Function,Plane

def TestLibrary():
    
    our_plane = Plane()

    our_plane.add_object( Function([-2,0],"d1"),Function([-0.5,2],"d2"),Function([-4,-2],"d3") )
    our_plane.intersect_and_set("d1","d2","A")
    our_plane.intersect_and_set("d2","d3","B")
    our_plane.intersect_and_set("d1","d3","C")
    our_plane.define_polygon_("Patates Cipsi","A","B","C")
    our_plane.add_object(our_plane.polygons[0].bisector(0,1,2),our_plane.polygons[0].bisector(2,0,1),Dot.average_of_points(our_plane.dots))



    our_plane.to_graph()