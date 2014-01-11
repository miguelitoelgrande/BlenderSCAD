# OpenSCAD example, ported by Michael Mlivoncic
# a beautiful dice...
# an interesting test case, to get the Boolean operations somehow fixed (TODO)


#import sys
#sys.path.append("O:/BlenderStuff") 


import blenderscad 

# import imp
# imp.reload(blenderscad)
# imp.reload(blenderscad.core)
# imp.reload(blenderscad.primitives)


blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
clearAllObjects()

###### End of Header ##############################################################################


def step(l, mod, child):
	children=len(child)
	for i in range(0,children):
		translate([ l*(i - (children-1)/2), 0, 0 ], child[(i+mod) % children] )
	return group(child[0],*child[1:])
    

for i in range(1,5):  # 1..4
	# need to explicitly generate the child nodes as array first...
	objs=[]
	objs.append(sphere(30))
	objs.append(cube(60, true) )
	objs.append( cylinder(r = 30, h = 50, center = true) )
	objs.append(   
        union(
            cube(45, true)
            , rotate([45, 0, 0], cube(50, true) )
            , rotate([0, 45, 0], cube(50, true) )
            , rotate([0, 0, 45], cube(50, true) )
		))	
	translate([0, -250+i*100, 0], step(100, i, objs) )

###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)
  