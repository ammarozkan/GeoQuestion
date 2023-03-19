from PIL import Image, ImageDraw, ImageFont
from .variables import Plane
from math import sqrt,pi

def Draw(w,h,plane,dotSize = 5,fontSize = 16,realisticSize = False,onesizeAnglePos=True,title="EnormousShapes",font_name="Hack-Regular.ttf",anglei_distance=None):
    if anglei_distance == None: anglei_distance = sqrt(w**2+h**2)/50
    img = Image.new("RGB", (w, h))
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
        drawer.line([(0,yi(ymin)),(w,yi(ymax))], fill="red",width = 2)

    for dot in plane.dots:
        x,y = xi(dot.coord.x), yi(dot.coord.y)
        start = (x-dotSize,y-dotSize)
        stop = (x+dotSize,y+dotSize)
        drawer.ellipse([start,stop],fill=(255,0,0))
        drawer.text((x,y-2),dot.name, fill=(255,255,255),font=font)

    for polygon in plane.polygons:
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
            drawer.text((x,y), anglestring, fill=(255,255,255),font=font)

    drawer.text((10,10),title,fill=(255,255,255),font=font)


    return img
