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



# // example016.stl is derived from Mblock.stl
# // (c) 2009 Will Langford licensed under
# // the Creative Commons - GNU GPL license.
# // http://www.thingiverse.com/thing:753
# //
# // Jonas Pfeil converted the file to binary
# // STL and duplicated its content.

def blk1():
    return cube([ 65, 28, 28 ], center = true)
    

def blk2():
    return difference(
        translate([ 0, 0, 7.5 ],
			cube([ 60, 28, 14 ], center = true))
        , cube([ 8, 32, 32 ], center = true)
    )
    

def chop():
    return translate([ -14, 0, 0 ],
		import_(file = "example016.stl", convexity = 12))
    

#difference(
o1=blk1(); objs=[]
for alpha in [0, 90, 180, 270]:
	o= rotate(alpha, [ 1, 0, 0], # render(convexity = 12)
		difference(  blk2(),  chop() ))
	objs.append(o)
o=difference(o1,*objs)	
#)            
        
  

###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)
  


