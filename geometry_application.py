import GeoQuestion
from datetime import date
today = date.today()
def spec(name,realisticSize = False,onesizeAnglePos = False):
    for i in range(0,5):
        languageReader = GeoQuestion.GeometricLanguager("Basic_Application")
        languageReader.read_file("basic_image_stuff.gml")
        title = str(today)+name+"EnormousShapes"+str(i)
        img = GeoQuestion.Draw(800,600,languageReader.plane,realisticSize=realisticSize,onesizeAnglePos=onesizeAnglePos,title=title)
        img.save("exampleimages/"+title+".jpg")

spec("RealOnesized",True,True)
spec("NonrealOnesized",False,True)
spec("RealNonsized",True,False)
spec("NonrealNonsized",False,False)
