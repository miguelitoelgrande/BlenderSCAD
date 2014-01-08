# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 

from mathutils import Vector  # using Vector type below...

import blenderscad 
from blenderscad import *  # contains blenderscad core, primitives, math and colors

## Clear the open .blend file!!!
#clearAllObjects()

## ------------------------------------------

def example005():
	def sub():
		res=None
		for i in range (0,6):
			echo(360*i/6, sin(360*i/6)*80, cos(360*i/6)*80)
			o=translate([sin(360*i/6)*80, cos(360*i/6)*80, 0 ],
				cylinder(h = 200, r=10) )
			res=union(o,res)
		return res

	translate([0, 0, -120],
		union(	
	        difference(
	            cylinder(h = 50, r = 100)
	          , translate([0, 0, 10], cylinder(h = 50, r = 80) )
	          , translate([100, 0, 35], cube(50, center = true) )
	        )    
	        , sub() # need to factor the for loop out.
	        ,translate([0, 0, 200],
		        cylinder(h = 80, r1 = 120, r2 = 0) )
		)	        
     ) 

example005()

