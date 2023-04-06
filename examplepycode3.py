import GeoQuestion
from datetime import date
today = date.today()


imager = GeoQuestion.GeometricImager(1280,720,fontSize=36,variableMargin=(50,15),spacesBetweenVariables=15,roundToDigits=2)

'''
imager.background_color = (255,255,255)
imager.text_color = (0,0,0)
imager.line_color = (175,20,20)
imager.dot_color = (75,0,0)
'''

def spec(name,realisticSize = False,onesizeAnglePos = False):
    for i in range(0,2):
        languageReader = GeoQuestion.GeometricLanguager("Basic_Application")
        languageReader.read_file("basic_image_stuff.gml")
        title = str(today)+name+"EnormousShapes"+str(i)

        imager.realisticSize = realisticSize
        imager.onesizeAnglePos = onesizeAnglePos

        img = imager.DrawWithVariables(languageReader.plane,languageReader.variables,title)
        img.save("exampleimages_variables/"+title+".jpg")

spec("RealOnesized",True,True)
spec("NonrealOnesized",False,True)
spec("RealNonsized",True,False)
spec("NonrealNonsized",False,False)
