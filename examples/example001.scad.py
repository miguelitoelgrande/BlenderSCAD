# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 

from mathutils import Vector  # using Vector type below...

import blenderscad 
from blenderscad import *  # contains blenderscad core, primitives, math and colors

## Clear the open .blend file!!!
#clearAllObjects()

## ------------------------------------------


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


