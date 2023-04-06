# GeoQuestion
The thing that calculates geometric things with line methods. You can generate geometric images and see result of calculations with that. Or you can just see with matplotlib library. Your choice.

## Style of Page
I used '[]' for showing empty thing that will be filled by user. I think this is a good and quick method.

* [Object(Type)] or [O(Type)] = User will be fill it with the name of an object of the type written in parantheses.
* [A,B,2,G] = User will be fill it with A or B or 2 or G. It can be filled with anything written in it.
* Or mathematical expression like [a ∈ Z] = User will be fill it with anything that can be putted in a.

## General Use

You can use that library with just only a python code. Or you can create a geometric language reader with python code easily. For general use, I recommend to create a basic code reader. For that:

```python
import GeoQuestion
languageReader = GeoQuestion.GeometricLanguager("Basic_Application")
languageReader.read_file("thefile.gml")
```

This basic code generates a reader named ```languageReader``` with project name ```Basic_Application``` . Then it reads file named ```thefile.gml```. 
After reading, you can easily see the progress.

```python
languageReader.plane.to_graph()
```

### Wait a minute, what is that .gml file?

That file is an geometric language file. (Not an gamemaker language file!) 

In example:

```
line -> name:d1
line -> name:d1p, c:2, parallel:d1
line -> name:d2
line -> name:d2p, c:2, parallel:d2
line -> name:d3
dot -> name:AA, cut:d1;d2
dot -> name:AB, cut:d1p;d2
dot -> name:BA, cut:d2p;d1
dot -> name:BB, cut:d2p;d1p
dot -> name:C, cut:d1;d3
dot -> name:D, cut:d2;d3
```

In that example, the code defines 5 lines and 6 dots by intersecting those lines. Lines named d1p and d2p is parallel to lines named d1 and d2.
And they has a constant c as 2. (f(x) = kx + c)
You can understand that language easily by looking once actually.

### Geometric Language

If you did look at the example up of this sentence, you can see some similarities between that definings. In a short presentation:

```
[The Type of Thing That Defined] -> Properties
```
Lets understand defining an object. 

#### Defining a Variable

The system uses lines for calculations. So if you are trying to define a dot, you should define minimum 2 lines firstly.
And then, you can intersect those lines for creation of an dot. Or you can use 3 lines for 3 dots.
Then, you can use those dots for creating a polygon. And thats it. But for defining a thing, you should know more about properties.

Properties, is the key of setting things to what you want to. For use of properties, just use '->' after object's type. 
For setting a property to something, you just write property's name after '->' and type ':' for mention that "I'm setting my property now.".
And then, write your setting. If you want to add another property, you can seperate your properties with comma. In example:

```
line -> name:patatoline,parallel:aline
```

In that example, we defined a parallel line to "aline" named "patatoline". Thats easy isn't it?

Do a quick look to that table: 

| Type of Object | Properties        |
| -------------- |:-----------------:|
| line           | name,c,parallel   |
| dot            | name,cut          |
| polygon        | name,dots         |
| triangle       | name,dots         |
| variable       | name,visible      |

You can see different types of objects has different types of properties. Not a lot, but a difference.

##### "Uses of Properties" Table
| Property       | Explanation                                                             | Use                                    |
| -------------- |:-----------------------------------------------------------------------:|:--------------------------------------:|
| name           | Name of Object                                                          | name:nameofobject                      |
| c              | Constant for line  (You can understand by looking at that f(x):kx + c)  | c:[a ∈ Z]                              |
| parallel       | For paralleling to another line                                         | parallel:[Object(Line)]                |
| cut            | For defining a dot intersecting by lines                                | cut:[O(Line)];[O(Line)]                |
| dots           | For defining a polygon by dots                                          | dots:[O(Dot)];[O(Dot)];[O(Dot)]        |
| visible        | Visibility of an variable (you will understand why is that here later.) | visible:[yes,no]                       |

#### Variables

Variables is not for drawing or calculating something. It just exists because it is necessary for getting any result from calculation that is a number.
In example if you want to get length between dots, you should define a variable. And then log that variable for seeing it. But non visible variables will
not be printed in the log. But they are exists as variable. You can reach them from your language reader python code.

General style of defining a variable:

```
variable -> properties
```

We should mention that, "What is our variable? What should the program put there?". 
So we add a second '->', I call it super properties, and then say what is should be setted as variable to program.
For using and understanding super properties, you should read the section next to this section.
Because, super properties has a lot application areas. When you understood super properties, you can create a variable on your own.

#### Super Properties
Do you want to define a line that bisector of an triangle? Or do you want to know length between dots? BOOM, super properties here for that!

Look quickly:

```
triangle -> name:t1, dots:A;B;C
line -> name:patatoline -> t1's bisector A
```
That code defines a line that is a bisector of ``` t1 ``` from dot ``` A ``` named ``` patatoline ```
Super properties not like properties. You can use super properties like you are just building a sentence. (Not exact that, but similar.)
Just add an extra '->' to the line and write your super property.

