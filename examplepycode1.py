import GeoQuestion
languageReader = GeoQuestion.GeometricLanguager("Basic_Application",True,True)
languageReader.read_file("file.gml")
languageReader.plane.to_graph()

imager = GeoQuestion.GeometricImager(fontSize = 25,anglei_distance = 30)
img = imager.Draw(languageReader.plane)
img.show()
