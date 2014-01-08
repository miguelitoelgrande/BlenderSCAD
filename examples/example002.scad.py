# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 

from mathutils import Vector  # using Vector type below...

import blenderscad 
from blenderscad import *  # contains blenderscad core, primitives, math and colors

## Clear the open .blend file!!!
#clearAllObjects()

## ------------------------------------------

def example002():

    intersection(
        difference(
            union(
                cube([30, 30, 30], center = true)
                , translate([0, 0, -25],
					cube([15, 15, 50], center = true))
            )    
            , union(
                cube([50, 10, 10], center = true)
                , cube([10, 50, 10], center = true)
                , cube([10, 10, 50], center = true)
            )    
		)           
        , translate([0, 0, 5],
        cylinder(h = 50, r1 = 20, r2 = 5, center = true))       
	)	
    

example002()


