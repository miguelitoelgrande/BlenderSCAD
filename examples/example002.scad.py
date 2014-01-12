# OpenSCAD example, ported by Michael Mlivoncic

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
#from blenderscad.shapes import *   # optional 

blenderscad.initns(globals()) # to avoid prefixing all calls, we make "aliases" in current namespace

## Clear the open .blend file!!!
clearAllObjects()


###############################
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("BEGIN", st)

###### End of Header ##############################################################################
blenderscad.fa=0.1;

def example002():

    intersection(
        blenderscad.core.difference(
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
			,apply=true
		)           
        , translate([0, 0, 5],
        cylinder(h = 50, r1 = 20, r2 = 5, center = true))       
	)	
    

example002()

# experimenting with dissolve to cleanup shape..
import bpy; o = bpy.context.scene.objects.active
o = blenderscad.core.dissolve(o)
#o= cleanup_object(o=o, quads=True)

###### Begin of Footer ##############################################################################

color(rands(0,1,3)) # random color last object. to see "FINISH" :-)


print("num vertices: "+str(len(o.data.vertices)))
print("num polygons: "+str(len(o.data.polygons)))


# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)

