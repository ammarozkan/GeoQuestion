import GeoQuestion
from datetime import date
today = date.today()
def spec(name,realisticSize = False,onesizeAnglePos = False):
    for i in range(0,2):
        languageReader = GeoQuestion.GeometricLanguager("Basic_Application")
        languageReader.read_file("basic_image_stuff.gml")
        title = str(today)+name+"EnormousShapes"+str(i)
        img = GeoQuestion.DrawWithVariables(1280,720,languageReader.plane,languageReader.variables,fontSize=36,realisticSize=realisticSize,onesizeAnglePos=onesizeAnglePos,title=title,background_color=(255,255,255),text_color=(0,0,0),line_color=(175,20,20),dot_color=(75,0,0))
        img.save("exampleimages_variables/"+title+".jpg")

spec("RealOnesized",True,True)
spec("NonrealOnesized",False,True)
spec("RealNonsized",True,False)
spec("NonrealNonsized",False,False)
