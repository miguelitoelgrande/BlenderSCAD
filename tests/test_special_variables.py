# BlenderSCAD Tests
# Just a bunch of demos and test cases.
# by Michael Mlivoncic, 2013
#

# if your blenderscad is NOT in the Blender module dir...
#  ( <path>/blender-2.69-windows64/2.69/scripts/modules/blenderscad)
# change this line to where your blenderscad is located (as a subdir)
import sys
sys.path.append("O:/BlenderStuff") 
#from blenderscad.shapes import *

from mathutils import Vector


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
##############################


blenderscad.fa=20
## cylinder(h = 1, r=1, r1 = -1, r2 = -1, center = False, d=-1, d1=-1, d2=-1,   fn=0, fs=1, fa=12)
#o=cylinder(d=30,h=30,fn=3)
#o=sphere(20,fs=1)
#o=sphere(20,fn=5)
o=sphere(20,fa=90)

# simple polygon without explicit "path"
#o=translate([80,10,0],polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] , fill=True))
# triangle with two triangular holes...
#o=translate([20,0,0],polygon(points=[[0,0],[100,0],[0,100],[5,5],[30,5],[5,30],[25,25],[25,60],[60,25]], paths=[[3,4,5],[0,1,2],[6,7,8]], fill=true))
# "Fish"
#o=polygon(points=[[0,0],[100,0],[0,100],[5,5],[40,5],[5,40],[45,45],[45,80],[80,45]], paths=[[3,4,5],[0,1,2],[6,7,8]])
#o=linear_extrude(30,o)
#o=rotate_extrude (o,fn=300)
#o=rotate_extrude (o,fa=8)
#o=blenderscad.core.dissolve(o)
##########################################################################

print("num vertices: "+str(len(o.data.vertices)))
print("num polygons: "+str(len(o.data.polygons)))
# blenderscad.core.dissolve(o)
# print("num vertices: "+str(len(o.data.vertices)))
# print("num polygons: "+str(len(o.data.polygons)))
# blenderscad.core.decimate(o)
# print("num vertices: "+str(len(o.data.vertices)))
# print("num polygons: "+str(len(o.data.polygons)))
# #blenderscad.core.remesh(o)


##########################################################################

color(rands(0.0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)
