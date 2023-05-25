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
| freepolygon    | name,dots         |
| triangle       | name,dots         |
| freetriangle   | name,dots         |
| variable       | name,visible      |

You can see different types of objects has different types of properties. Not a lot, but a difference.

#### Generally Object Specialities:

##### line
Just for defining a line, as a function or a equation. You say.
Generally a line creation happens randomly. But you can limit it. In example you can say it to be parallel to an another line. Or you can
set it constant to 5. In example if we want to set our line d2 parallel to d1 and that d2 should be like f:kx + 5

```
line -> name:d1,parallel:d2,c:5
```

Thats it.

##### dot
For defining a dot, you should specify 2 lines min. Because for defining a dot, we need lines to intersect. In example
we have lines named d1 and d2. And we want to define a dot with intersecting them. And name the dot with 'A' letter.

```
dot -> name:A,cut:d1;d2
```

##### polygon and triangle
For polygon, we should have 3 dots at least. If we have 3 dots, we can just define a triangle. Defining polygon and triangle is same.
Let's define a triangle named t1 and consisting of these A, B, C points

```
triangle -> name:t1,dots:A;B;C
```

And lets define polygon named p1 and consisting of these A, B, C, D, E points

```
polygon -> name:p1,dots:A;B;C;D;E
```
But I should mention that, defining a polygon from these dots is not easy. Because intersections from random lines not creates perfect
polygon.

##### freepolygon and freetriangle

At defining a polygon with dots that intersects from lines, this library uses lines for connecting dots. But sometimes
you maybe not have properly connected dots. In example:

```
"line -> name:d1",
"line -> name:d2",
"line -> name:d3",
"dot -> name:A, cut:d1;d2",
"dot -> name:B, cut:d2;d3",
"dot -> name:C, cut:d1;d3",
"triangle -> name:t1, dots:A;B;C",
"line -> name:f1 -> t1's bisector A",
"dot -> name:D, cut:f1;d3",
```

and then we want to define a triangle with A,C,D. But A is intersection between d1,d2 and D is intersection between f1,d3.
This library will look at these and say: "you can't define a triangle with them. They are not connected. I can only calculate
angles with connected lines." So for example like these , we can use freetriangle and freepolygon variables. These variables
are same as triangle and polygon variables but they don't need a connection. They create their connection by just looking to
dots.

For that example, we can use that piece of code:

```
freetriangle -> name:ft1, dots:A;C;D
```

##### variable

I'll tell more about them later.

#### "Uses of Properties" Table
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
| Angle          | Variable | Angle at any dot in polygon.                                            | [Object(Polygon)]'s angle [Object(Dot)]      |

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

| Modifications               | Changes What?                                           | Values                                                             |
| --------------------------- |:-------------------------------------------------------:|:------------------------------------------------------------------:|
| w                           | Width of Image                                          | An integer value that can be a width of an image.                  |
| h                           | Heigth of Image                                         | An integer value that can be a heigth of an image.                 |
| dotSize                     | Dot's Visual Circle Size                                | Diameter of circle So can be a float value for a diameter.         |
| fontSize                    | Font Size of Texts in Image                             | Just a font size. So can be an integer that bigger than 0          |
| lineWidth                   | Thickness of Lines                                      | A float value. I called it lineWidth because it works like width.  |
| variableMargin              | Changes Margin in Variable Segment Like CSS             | Takes a tuple that contains (xmargin, ymargin). It so cooooooollu  |
| rangec                      | Changes Empty Segment in Image (so its like margin yeah)| Takes a tuple that contains (xrangec, yrangec). Empty segment increases when value -> 0  |
| spacesBetweenVariables      | Spaces Between Variables as Pixels                      | Just an integer. That will change pixel space between variables.   |
| roundToDigits               | Rounds to the Desired Number of Digits After the Point  | Integer. How many digits you want after dot?                       |
| modifyToRealistic           | Drawing Shapes for According to Realistic Sizes         | True or False. If True, imager will draw realisticly. Else wont.   |
| onesizeAnglePos             | If True, Imager will text the deegre to a coordinate that distance with dot is a constant. Else just text it to between bisector of triangle and the dot.        | True or False.   |
| anglei_distance             | For onesizeAnglePos = True, You Can Change the Distance Constant        | The distance dude. Float...   |
| line_color                  | Line's Color                                            | Just tuple like (R,G,B)                                            |
| dot_color                   | Dot's Color                                             | Just tuple like (R,G,B)                                            |
| text_color                  | Text's Color                                            | Just tuple like (R,G,B)                                            |
| background_color            | Background's Color                                      | Just tuple like (R,G,B)                                            |
| font_name                   | Text's Font                                             | Just string as font's name in system.                              |
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


#### Deep Calculations

Damn dude. I had an trash like photo from this code. I cant even see the geometric shape!

And now, this sentence is almost impossible. Because, I did a system that calculates "beuty" of an generation.
For using "beuty calculator" you can directly use one of the calculator functions. In example this library
have a *"NE1_fixed"* function.


```python
import GeoQuestion

languageReader = GeoQuestion.GeometricLanguager("Basic_Application",False,False,False)
languageReader.read_file("thefile.gml")

while False in [NE1_fixed(polygon.dots) for polygon in GL.plane.polygons] or NE1_fixed(GL.plane.dots) == False:
            languageReader = GeometricLanguager("Basic_Application",False,False,False)
            languageReader.read_file("thefile.gml")
            print("I dont liked it.")

imager = GeoQuestion.GeometricImager(fontSize=25,lineWidth=10)
img = imager.Draw(languageReader.plane)
img.show()
```

In this example:
- a languageReader variable defined for reading from file to create shapes.
- a while loop that continues if a bad polygon in shape creation.
- as while loop continues, new shapes generated. again and again.
- If every polygon is detected beutiful by the *"NE1_fixed"* function, loop stops.
- And program draws image.

So, you can see in this code we have that *NE1_fixed* for controlling the shape is good or bad.
Mostly, beuty controlling functions, or algorithms, gets a list of dots and returns this list of dots
is beautiful or trashful. You can write an beuty controlling function too. But if you want to use
functions that already defined, you can use that functions:
- **NE1_fixed**: This function gets dots, calculates 2 lines that look like the list of dots. I think this is called 
linear regression in statistics. But why 2 lines? 1 for x to the y axis and 1 for y to the x axis function. And
from this 2 lines this functon calculates "how good is this lines for a geometric shape".
- **NE6**: This function gets dots too. But, for working with this function you will need a data. More data.
Why? Because this function gets the input dots, generates some values from these dots (like linear regression 
as mentioned in previous example or standart deviation of coordinates) and looks to the data. Looks to the database
for "which one data is closest to thıs new data" and then finds the closest one. And, if this closest one is a
good shape, this is a good shape, else this is not a good shape.


When I create new algorithms or new functions, I'll add them here. And **NE1_fixed** is my personally
favorite. Because,  *NE1_fixed* is fast, simple and more correct. But *NE6* is more correct if
enough data is given to it. But if this is didden to it, *NE6* will be working so slow.







