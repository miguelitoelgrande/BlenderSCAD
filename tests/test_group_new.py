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
#from blenderscad.shapes import *	# optional 

blenderscad.initns(globals()) # to avoid prefixing all calls, we make "aliases" in current namespace

## Clear the open .blend file!!!
clearAllObjects()


###############################
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("BEGIN ", st)
##############################


# NO OpenSCAD thing, but nice alternative to union(). It preserves the objects and
# therefore different colors. However, need to rework subsequent modifiers?
# TODO: Should use obj.constraint("Copy Location")...  , "Copy Rotation", "Copy Scale" instead. Prob: Rotation around axis of target obj...
def group_old(o1,*objs):
	res = o1
	o1.select = True
	bpy.context.scene.objects.active = o1	
	for obj in objs:
		if obj != None:			
			obj.select = True
			#obj.hide_select = True
			#Keep Hierarchy selectable, but avoid transforming children independent of parent.
			obj.lock_location = (True,True,True)
			obj.lock_rotation = (True,True,True)
			obj.lock_scale	 = (True,True,True)
	bpy.ops.object.parent_set(type='OBJECT',keep_transform=True)	
	#bpy.ops.object.parent_clear(type='CLEAR_INVERSE')
	return res

import bpy

# NO OpenSCAD thing, but nice alternative to union(). It preserves the objects and
# therefore different colors. However, need to rework subsequent modifiers?
# TODO: Should use obj.constraint("Copy Location")...  , "Copy Rotation", "Copy Scale" instead. Prob: Rotation around axis of target obj...
#def group(o1,*objs):
#	res = o1
#	#creating a boundary box, similar to "empty", but using real box for "dimension" property...
#	bpy.ops.mesh.primitive_cube_add(location=(0.0,0.0,0.0), layers=blenderscad.mylayers)
#	if bpy.context.active_object.mode is not 'OBJECT': 
#		bpy.ops.object.mode_set(mode = 'OBJECT')
#	bb = bpy.context.active_object # bb ~ reference to this bounding box representing group
#	bb.data.materials.append(blenderscad.mat)
#	bb.draw_type='WIRE'
#	bb.hide_render=True
#	bb.name="group"
#	bb.data.name="bbox"
#
#	bpy.ops.object.select_all(action='DESELECT')	
#	o1.select = True
#	bpy.context.scene.objects.active = o1
#	#objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
#	objs=list(objs)
#	objs.append(o1)
#	#go through all formerly selected objects, we need the overall min/max in all three dims.
#	# location set to center...
#	gminx = 0; gmaxx=0;gminy=0; gmaxy=0; gminz=0; gmaxz=0;
#	for obj in objs:
#		if obj != None:
#			scale = obj.scale
#			minx = obj.bound_box[0][0] * scale.x  +  obj.location[0]; 
#			gminx = minx if gminx>minx else gminx;
#			maxx = obj.bound_box[4][0] * scale.x  +  obj.location[0];
#			gmaxx = maxx if gmaxx<maxx else gmaxx;		
#			miny = obj.bound_box[0][1] * scale.y  +  obj.location[1];
#			gminy = miny if gminy>miny else gminy;
#			maxy = obj.bound_box[2][1] * scale.y  +  obj.location[1];
#			gmaxy = maxy if gmaxy<maxy else gmaxy;		
#			minz = obj.bound_box[0][2] * scale.z  +  obj.location[2];
#			gminz = minz if gminz>minz else gminz;
#			maxz = obj.bound_box[1][2] * scale.z  +  obj.location[2];
#			gmaxz = maxz if gmaxz<maxz else gmaxz;
#			#print(('obj bounds',minx,maxx,miny,maxy,minz,maxz));
#			#print(('global:',gminx, gmaxx, gminy, gmaxy, gminz, gmaxz));
#	dx = gmaxx - gminx
#	dy = gmaxy - gminy
#	dz = gmaxz - gminz
#	bb.dimensions= (dx,dy,dz)
#	bb.location = (gminx+dx/2,gminy+dy/2,gminz+dz/2) # location as center of bbox	
#	bpy.context.scene.objects.active = bb
#	bpy.ops.object.select_all(action='DESELECT')
#	for obj in objs:
#		obj.select=True
#		bpy.ops.object.parent_set(type='OBJECT',keep_transform=True)
#		obj.select=False
#		#obj.hide_select = True
#		#Keep Hierarchy selectable, but avoid transforming children independent of parent.
#		obj.lock_location = (True,True,True)
#		obj.lock_rotation = (True,True,True)
#		obj.lock_scale	 = (True,True,True)		
#	bb.select=True		
#	return bb


def	uiuretrete():
	for obj in objs:
		if obj != None:			
			obj.select = True

	bpy.ops.object.parent_set(type='OBJECT',keep_transform=True)	
	#bpy.ops.object.parent_clear(type='CLEAR_INVERSE')
	return res

o1=color(yellow, translate([20,0,0],cube(10)))
o2=color(green, translate([0,34,0],cube(10)))
o3=color(blue, translate([0,0,-40],cube(10)))
o4=translate([-20,-5,10],sphere(20))
o=group(o1,o2,o3,o4)


#o=bpy.data.objects["c"]
#bo=bpy.data.objects["Cube"]

#o=translate([10,20,0], scale([1,1.5,1],cylinder(12,60)))
#o=difference(sphere(20,center=true),translate([5,0,0],cylinder(10,50)))

#color(green,o)
#bo=cube(10)
#color(yellow,bo)

#bb=o.bound_box[4][0] # boundbox 8x<x,y,z>->( LoX,LoY,LoZ, LoX,LoY,HiZ, LoX,HiY,HiZ, LoX,HiY,LoZ, HiX,LoY,LoZ, HiX,LoY,HiZ, HiX,HiY,HiZ, HiX,HiY,LoZ ). 
#  r = o.location[0] + bb  # outer radius of object.. X-location defines inner "hole", plus bound box outer in X direction..

#dimX=o.bound_box[5][0]-o.bound_box[0][0]
#dimY=o.bound_box[2][1]-o.bound_box[1][1]
#dimZ=o.bound_box[1][2]-o.bound_box[0][2]
#print(dimX,dimY,dimZ)
#


# calculate parent bounding box
#bo.dimensions = o.dimensions
##bo.location = o.location
#bo.location[0]=o.bound_box[0][0]
#bo.location[1]=o.bound_box[0][1]
#bo.location[2]=o.bound_box[0][2]

##Keep Hierarchy selectable, but avoid transforming children independent of parent.
#o.lock_location = (True,True,True)
#o.lock_rotation = (True,True,True)
#o.lock_scale	 = (True,True,True)
#


#for i in range(0,8):
#  for x in range(0,2):
#	  print(o.bound_box[i][x])
	
	
#for i in range(0,8):
#  print(bo.data.vertices[i].co)
#  for x in range(0,2):
#	  print (o.bound_box[i][x])	  
#	  bo.data.vertices[i].co[x] = o.bound_box[i][x]
#	  
		
	#bo.data.vertices[p.vertices[i]].co
#for i in range(0,8):
#	print(bo.data.vertices[i].co)








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