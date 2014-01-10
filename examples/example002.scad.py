# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 

from mathutils import Vector  # using Vector type below...

import blenderscad 

blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
#clearAllObjects()

###### End of Header ##############################################################################

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

###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)

