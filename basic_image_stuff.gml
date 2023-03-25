line -> name:d1
line -> name:d2
line -> name:d3
dot -> name:A, cut:d1;d2
dot -> name:B, cut:d2;d3
dot -> name:C, cut:d1;d3
triangle -> name:t1, dots:A;B;C
line -> name:Abisectort1 -> t1's bisector A
line -> name:Bbisectort1 -> t1's bisector B
line -> name:Cbisectort1 -> t1's bisector C
variable -> name:areaoft1,visible:yes -> t1's area
variable -> name:distanceofAB,visible:yes -> lengthof A B
variable -> name:distanceofAC,visible:yes -> lengthof A C
next is log
end
