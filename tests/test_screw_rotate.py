# BlenderSCAD Tests
# Just a bunch of demos and test cases.
# by Michael Mlivoncic, 2013
#

# if your blenderscad is NOT in the Blender module dir...
#  ( <path>/blender-2.69-windows64/2.69/scripts/modules/blenderscad)
# change this line to where your blenderscad is located (as a subdir)
#import sys
#sys.path.append("O:/BlenderStuff") 
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
echo ("BEGIN ", st)
##############################



# Extra as Blender supports it: screw extrusion bpy.ops.mesh.screw()
# Extrude selected vertices in screw-shaped rotation around the cursor in indicated viewport 
def screw_extrude(steps, turns, o=None, fn=None, fs=None, fa=None):	
	#segments = fn if fn != -1 else blenderscad.fn # globals()["fn"]
	#print(segments)
	if o is None:
		o = bpy.context.object
	bpy.context.scene.objects.active = o
	o.select = True
	# therefore: X-Axis determines "radius" of the spin, but y will transform into height of resulting spin object
	newz = o.location[1] # z-Offset of the final object...
	o.location[1]=0.0	
	rotate([90,0,0],o ) # emulating OpenSCAD: assumes 2D object in X-Y-Plane...
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.ops.mesh.select_all(action="SELECT")		
	prevAreaType = bpy.context.area.type # TEXT_EDITOR or CONSOLE
	bpy.context.area.type = 'VIEW_3D' # probably: need to set cursor for Spin to be right...	
	#print(o.location)
	bpy.context.scene.cursor_location = o.location
	#o.location=(10,0,0)
	bpy.ops.view3d.viewnumpad(type='TOP')
	bpy.ops.view3d.snap_cursor_to_selected()
	#print (bpy.ops.mesh.spin.poll())	
    # params to emulate rotate_extrude of OpenSCAD, 2D object in XY plane
	bb=o.bound_box[4][0] # boundbox 8x<x,y,z>->( LoX,LoY,LoZ, LoX,LoY,HiZ, LoX,HiY,HiZ, LoX,HiY,LoZ, HiX,LoY,LoZ, HiX,LoY,HiZ, HiX,HiY,HiZ, HiX,HiY,LoZ ). 
	r = o.location[0] + bb  # outer radius of object.. X-location defines inner "hole", plus bound box outer in X direction..
	#print("boundBox"); print(bb); print("radius"); print(r);
	segments=blenderscad.core.get_fragments_from_r( r=r, fn=fn, fs=fs, fa=fa )
	angle = math.pi*2.0 #(360 * pi / 180) # ggrrr.. need to convert or debug for hours :-)
	#bpy.ops.mesh.spin(steps=segments, dupli=False, angle=angle, center=(0.0, 0.0, 0.0), axis=(0.0, 0.0, 1.0))
	bpy.ops.mesh.screw(steps=steps, turns=turns, center=(0.0, 0.0, 0.0), axis=(0.0, 0.0, 0.0))
	# if duplicate: delete original meshes... still selected.
	#bpy.ops.mesh.delete(type='VERT')	
	#bpy.ops.mesh.delete(type='EDGE')	
	bpy.ops.mesh.select_all(action='SELECT')	
	#bpy.ops.mesh.remove_doubles()	
	bpy.context.area.type = prevAreaType  	# restore area / context
	#bpy.ops.mesh.normals_make_consistent(inside=False)
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')	
	o.location[2] += newz
	o.name = 're('+o.name+')'
	o.data.name = 'le('+o.data.name+')'	
	#	o.data.materials.append(mat)
	#	o.color = blenderscad.defColor
	# TODO: need to cleanup the result
	#bpy.ops.mesh.flip_normals()  # blender treats normals the other way around than OpenSCAD...
	bpy.ops.object.mode_set(mode = 'EDIT')	
	bpy.ops.mesh.select_all(action="SELECT")	
	bpy.ops.mesh.normals_make_consistent(inside=False) #recalc normals on outside
	#mod1 = o.modifiers.new('Mod1', 'SOLIDIFY')	
	#bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Mod1')
	bpy.ops.object.mode_set(mode = 'OBJECT')	
	return o


	
	
blenderscad.fa=20
## cylinder(h = 1, r=1, r1 = -1, r2 = -1, center = False, d=-1, d1=-1, d2=-1,   fn=0, fs=1, fa=12)
#o=cylinder(d=30,h=30,fn=3)
#o=sphere(20,fs=1)
#o=sphere(20,fn=5)
#o=sphere(20,fa=90)

# simple polygon without explicit "path"
o=translate([10,5,0],polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] , fill=True))
# triangle with two triangular holes...
#o=translate([20,0,0],polygon(points=[[0,0],[100,0],[0,100],[5,5],[30,5],[5,30],[25,25],[25,60],[60,25]], paths=[[3,4,5],[0,1,2],[6,7,8]], fill=true))
# "Fish"
#o=polygon(points=[[0,0],[100,0],[0,100],[5,5],[40,5],[5,40],[45,45],[45,80],[80,45]], paths=[[3,4,5],[0,1,2],[6,7,8]])

#o=linear_extrude(30,o)
#o=rotate_extrude (o,fn=300)
o= blenderscad.core.screw_extrude(10,2,o)

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
echo ("FINISH ", st)
