import GeoQuestion

for i in range(0,25):
    languageReader = GeoQuestion.GeometricLanguager("Basic_Application")
    languageReader.read_file("basic_image_stuff.gml")
    img = GeoQuestion.Draw(1200,800,languageReader.plane,realisticSize=True)
    img.save("exampleimages/testimg"+str(i)+".jpg")
