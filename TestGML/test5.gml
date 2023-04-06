next is clear
line -> name:d1,k:1,c:4
line -> name:d2,k:2,c:-12
line -> name:d3,k:-1,c:14
line -> name:d4,k:0,c:0
line -> name:d5,k:-2,c:4
dot -> name:A,cut:d4;d5
dot -> name:B,cut:d4;d2
dot -> name:C,cut:d2;d3
dot -> name:D,cut:d1;d3
dot -> name:E,cut:d1;d5
polygon -> name:p1,dots:A;B;C;D;E
end
