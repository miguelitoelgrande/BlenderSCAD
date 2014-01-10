# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 

from mathutils import Vector  # using Vector type below...

import blenderscad 

blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
#clearAllObjects()

###### End of Header ##############################################################################

def example001():

	def r_from_dia(d):
		return (d / 2)
	
	def rotcy(rot, r, h):
		print([r,h])
		return rotate(90, rot,
			cylinder(r = r, h = h, center = true) )
		
	size = 50
	hole = 25		

	cy_r = r_from_dia(hole)
	cy_h = r_from_dia(size * 2.5)
		
	difference(
		sphere( r_from_dia(size) )
		, rotcy([0, 0, 0], cy_r, cy_h)
		, rotcy([1, 0, 0], cy_r, cy_h)
		, rotcy([0, 1, 0], cy_r, cy_h)
	)
	

example001()

###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)

