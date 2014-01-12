# Based on Projection Demo
#http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/3D_to_2D_Projection
# which is based on OpenSCAD example002()

# additional module path
#import sys
#sys.path.append("O:/BlenderStuff") 

from mathutils import Vector  # using Vector type below...


# This block helps during developmentas it reloads the blenderscad modules which are already present
# and may have changed...
# can be commented out or removed if you do not modify blenderscad libs during this blender session.
import imp; import sys
rel = ['blenderscad','blenderscad.math',
'blenderscad.core', 'blenderscad.primitives','blenderscad.impexp', 'blenderscad.shapes']
for mo in rel:
	if mo in sys.modules.keys():
		print ('reloading: '+mo+' -> '+ sys.modules[mo].__file__)
		imp.reload(sys.modules[mo])
########################

import blenderscad 

import bpy
#bpy.ops.wm.console_toggle()

blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
#clearAllObjects()

###### Timestamp ##############################################################################
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("BEGIN", st)
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
	
# uncomment the projection you want to see on the screen
	
#projection(cut = true, o=example002());
#projection(cut = false, o=example002());
#translate([0,0,25], rotate([90,0,0], example002()));
#projection( translate([0,0,25], rotate([90,0,0], example002())));
#translate([0,0,-6], rotate([90,0,0], example002()))
#dissolve( translate([0,0,-6], rotate([90,0,0], example002())) );
#o=projection(cut=true, o=translate([0,0,-6], rotate([90,0,0], example002())));
o=projection(cut=false, o=translate([0,0,-60], rotate([90,0,0], example002())));
#num vertices: 313
#num polygons: 207

#resize([20,20,0], o=translate([0,0,-6], rotate([90,0,0], example002())));
#linear_extrude(10,o)
#translate([0,0,-5], rotate([45,0,45], cube(20)))
#o=projection( cut=true, o=translate([0,0,-5], rotate([45,0,45], cube(20))));
#o=projection( cut=false, o=translate([0,0,-5], rotate([45,0,45], cube(20))));

linear_extrude(10,o)
#rotate_extrude(o)

#cube(20)

###### Begin of Footer ##############################################################################
color(rands(0.05, 1.00 , 3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)
