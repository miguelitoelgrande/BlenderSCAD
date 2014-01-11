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
 
# function get_cylinder_h(p) = lookup(p, [
# [ -200, 5 ],
# [ -50, 20 ],
# [ -20, 18 ],
# [ +80, 25 ],
# [ +150, 2 ]
# ])

# for (i = [-100:5:+100])
    # // echo(i, get_cylinder_h(i))
    # translate([ i, 0, -30 ]) cylinder(r1 = 6, r2 = 2, h = get_cylinder_h(i)*3)
	
def get_cylinder_h(p):
	return lookup(p, [
		[ -200, 5 ],
		[ -50, 20 ],
		[ -20, 18 ],
		[ +80, 25 ],
		[ +150, 2 ]
	])	
for i in range (-100, +100, 5):  # note: range increment is middle param in OpenSCAD, in python, it is the third param!!
	# echo(i, get_cylinder_h(i));
	translate([ i, 0, -30 ] , cylinder(r1 = 6, r2 = 2, h = get_cylinder_h(i)*3) )

###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)
 
    