##### "Uses of Super Properties" Table
| Property       | Used At  | Explanation                                                             | Use                                          |
| -------------- |:--------:|:-----------------------------------------------------------------------:|:--------------------------------------------:|
| Bisector       | Line     | Bisector of an Polygon from an Dot.                                     | [Object(Polygon)]'s bisector [Object(Dot)]   |
| Area           | Variable | Area of an Triangle. (Just Triangle for now)                            | [Object(Triangle)]'s area                    |
| Length         | Variable | Length between dots.                                                    | lengthof [Object(Dot)] [Object(Dot)]         |

Super Properties is only way of getting and using information. (You can see, they are being uniquely suited to variables.)

> For a good variable, you should use super properties. Because, super properties is only way of getting and using information.

#### "Next" Commands
"Next" commands is here for logging, graphing, cleaning, rereading and reading another file with not touching any python code.

Let's see all of em!

* next
  * is
    * graphing             = Shows a graph of your geometric thing with matplotlib.
    * log                  = Logs all of your content to terminal. Included variables that visible.
    * clear                = Removes all objects. Or you can say it doin' like "cleaning the screen"
    * reread               = This is most complicated command in that language. I'll tell more about that at down.
  * to [File Name]         = Reads the file named [File Name]

Example use:
```
next is clear
next is log
next to secondfile.gml
```

##### About reread command
```
next is reread [Target File] n
```
If reader sees ``` reread ``` command at a code, reader stops reading that file. And reads the target file ``` n ``` times. 
And continues to read the first file.

I hope I add a command for printing the graph to a image file. That thing exists in the GeoQuestion library, but not in the geometric language.

### After Reading

Let's return to python code. Let's say we have that command for file reading.

```python
import GeoQuestion

languageReader = GeoQuestion.GeometricLanguager("Basic_Application",True,True)
languageReader.read_file("thefile.gml")
```
After reading, we have plane object in ```languageReader```.  With that object, we can graph it, edit it or print it to an image.
For graphing:
```python
languageReader.plane.to_graph()
```

For printing to a file, an imager should be defined:
```python
imager = GeoQuestion.GeometricImager()
```

This imager will print our plane object to a image file. For that:
```python
img = imager.Draw(languageReader.plane)
```

We got our image. That image created with PILLOW library. So we can use ```python img.show()``` for seeing the image.
```python
img.show()
```

Or we can create a image with variables. That will look like an geometry question.

```python
img = imager.DrawWithVariables(languageReader.plane,langueageReader.variables)
```

An example of a image created with ```python imager.DrawWithVariables()```
![ShapesImageExample](/exampleimages_variables/2023-03-26RealNonsizedEnormousShapes1.jpg)

### Printing to a Image File

Hooooo! We can specify our styling modifications too. For that, we use imager.

You can define your geometric imager with your modifications. Or you can set your modifications after defining your imager.

An example for setting modifications while defining:
```python
imager = GeoQuestion.GeometricImager(fontSize=25,lineWidth=10,modifyToRealistic=True)
```
Same example but setting modifications after defining:
```python
imager = GeoQuestion.GeometricImager()
imager.fontSize  = 25
imager.lineWidth = 10
imager.modifyToRealistic = True
```
All modifications you can make:

| Modifications               | Changes What?                                          | Values                                                             |
| --------------------------- |:------------------------------------------------------:|:------------------------------------------------------------------:|
| w                           | Width of Image                                         | An integer value that can be a width of an image.                  |
| h                           | Heigth of Image                                        | An integer value that can be a heigth of an image.                 |
| dotSize                     | Dot's Visual Circle Size                               | Diameter of circle So can be a float value for a diameter.         |
| fontSize                    | Font Size of Texts in Image                            | Just a font size. So can be an integer that bigger than 0          |
| lineWidth                   | Thickness of Lines                                     | A float value. I called it lineWidth because it works like width.  |
| variableMargin              | Changes Margin in Variable Segment Like CSS            | Takes a tuple that contains (xmargin, ymargin). It so cooooooollu  |
| spacesBetweenVariables      | Spaces Between Variables as Pixels                     | Just an integer. That will change pixel space between variables.   |
| roundToDigits               | Rounds to the Desired Number of Digits After the Point | Integer. How many digits you want after dot?                       |
| modifyToRealistic           | Drawing Shapes for According to Realistic Sizes        | True or False. If True, imager will draw realisticly. Else wont.   |
| onesizeAnglePos             | If True, Imager will text the deegre to a coordinate that distance with dot is a constant. Else just text it to between bisector of triangle and the dot.        | True or False.   |
| anglei_distance             | For onesizeAnglePos = True, You Can Change the Distance Constant        | The distance dude. Float...   |
| line_color                  | Line's Color                                           | Just tuple like (R,G,B)                                            |
| dot_color                   | Dot's Color                                            | Just tuple like (R,G,B)                                            |
| text_color                  | Text's Color                                           | Just tuple like (R,G,B)                                            |
| background_color            | Background's Color                                     | Just tuple like (R,G,B)                                            |
| font_name                   | Text's Font                                            | Just string as font's name in system.                              |
> (they are more actually, I'll write rest of them later.)


An example that shows what you can do with that:

```python
import GeoQuestion

languageReader = GeoQuestion.GeometricLanguager("Basic_Application",True,True)
languageReader.read_file("thefile.gml")

imager = GeoQuestion.GeometricImager(fontSize=25,lineWidth=10)
img = imager.Draw(languageReader.plane)
imager.lineWidth=25
img_withbiggerlines = imager.Draw(languageReader.plane)
```








