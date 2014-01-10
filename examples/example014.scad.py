# OpenSCAD example, ported by Michael Mlivoncic
# a beautiful dice...
# an interesting test case, to get the Boolean operations somehow fixed (TODO)


#import sys
#sys.path.append("O:/BlenderStuff") 


import blenderscad 

import imp
imp.reload(blenderscad)
imp.reload(blenderscad.core)
imp.reload(blenderscad.primitives)


blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
clearAllObjects()

###### End of Header ##############################################################################

#OpenSCAD' intersection_for() is only a work around. As standard "for" implies a union of its content, this one is a combination of
# for() and intersection() statements.
# Not really needed as we currently do not support implicit union()'s, but to demonstrate, how it would be rewritten.
# see: http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Intersection_For_Loop


# intersection_for(i = [
# [0, 0, 0],
# [10, 20, 300],
# [200, 40, 57],
# [20, 88, 57]
# ])
# rotate(i) cube([100, 20, 20], center = true)

# example 2 - rotation:
#intersection_for(i = [ ]
tmp = None
rnge = [ [  0,  0,   0],
		[ 10, 20, 300],
		[200, 40,  57],
		[ 20, 88,  57] ]
for i in rnge:
	tmp = intersection(
		rotate(i ,
		cube([100, 20, 20], center = true))
		, tmp);


###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)


