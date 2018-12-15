import functions
from functions import *


text = '''
read, read
x, identifier
;, ;
if, if
(, (
0, number
<, <
x, identifier
), )
then, then
fact, identifier
:=, :=
1, number
;, ;
repeat, repeat
fact, identifier
:=, :=
fact, identifier
*, *
x, identifier
;, ;
x, identifier
:=, :=
x, identifier
-, -
1, number
until, until
x, identifier
=, =
0, number
;, ;
write, write
fact, identifier
end, end
'''


tokens = [i.split(', ') for i in text.strip().split('\n')]
i = 0
functions.tokens = tokens 
functions.i = i
program()
