from PIL import Image, ImageDraw, ImageFont
from .variables import Plane
from math import sqrt,pi

DEF_LINECOLOR = (255,0,0)
DEF_DOTCOLOR = DEF_LINECOLOR
DEF_TEXTCOLOR = (255,255,255)
DEF_BCKR = (0,0,0)

def Draw(w,h,plane,dotSize = 5,fontSize = 16,realisticSize = False,onesizeAnglePos=True,title="EnormousShapes",font_name="Hack-Regular.ttf",anglei_distance=None,draw_angles=True,line_color=DEF_LINECOLOR,dot_color=DEF_DOTCOLOR,text_color=DEF_TEXTCOLOR,background_color=DEF_BCKR,line_width=5):
    if anglei_distance == None: anglei_distance = sqrt(w**2+h**2)/50
    img = Image.new("RGB", (w, h),background_color)
    drawer = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_name,fontSize)
    dotRange = Plane.minimumRange(plane.dots)
    if realisticSize:
        rangeShould = max(dotRange.x.max - dotRange.x.min, dotRange.y.max - dotRange.y.min)
        xmid = (dotRange.x.max+dotRange.x.min)/2
        ymid = (dotRange.y.max+dotRange.y.min)/2
        
        dotRange.x.max = xmid+rangeShould/2
        dotRange.x.min = xmid-rangeShould/2
        dotRange.y.max = ymid+rangeShould/2
        dotRange.y.min = ymid-rangeShould/2

    xrange = (dotRange.x.max - dotRange.x.min)
    yrange = (dotRange.y.max - dotRange.y.min)
    dotRange.x.max += xrange/25
    dotRange.x.min -= xrange/25
    dotRange.y.max += yrange/25
    dotRange.y.min -= yrange/25

    xi = lambda x: (x - dotRange.x.min)*w/(dotRange.x.max - dotRange.x.min)
    yi = lambda y: (y - dotRange.y.min)*h/(dotRange.y.max - dotRange.y.min)
    
    
    for line in plane.lines:
        ymin, ymax = line.f(dotRange.x.min),line.f(dotRange.x.max)
        drawer.line([(0,yi(ymin)),(w,yi(ymax))], fill=line_color,width = line_width)

    for dot in plane.dots:
        x,y = xi(dot.coord.x), yi(dot.coord.y)
        start = (x-dotSize,y-dotSize)
        stop = (x+dotSize,y+dotSize)
        drawer.ellipse([start,stop],fill=dot_color)
        drawer.text((x,y-2),dot.name, fill=text_color,font=font)

    for polygon in plane.polygons:
        if draw_angles == True: 
            for i in range(0,len(polygon.dots)):
                x,y = None,None
                if onesizeAnglePos:
                    avy = polygon.angle_vision[i].y*(xrange/yrange)
                    avx = polygon.angle_vision[i].x
                    avx, avy = avx/sqrt(avx**2+avy**2),avy/sqrt(avx**2+avy**2)
                    x = xi(polygon.dots[i].coord.x) + anglei_distance*avx
                    y = yi(polygon.dots[i].coord.y) + anglei_distance*avy
                else:
                    x = xi(polygon.dots[i].coord.x + polygon.angle_vision[i].x)
                    y = yi(polygon.dots[i].coord.y + polygon.angle_vision[i].y)

                slope = abs(polygon.angle_vision[i].y/polygon.angle_vision[i].x)
                anglestring = "{:.2f}".format(polygon.angles[i]*180/pi)
                print(len(anglestring))
                x -= (fontSize*12/16)*len(anglestring)/2
                y -= (fontSize*12/16)/2
                drawer.text((x,y), anglestring, fill=text_color,font=font)

    drawer.text((10,10),title,fill=text_color,font=font)


    return img


def DrawWithVariables(w,h,plane,variables,dotSize = 5,fontSize = 16,realisticSize = False,onesizeAnglePos=True,title="EnormousShapes",font_name="Hack-Regular.ttf",anglei_distance=None,line_color=DEF_LINECOLOR,dot_color=DEF_DOTCOLOR,text_color=DEF_TEXTCOLOR,background_color=DEF_BCKR,line_width=5):
    geo_img = Draw(w,h,plane,dotSize,fontSize,realisticSize,onesizeAnglePos,title,font_name,anglei_distance,False,line_color,dot_color,text_color,background_color,line_width)
    w, h = geo_img.size
    variable_count = variables["^visible_count"]
    height_ofan_character = fontSize

    variable_image = Image.new("RGB",(w,variable_count*height_ofan_character),background_color)
    drawer = ImageDraw.Draw(variable_image)
    font = ImageFont.truetype(font_name,fontSize)

    area_notation = lambda name, value : "Area["+name+"] = "+str(value)
    distance_notation = lambda name, value : "|"+name+"| = "+str(value)

    counter = 0
    for varname in variables:
        if varname == "^visible_count" or variables[varname]["visibility"] != True:continue
        varType = variables[varname]["type"]
        notation = lambda name, value: str(name)+"="+str(value)
        if varType == "distance": notation = distance_notation
        elif varType == "area": notation = area_notation

        varstring = notation(variables[varname]["objectname"],variables[varname]["value"])
        drawer.text((0,counter*height_ofan_character),varstring,fill=text_color,font=font)
        counter+=1

    merged = Image.new("RGB",(w,h+variable_count*height_ofan_character))
    merged.paste(geo_img,(0,0))
    merged.paste(variable_image,(0,h))

    return merged

