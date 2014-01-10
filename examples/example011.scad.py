# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 


import blenderscad 

# import imp
# imp.reload(blenderscad)
# imp.reload(blenderscad.core)
# imp.reload(blenderscad.primitives)

blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
#clearAllObjects()

###### End of Header ##############################################################################




polyhedron(
points = [
[10, 0, 0],
[0, 10, 0],
[-10, 0, 0],
[0, -10, 0],
[0, 0, 10]
],
triangles = [
[0, 1, 2, 3],
[4, 1, 0],
[4, 2, 1],
[4, 3, 2],
[4, 0, 3]
]
)


	
###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)


