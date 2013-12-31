## OpenSCAD like Blender programming
## This is just a proof of concept implementation - Work in Progress.
## It will enhance Blender with additional Python definitions for convenience. 
## Should help in making scripting as easy as in OpenSCAD. 
##
## in a later phase, simple OpenSCAD could be transformed into something that evaluates in Blender
##  might be a way to join projects and overcome OpenSCAD performance problems?
## written by Michael Mlivoncic, December 2013

# TODOs
# - resize: adjust location
# - minkowski sum emulation?
# - $fn ...

## Instructions
#
### Open in Blenders's internal text editor and run as script.
#
## Warning: The open file will be saved as part of the blender file, be careful if you change it externally as well!
## To see output and error messages: Window->Toggle System Console  
#
### To edit in external editor and run in Blender's Python Console:
#
## filename = "O:/BlenderStuff/BlenderSCAD.py
## clearAllObjects()
## exec(compile(open(filename).read(), filename, 'exec'))
#
### Clear command history in Python Console:
## bpy.ops.console.clear(history=True)

import os
import bpy
import bpy_types

from mathutils import *
from math import *

#################################################################
## BlenderSCAD core functionality
#################################################################   

#default layers for all objects
mylayers = [False]*20
mylayers[0] = True

# need to setup our default material
mat = bpy.data.materials.get('useObjectColor')
if mat is None:
	mat=bpy.data.materials.new('useObjectColor')
	mat.use_object_color=1


#constants
true=True
false=False
#pi = math.pi #3.141592

# some colors... 
black = (0.00,0.00,0.00,0)
silver = (0.75,0.75,0.75,0)
gray = (0.50,0.50,0.50,0)
white = (1.00,1.00,1.00,0)
maroon = (0.50,0.00,0.00,0)
red = (1.00,0.00,0.00,0)
purple = (0.50,0.00,0.50,0)
fuchsia = (1.00,0.00,1.00,0)
green = (0.00,0.50,0.00,0)
lime = (0.00,1.00,0.00,0)
olive = (0.50,0.50,0.00,0)
yellow = (1.00,1.00,0.00,0)
navy = (0.00,0.00,0.50,0)
blue = (0.00,0.00,1.00,0)
teal = (0.00,0.50,0.50,0)
aqua = (0.00,1.00,1.00,0)

# default color for object creators below...
defColor = (1.0,1.0,0.1,0)

# emulate OpenSCAD $fn
fn=32  # default precision: every 10 degrees a segment..



if bpy.context.active_object is not None:
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')


# remove everything after experiments...
def clearAllObjects():
	if bpy.context.active_object is not None:
		if bpy.context.active_object.mode is not 'OBJECT': 
			bpy.ops.object.mode_set(mode = 'OBJECT')
	#fix: also remove not selectable objects from scene
	#bpy.ops.object.select_all()
	#bpy.ops.object.delete()
	for o in bpy.context.scene.objects:
		if o.type == 'MESH':
			mesh = o.data
			bpy.context.scene.objects.unlink(o)	
			bpy.data.objects.remove(o)
			bpy.data.meshes.remove(mesh)
		else:		
			bpy.context.scene.objects.unlink(o)
			bpy.data.objects.remove(o)
		

# CAUTION! clear workspace 
clearAllObjects()   


# print all objects
def listAllObjects():
	for obj in bpy.data.objects:
 		print(obj.name)	


# Construct a cube mesh 
# bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def cube(size=(0.0,0.0,0.0), center=False):
	if type(size) == int:    # support for single size value argument
		size=(size,size,size)
	bpy.ops.mesh.primitive_cube_add(location=(0.0,0.0,0.0), layers=mylayers)
	#o = bpy.data.objects['Cube']  # not safe enough if an earlier object named 'Cube' exists...
	o = bpy.context.active_object
	o.dimensions=size
	bpy.ops.object.transform_apply(scale=True)  
	o.name='cu' # +str(index)
	o.data.name='cu'
	# simple color will only display via my def. Material setting
	o.data.materials.append(mat)
	# just some default color
	o.color = defColor
	# scale
	#bpy.ops.transform.resize(value=size)
	#bpy.ops.object.transform_apply(scale=True)
	if (center==False):
		bpy.ops.transform.translate(value=(size[0]/2,size[1]/2,size[2]/2))
	return o


# Construct a cylinder mesh
# bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=2.0, end_fill_type='NGON', view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def _cylinder(h=1, r=1, fn=-1):
	segments = fn if fn != -1 else globals()["fn"]
	bpy.ops.mesh.primitive_cylinder_add(location=(0.0,0.0,0.0), radius=r , depth=h , vertices=segments, layers=mylayers)  
	#o = bpy.data.objects['Cylinder'] # not safe enough if an earlier object named 'Cylinder' exists...
	o = bpy.context.active_object
	o.name='cy' # +str(index)   
	o.data.name='cy'
	return o

# Construct a conic mesh 
#  bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=1.0, radius2=0.0, depth=2.0, end_fill_type='NGON', view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def _cone(h=1, r1=1, r2=2, fn=-1):
	segments = fn if fn != -1 else globals()["fn"]
	bpy.ops.mesh.primitive_cone_add(location=(0.0,0.0,0.0), radius1=r1, radius2=r2, depth=h , vertices=segments, layers=mylayers)
	#o = bpy.data.objects['Cone'] # not safe enough if an earlier object named 'Cone' exists...
	o = bpy.context.active_object
	o.name='cn' # +str(index)
	o.data.name='cn'
	return o

# OpenSCAD: cylinder(h = <height>, r1 = <bottomRadius>, r2 = <topRadius>, center = <boolean>);
#	   cylinder(h = <height>, r = <radius>);
def cylinder(h = 1, r=1, r1 = -1, r2 = -1, center = False, fn=-1):
	if r1 != -1 and r2 != -1 :
		o =_cone(h,r1,r2,fn=fn)
	else:
		o =_cylinder(h,r,fn=fn)
	# just a suitable default material and some default color
	o.data.materials.append(mat)
	o.color = defColor
	if center==False:
		bpy.ops.transform.translate(value=(0,0,h/2))
	return o


# OpenSCAD: sphere(r=1, d=-1)   
# bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, size=1.0, view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False,   
def sphere(r=1, d=-1, center=true, fn=-1):
	segments = fn if fn != -1 else globals()["fn"]
	if d != -1 :
		  r= d/2;
	bpy.ops.mesh.primitive_uv_sphere_add(size=r , segments=segments, ring_count=16,location=(0.0,0.0,0.0), layers=mylayers)
	#o = bpy.data.objects['Sphere'] # not safe enough if an earlier object named 'Sphere' exists...
	o = bpy.context.active_object
	o.name='sp' # +str(index)
	o.data.name='sp'
	# simple color will only display via my def. Material setting
	o.data.materials.append(mat)
	# just some default color
	o.color = defColor
	# scale
	#bpy.ops.transform.resize(value=size)
	#bpy.ops.object.transform_apply(scale=True)
	return o

# Construct a circle
## OpenSCAD: circle(r = <val>);
def circle(r=10.0, fill=False, fn=-1):
	segments = fn if fn != -1 else globals()["fn"]  
	if fill is False:    
		fill_type = 'NOTHING'
	else:
		fill_type = 'NGON'	 #  fill_type (enum in [‘NOTHING’, ‘NGON’, ‘TRIFAN’], (optional))
	bpy.ops.mesh.primitive_circle_add(vertices=segments, radius=r, fill_type=fill_type, location=(0.0,0.0,0.0), layers=mylayers)
	#bpy.ops.curve.primitive_bezier_circle_add(radius=r, location=(0.0,0.0,0.0), layers=mylayers)
	#o = bpy.data.objects['Cube']  # not safe enough if an earlier object named 'Cube' exists...
	o = bpy.context.active_object
	o.name='ci' # +str(index)
	o.data.name='ci'
	o.data.materials.append(mat)
	o.color = defColor
	return o

# OpenSCAD: import_stl("filename.stl", convexity = <val>);
# TODO: implement convexity...
def import_stl(filename ,convexity=10):
	bpy.ops.import_mesh.stl(filepath=filename)
	o = bpy.context.active_object
	return o

#import_stl("O:/BlenderStuff/demo.stl")


# extra function, not OpenSCAD
# export object as STL.
def export_stl(filename, o=None, ascii=False):
	if o is None:
		o = bpy.context.active_object
	bpy.ops.export_mesh.stl(filepath=filename, ascii=ascii)
	return o

#export_stl("O:/BlenderStuff/demo.stl", cube([10,20,15]) )

#import sys
#sys.path.append("O:/BlenderStuff/BlenderSCAD") 
#from bpy.addons import io_import_scene_dxf
#readAndBuildDxfFile("O:/BlenderStuff/test.dxf")
#cube([10,10,20])			
#bpy.ops.import_scene.autocad_dxf(filepath="O:/BlenderStuff/test.dxf")
#o = bpy.context.active_object
#o.name="DXFtest"



# OpenSCAD: translate(v = [x, y, z]) { ... }
def translate( v=(0.0,0.0,0.0), o=None):
	if o is None:
		o = bpy.context.object
	bpy.ops.object.select_all(action = 'DESELECT')
	o.select = True
	bpy.ops.transform.translate(value=v)
	#
    # not sure if those updates are useful	
	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)
	bpy.context.scene.update()	
	bpy.ops.object.transform_apply(location=True) # Apply the object’s transformation to its data
	return o

		
# OpenSCAD: rotate(a = deg, v = [x, y, z]) { ... }
# Rotation in Blender: http:#pymove3d.sudile.com/stationen/kc_objekt_rotation/rotation.html#eulerrotation
# todo: implement optional v?
def rotate( a=[0.0,0.0,0.0], o=None):
	if o is None:
		o = bpy.context.object
	bpy.ops.object.select_all(action = 'DESELECT')
	o.select = True
	# deg = (pi/180)  # one degree is 2*pi/360
	ax=radians(a[0]) # a[0]*deg
	ay=radians(a[1]) # a[1]*deg
	az=radians(a[2]) # a[2]*deg
	#print([ax,ay,az])		
	#o.rotation_euler = ( old[0]+ax , old[1]+ay, old[2]+ az)
	
	bpy.ops.transform.rotate(value = ax, axis = (1, 0, 0), constraint_axis = (True, False, False), constraint_orientation = 'GLOBAL')
	bpy.ops.transform.rotate(value = ay, axis = (0, 1, 0), constraint_axis = (False, True, False), constraint_orientation = 'GLOBAL')
	bpy.ops.transform.rotate(value = az, axis = (0, 0, 1), constraint_axis = (False, False, True), constraint_orientation = 'GLOBAL')

    # not sure if those updates are useful	
	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)
	bpy.context.scene.update()	
	bpy.ops.object.transform_apply(rotation=True) # Apply the object’s transformation to its data 
#	
	# OpenSCAD emulation: need to also rotate location vector.
	# some relocation via matrix multiplications (hopefully correct)
	# have a look at e.g. http://www.cs.mtu.edu/~shene/COURSES/cs3621/NOTES/geometry/geo-tran.html
	x = o.location[0]
	y = o.location[1]
	z = o.location[2]
	#     z-Transform  
#	o.location[0] = (cos(az)*x -sin(az)*y) 
#	o.location[1] = (sin(az)*x +cos(az)*y)            
#	x = o.location[0]
#	y = o.location[1]
	#     x Transform 
#	o.location[1] = ( cos(ax)*y -sin(ax)*z )
#	o.location[2] = ( sin(ax)*y +cos(ax)*z ) 
#	y = o.location[1]
#	z = o.location[2]
	#     y-Transform   
#	o.location[0] = (cos(ay)*x +sin(ay)*z) 
#	o.location[2] = (-sin(ay)*x +cos(ay)*z)
#	x = o.location[0]
#	z = o.location[2]
	# combined rotations...
	o.location[0] = ( cos(ay) + cos(az)  )*x + (  -sin(az)  )*y + (  sin(ay)  )*z
	o.location[1] = ( sin(az)  )*x + (  cos(ax) + cos(az)  )*y + (  -sin(ax)  )*z
	o.location[2] = ( -sin(ay) )*x + (  sin(ax)  )*y + ( cos(ax) + cos(ay)  )*z
	return o

#translate([10,0,0],cube([10,10,10],center=false ))
#rotate([0,00,90]  )	
#rotate([0,00,90]  )	
#rotate([0,00,90]  )	
#rotate([0,00,90]  )	

#rotate([0,90,00]  )
#rotate([90,00,00] )
#rotate([90,90,90] )
#rotate([45,45,45]	)
#
#cylinder(h=10,r=3)
#rotate( [90,0,90], cylinder(h=10,r=3) ) 
#rotate([0,0,90],  rotate( [90,0,0], cylinder(h=10,r=3) )   ) 
#rotate([90,0,0], rotate( [0,0,90], cylinder(h=10,r=3) )   )

# OpenSCAD: scale(v = [x, y, z]) { ... }
def scale(v=[1.0,1.0,1.0], o=None):
	if o is None:
		o = bpy.context.object
	bpy.ops.object.select_all(action = 'DESELECT')
	o.select = True
	# location needs to be scaled as well..
	l = o.location
	o.location = [l[0]*v[0],l[1]*v[1],l[2]*v[2]]
	bpy.ops.transform.resize(value=v)
	#bpy.ops.object.transform_apply(scale=True)
    # not sure if those updates are useful	
	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)
	bpy.context.scene.update()	
	bpy.ops.object.transform_apply(scale=True) # Apply the object’s transformation to its data
	return o

# OpenSCAD: resize(newsize=[30,60,10])  
def resize( newsize=(1.0,1.0,1.0), o=None):
	if o is None:
		o = bpy.context.object
	bpy.ops.object.select_all(action = 'DESELECT')
	# TODO: location!!
	o.select = True
	o.dimensions=newsize
	bpy.context.active_object.data.update()
	bpy.ops.object.transform_apply(scale=True) # Apply the object’s transformation to its data
	return o
	
#resize([15,5,20], cube(size=5)	)
	
def color( rgba=(1.0,1.0,1.0,1.0), o=None): 
	if o is None:
		o = bpy.context.object
	o.color = rgba
	return o

#   bpy.ops.mesh.convex_hull(delete_unused_vertices=True, use_existing_faces=True)
#   Enclose selected vertices in a convex polyhedron   
def hull(o1,*objs):
	o = union(o1,*objs)
	bpy.context.scene.objects.active = o
	o.select=True
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')
	#print("VERTICES: *********")	
	#for v in o.data.vertices:
	#	v.select = True
		#print (v)
	#bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.convex_hull(use_existing_faces=False)
	bpy.ops.mesh.remove_doubles()
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')
	o.name= "hull(" + o.name + ")"
	o.data.name= "hull(" + o.data.name + ")"
	cleanup_object(o)
	return o


# NO OpenSCAD thing, but nice alternative to union(). It preserves the objects and
# therefore different colors. However, need to rework subsequent modifiers?
def group(o1,*objs):
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
			obj.lock_scale    = (True,True,True)
	bpy.ops.object.parent_set(type='OBJECT',keep_transform=True)	
	#bpy.ops.object.parent_clear(type='CLEAR_INVERSE')
	return res


def cleanup_object(o=None):
	if o is None:	
		o = bpy.context.scene.objects.active
	else:
		bpy.context.scene.objects.active = o
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')		
	bpy.ops.mesh.remove_doubles()
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')	
	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)	
	bpy.context.scene.update()	
	return o	

# TODO: apply=False will require a fix to allow for later scaling, etc.
def booleanOp(objA, objB, boolOp='DIFFERENCE', apply=True):		
	#bpy.ops.object.select_all(action = 'DESELECT')
	#obj_A.select = True
	# circumvent problem with "CSG failed, exception degenerate edge, Unknown internal error in boolean"
	cleanup_object(objA)
	cleanup_object(objB)
	#
	boo = objA.modifiers.new('MyBool', 'BOOLEAN')
	boo.object = objB
	boo.operation = boolOp  #  { 'DIFFERENCE', 'INTERSECT' , 'UNION' }
	# often forgotten: needs to be active!!
	bpy.context.scene.objects.active = objA
	objA.name = boolOp[0]+'('+objA.name+','+objB.name+')'
	objA.data.name = boolOp[0]+'('+objA.data.name+','+objB.data.name+')'
	if apply is True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyBool')
		mesh = objB.data
		bpy.context.scene.objects.unlink(objB)	
		bpy.data.objects.remove(objB)
		bpy.data.meshes.remove(mesh)
	else:
		objB.hide_select = True
		objB.hide = True
    # 
	cleanup_object(objA)
	return objA



def union(o1,*objs, apply=True):
	res = o1
	for obj in objs:
		if obj != None:
			res = booleanOp(res,obj, boolOp='UNION', apply=apply)
	return res
		
def difference(o1,o2,*objs, apply=True):
	return booleanOp(o1,union(o2,*objs), boolOp='DIFFERENCE', apply=apply)

def intersection(o1,o2,*objs, apply=True):
	return booleanOp(o1,union(o2,*objs), boolOp='INTERSECT', apply=apply)


# OpenSCAD: polygon(points = [[x, y], ... ], paths = [[p1, p2, p3..], ... ], convexity = N);
# TODO: http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects
# fill seems to cause probs with rotate_extrude in some cases. ->faces at start/end
def polygon(points, paths=[], fill=False):
	# Create mesh and object
	me = bpy.data.meshes.new('p')
	o = bpy.data.objects.new('p', me)
	o.data.materials.append(mat)
	o.color = defColor
	o.location = (0.0,0.0,0.0)
	o.show_name = True
	bpy.context.scene.objects.link(o) 	# Link object to scene
	verts=[] 
	for p in points:
		verts.append([p[0],p[1],0])
	edges = []
	if len(paths)== 0:
		for i in range (0, len(points)-1):			
			edges.append([i,i+1])
		edges.append([len(points)-1, 0])	
	else:
		for p in paths:
			for i in range(0, len(p)-1):
				#print([p[i],p[i+1]])
				edges.append([p[i],p[i+1]])		
			#print([p[i],p[0]])
			edges.append([p[i+1],p[0]])									
	faces = []
	# cool code below to generate faces, however, holes in the polygon would be tricky :-)
	# see path example with inner triangle
#	if len(paths)== 0:
#		face = []
#		faceB = [] # back side
#		for i in range (0, len(verts)):			
#			face.append(i)
#			faceB.append(len(points)-i-1)
#		#edges.append([len(points)-1, 0])	
#		faces = [face, faceB]
#	else:
#		faces = paths	
	# print({'verts':verts} , {'edges': edges}, {'faces': faces} )
	me.from_pydata(verts, edges, faces) # Create mesh fromverts, edges, faces. Use edges OR faces to avoid problems  
	# Update mesh with new data
	me.update(calc_edges=True)		
	bpy.context.scene.objects.active = o
	o.select = True
	# Note: switching mode would fail before mesh is defined and object selected...
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')	
	for el in o.data.vertices: el.select = True
	for el in o.data.edges: el.select = True
	if fill is True:
		try:  # not a clean implementation, but should work for triangular shapes, holes, squares,etc
			bpy.ops.mesh.fill_grid()
		except RuntimeError:
			bpy.ops.mesh.fill() 	
	bpy.ops.mesh.flip_normals()
	#bpy.ops.mesh.edge_face_add() # add face...wrong results for polygones with holes...
	bpy.ops.object.mode_set(mode = 'OBJECT')
	#bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
	#bpy.context.scene.cursor_location = (5,5,0)
	# having this as a curve to reuse in rotate_extrude...
	#bpy.ops.object.convert(target='CURVE')
	return o

## triangle
#polygon(points=[ [8,-8],[8,8],[-8,8] ]) 
## single square, centered around origin
#polygon( points=[ [8,-8],[8,8],[-8,8],[-8,-8] ] , paths=[[0,1,2,3]])
## some profile
#polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] )
#rotate([90,0,0],  polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] ))
## OpenSCAD example: double Triangle, using two paths...
#polygon(points=[[0,0],[50,0],[0,50],[5,5],[40,5],[5,40]], paths=[[0,1,2],[3,4,5]])
#
# "Fish"
#polygon(points=[[0,0],[100,0],[0,100],[5,5],[40,5],[5,40],[45,45],[45,80],[80,45]], paths=[[3,4,5],[0,1,2],[6,7,8]])
# triangle with two triangular holes...
#polygon(points=[[0,0],[100,0],[0,100],[5,5],[30,5],[5,30],[25,25],[25,60],[60,25]], paths=[[3,4,5],[0,1,2],[6,7,8]])




# OpenSCAD: linear_extrude(height = <val>, center = <boolean>, convexity = <val>, twist = <degrees>[, slices = <val>, $fn=...,$fs=...,$fa=...]){...}
# see WIKI: http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion
# TODO: convexity and center currently ignored...
def linear_extrude(height, o=None , center=true, convexity=-1, twist=0):
	if o is None:
		o = bpy.context.object
	bpy.context.scene.objects.active = o
	o.select = True
	# TODO: center object...
	#bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
	#bpy.context.scene.cursor_location = (5,5,0)
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')	
	bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0.0,0.0,height)})
	# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude=None, TRANSFORM_OT_translate=None)
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')
	if twist != 0:	
		mod1 = o.modifiers.new('Mod1', 'SIMPLE_DEFORM')
		mod1.angle = twist	* (pi/180)
		#bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Mod1')				
	#o.data.materials.append(mat)
	#o.color = defColor
	o.name = 'le('+o.name+')'	
	o.data.name = 'le('+o.data.name+')'	
	return o

#linear_extrude( 20, polygon(points=[[30,0],[0,30],[0,0] ]) )
#linear_extrude( 50, circle(r=30) )
#
#linear_extrude(height = 80, center = true, twist = 100, o=translate([2, 0, 0], polygon(points=[ [8,-8],[8,8],[-8,8],[-8,-8] ]) ) )
#linear_extrude(height = 100, center = true, convexity = 10, twist = 100, o=translate([2, 0, 0], polygon(points=[ [8,-8],[8,8],[-8,8]]) ) )
#linear_extrude(height = 10, center = true, twist = -500, o=translate([2, 0, 0],circle(r = 1)))
#linear_extrude(height = 10, o=polygon(points=[[0,0],[100,0],[0,100],[5,5],[30,5],[5,30],[25,25],[25,60],[60,25]], paths=[[3,4,5],[0,1,2],[6,7,8]]))
#linear_extrude(height = 30, twist=-40, o=polygon(points=[[0,0],[100,0],[0,100],[5,5],[30,5],[5,30],[25,25],[25,60],[60,25]], paths=[[3,4,5],[0,1,2],[6,7,8]]))

# OpenSCAD: rotate_extrude(convexity = <val>[, $fn = ...]){...}
# This emulation would also swallow 3D objects ;-)
# params to emulate rotate_extrude of OpenSCAD, 2D object in XY plane
# Wiki on Blender Spin: http://de.wikibooks.org/wiki/Blender_Dokumentation:_Spin_und_SpinDup
def rotate_extrude(o=None, fn=-1):	
	segments = fn if fn != -1 else globals()["fn"]  
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
	prevAreaType = bpy.context.area.type # TEXT_EDITOR or CONSOLE
	bpy.context.area.type = 'VIEW_3D' # probably: need to set cursor for Spin to be right...	
	#print(o.location)
	bpy.context.scene.cursor_location = o.location
	#o.location=(10,0,0)
	bpy.ops.view3d.viewnumpad(type='TOP')
	bpy.ops.view3d.snap_cursor_to_selected()
	#print (bpy.ops.mesh.spin.poll())	
    # params to emulate rotate_extrude of OpenSCAD, 2D object in XY plane
	angle = pi*2.0 #(360 * pi / 180) # ggrrr.. need to convert or debug for hours :-)
	bpy.ops.mesh.spin(steps=segments, dupli=False, angle=angle, center=(0.0, 0.0, 0.0), axis=(0.0, 0.0, 1.0))
	# if duplicate: delete original meshes... still selected.
	#bpy.ops.mesh.delete(type='VERT')	
	#bpy.ops.mesh.delete(type='EDGE')	
	bpy.ops.mesh.select_all(action='SELECT')	
	bpy.ops.mesh.remove_doubles()	
	bpy.context.area.type = prevAreaType  	# restore area / context
	bpy.ops.mesh.normals_make_consistent(inside=False)
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')	
	o.location[2] += newz
	o.name = 're('+o.name+')'
	o.data.name = 'le('+o.data.name+')'	
	#	o.data.materials.append(mat)
	#	o.color = defColor
	# TODO: need to cleanup the result
	#mod1 = o.modifiers.new('Mod1', 'SOLIDIFY')	
	#bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Mod1')
	return o

#rotate_extrude (polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] ))
#translate([10,10,0],polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] ))
#rotate_extrude (translate([10,10,0],polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] )))
#rotate_extrude (translate([5,0,0] ,circle(r=4, fill=true)))
#rotate_extrude (translate([10,10,10] ,polygon(points=[[0,0],[100,0],[0,100]])))
# should better warn on 3D objects ...rotate_extrude (translate([5,0,0],cube([10,10,5])))
#rotate_extrude( translate([10,10,10] ,circle(r=5) ))
#hull( rotate_extrude(translate([20,0,0], circle(r = 10, fill=true) )) )
#rotate_extrude( translate([10,10,10] , polygon( points=[[0,0],[2,1],[1,2],[1,3],[3,4],[0,5]] ))) 
#rotate_extrude( translate([10,10,10] , polygon( points=[[0,0],[4,0],[4,4],[0,4]]) )) 
#rotate_extrude( translate([9-2, 2, 0], circle(r = 2)))



# an extra not present in OpenSCAD... using Blender's "bevel" Modifier
def round_edges(width=1.0, segments=4, verts_only=False, angle_limit=180, apply=True ,o=None):
	scn = bpy.context.scene 
	#bpy.ops.object.select_all(action = 'DESELECT')
	#o.select = True
	bev = o.modifiers.new('MyBevel', 'BEVEL')
	bev.width = width
	bev.segments = segments
	bev.use_only_vertices= verts_only
	bev.angle_limit = angle_limit
	# often forgotten: needs to be active!!
	scn.objects.active = o
	if apply==True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyBevel')
	o.name = 'rnd('+o.name+')'
	o.data.name = 'le('+o.data.name+')'	
	return o

#rotate_extrude (translate([10,10,0],polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] )),fn=16)
#round_edges(width=5, segments=64, o=rotate_extrude (translate([10,10,0],polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] ))))


#################################################################
## some additional library functions
#################################################################   
#TODO: translate more lib functions and eventually pack into separate files

# translated from "shapes.scad"
## size is the XY plane size, height in Z
def hexagon(size, height):
    boxWidth = size/1.75
    o = None
    for r in [-60, 0, 60]:
        tmp=rotate([0,0,r], cube([boxWidth, size, height], true))
        o=union(tmp,o) # trick to overcome OpenSCADs implicit union :-)
    return o

#hexagon(10,30)

# size is the XY plane size, height in Z
def octagon(size, height):
  intersection(
    cube([size, size, height], true)
    , rotate([0,0,45], cube([size, size, height], true))
  )

#octagon(size=10,height=25)

def ellipsoid(w, h, center = false):
    scale([1, h/w, 1], sphere(r=w/2, center=center) )

#ellipsoid(w=10,h=5, center=true)
	
# roundedBox -> only sides!!
# size is a vector [w, h, d]
def roundedBox(width, height, depth, radius):
  o1= cube([width-2*radius,height,depth], true)
  o2= cube([width,height-2*radius,depth], true)
  o = union(o1,o2)
  for x in [radius-width/2, -radius+width/2] :
       for y in [radius-height/2, -radius+height/2] :
            ot= translate([x,y,0] , cylinder(r=radius, h=depth, center=true))
            o = union(o,ot)

#roundedBox(width=10, height=5, depth=20, radius=2)


#" official" rcube module from thingiverse rounded primitives
def rcube(Size=[20,20,20],b=0.5):
    tmp = None
    for x in [-(Size[0]/2-b),(Size[0]/2-b)]:
       for y in [-(Size[1]/2-b),(Size[1]/2-b)]:
            for z in [-(Size[2]/2-b),(Size[2]/2-b)]:
                tmp= union(translate([x,y,z], sphere(b) ), tmp)                
    hull(tmp)


#rcube([10,20,10],1)

# based on "rounded Primitives" from Thingiverse
def rcylinder(r=1, h=1, b=0.5, r1=-1, r2=-1):
	if r1 == -1 or r2 == -1:
		r1 = r
		r2 = r
		print([r1,r2])
	return translate([0,0,-h/2],
			hull(
			   rotate_extrude(translate([r1-b, b, 0], circle(r = b)))
	  		 , rotate_extrude(translate([r2-b, h-b, 0], circle(r = b)))			
            )
         )

#rcylinder(8, 24, b=2)

# TODO: Alternative: rounded Cylinder Caps...
#intersection( translate([0,0,-70],sphere(r=80)), cylinder(r=10,h=30))
#intersection( translate([0,0,-5],sphere(r=15)), cylinder(r=10,h=30))
#difference(intersection( translate([0,0,-5],sphere(r=15)), cylinder(r=10,h=30)), translate([0,0,33],cube([20,20,50],center=true)) )


#################################################################
## Tests
#################################################################   
	
# A few OpenSCAD like operations... need to substitute brackets
# note that operators like translate,color,scale,etc. can also be called on active object 
def OpenSCADtests():
	c0 = cube((5,7,4),center=true) 
	translate(v=(-8,-5,0))
	c1 = cube((5,10,4),center=true)
	translate(v=(10,20,20))
	color(blue)
	color(red,c0)
	scale((5,9,4),c0)
	#   
	c0 = cube((12,12,4),center=true)
	c1 = cube((6,6,4),center=true)  
	color(green)
	difference(c0,c1)
	translate(v=(1,2,2))
	#  and almost OpenSCAD like...
	difference (
			   color(red,cube((12,12,4),center=true)), 
			   cube((6,6,4),center=true)
			   )
	translate([55,45,0])			
	#
	union (
			   color(green, cube((12,12,4),center=true) ), 
			   color(blue, cube((6,6,9),center=false) )
			   )
	translate([-55,45,0])			
	#
	color(green, translate([50,0,-10] ,cylinder(h=10,r=2)))
	#
	translate([-50,20,10], cylinder(r=10,h=20) )
	translate([25,40,6], cylinder(r=10,h=20, center=true) )


#OpenSCADtests()

def HullDemo():
    return hull (
        translate([0,0,0], cylinder(r=4,h=4) )
        ,translate([20,0,0], cylinder(r=4,h=4) )
        ,translate([10,20,0], cylinder(r=4,h=4) )
    )    
#HullDemo() 

def HullDemo2():
	return scale( (0.5,0.5,0.5) ,rotate( (90,0,90) , hull ( union( sphere(r=4),
	#cylinder(r1=10,r2=20,h=20) 
	translate( (20,20,-10) , cylinder(r1=4,r2=8,h=20,center=true)   )
))))
#HullDemo2()


def Demo1():
	scale([5,5,5], translate([0,0,5],
		union(
			rotate( [90,0,90], cylinder(h=10,r=3,center=true) )   
		,   rotate( [90,0,0], cylinder(h=10,r=3, center=true) )  
		,   rotate( [0,0,90], cylinder(h=10,r=3, center=true) )   
	  )
	)) 

#Demo1()


# OpenJSCAD.org Logo :-)	  
def Demo2():  
	scale([10,10,10], 
	   translate([0,0,1.5] 
		 , group(   
			 color(purple, difference(
				 cube([3,3,3], center=true)
			   , sphere(r=2, center=true)
			 ))
		   , color(yellow, intersection(
				 sphere(r=1.3, center=true)
			   , cube([2.1,2.1,2.1], center=true)
		   ))	 
		 )
	 )
	)

#Demo2()


# OpenJSCAD.org Logo :-)	  
def Demo2b_tripleGrouping():  
	scale([10,10,10], 
	   translate([0,0,1.5] 
		 , group(   
			 color(purple, difference(
				 cube([3,3,3], center=true)
			   , sphere(r=2, center=true)
			 ))
		   , color(yellow, intersection(
				 sphere(r=1.3, center=true)
			   , cube([2.1,2.1,2.1], center=true)
		   ))	 
		   , color(lime, cylinder(r=0.1,h=5,center=true))
		 )
	 )
	)
	  
#Demo2b_tripleGrouping()
	

# My Filament Holder (rough version without rounded corners)
# my original OpenSCAD version: http://www.thingiverse.com/thing:198859
def FilamentHolderSimple(D,A,b) :
   return union(
	difference(
			union(
			   cylinder(r1 = D/2, r2=D/2-1 , h = b, center = true)
			 , translate([0,0,-b/2+1] , cylinder(r1 = D/2+2, r2=D/2+1.5,h = 2, center = true))
			)
		  , cylinder(r = D/2-3, h = b, center = true)
		)  
	, difference(
			union(
				cylinder(r = A/2+4, h = b, center = true)
			  , cube([D-4,4,b],center=true) 
			  , cube([4,D-4,b],center=true) 
			)
		  , cylinder(r = A/2, h = b, center = true)
		) 
	)
  

# Drumm inner diameter in mm
D = 52
# axis diameter
A = 7  #Actually 6mm
b=14 # holder height
#FilamentHolderSimple(D,A,b)

#TODO: Fix error if "union" instead of "group":
#CSG failed, exception degenerate edge
#Unknown internal error in boolean

def pacman():
	global fn
	fn=180
	return scale([2,2,2], translate([0,0,6],rotate([90,45,0],
	    difference(
	        sphere(r=6)        
	    ,   translate([1,1,-6], cube([6,6,12]))
	    ,   translate([-1,4,+2], cylinder (r=1, h=3  ) )
	    ,   translate([-1,4,-5], cylinder (r=1, h=3  ) )
	 ))))

#pacman()

# a fischertechnik helper
def ft_nut(L,A,SLOT,H):
	return union(
		translate([L/2,0,0],
		  color(blue,
			cube([A,SLOT,H+2],center=true)))	
	,   translate([L/2-A/2,0,0],
          color(red,
			cylinder(r = (A/2), h = H*2+2,center = true)))
	)

# a fischertechnik basic block. incomplete, but serves as a demo for the
# fixed rotate() behavior: also rotating the location around the center.
def makeFtBlock():
	L = 15 # Laenge in mm
	B = 15 # Breite in mm
	H = 30 # Hoehe in mm
	A = 4 # axis diameter
	SLOT = 3 
	return translate ([0,0,H/2],
		difference(
			cube([L,B,H],center=true)
			, union(
				   rotate([0,0,0]  , ft_nut(L,A,SLOT,H) )
				 , rotate([0,0,90] , ft_nut(L,A,SLOT,H) )
				 , rotate([0,0,180], ft_nut(L,A,SLOT,H) )
				 , rotate([0,0,270] , ft_nut(L,A,SLOT,H) )
				 # bottom:
				 , translate([0,0,-7.5] , rotate([90,90,0],  ft_nut(L,A,SLOT,H) ))
			)
		)
	 )	

color(red, makeFtBlock() )

						
###########################################################################################
##
## Playground: Below are some experimental script blocks. Potential reuse...  
##
###########################################################################################

#http://askubuntu.com/questions/325485/how-to-make-a-mesh-by-using-python-script-on-blender
def remove_item(item):
	# clear mesh and object
	for item in bpy.context.scene.objects:
	    if item.type == 'MESH':
	        bpy.context.scene.objects.unlink(item)
	for item in bpy.data.objects:
	    if item.type == 'MESH':
	        bpy.data.objects.remove(item)
	for item in bpy.data.meshes:
	    bpy.data.meshes.remove(item)
	for item in bpy.data.materials:
	    bpy.data.materials.remove(item)

# cleanup datafile:
#clearAllObjects()   
#for o in bpy.data.objects:
#	# will fail on purpose on objects still in use!!!
#	bpy.data.objects.remove(o)
	
#item= bpy.data.materials["deleteMe"]
#bpy.data.materials.remove(item)

# Curve-based alternative: TODO: could be a follow-path operator at a later point in time...
# from: http://blenderscripting.blogspot.ch/2011/05/blender-25-python-bezier-from-list-of.html
# somewhat buggy... rather follow path, requires two curves circle and ... to  operate...
def rotate_extrudeOLD(o=None):
	if o is None:
		o = bpy.context.object
	bpy.ops.object.select_all(action = 'DESELECT')
	o.select = True
	#r = sqrt(o.location[0]*o.location[0] + o.location[1]*o.location[1])
	r = o.location[0]
	path = bpy.ops.curve.primitive_bezier_circle_add(radius=r, location=(0.0,0.0,0.0), layers=mylayers)
#	path.location[2] += o.location[1]
	curve = path.data
	curve.bevel_object = o
	bpy.ops.object.convert(target='MESH')
	res = bpy.context.object
	res.name = o.name
	res.data.materials.append(mat)
	res.color = defColor
	bpy.context.scene.objects.unlink(o)
	return res



# round_edges(width=0.1, segments=32, angle_limit=30, apply=False ,obj=None):
def round_edgesTEST(*pargs, **kwargs):
	width = kwargs.pop('width', 0.1)
	segments = kwargs.pop('segments', 16)
	angle_limit = kwargs.pop('angle_limit', 0.1)
	apply = kwargs.pop('apply', False)
	obj = kwargs.pop('obj', None)
	for a in pargs: 
		print(a)
	#
	if type(obj) is  bpy_types.Object:
		print(type(obj)) # bpy_types.Object	 
	scn = bpy.context.scene 
	#bpy.ops.object.select_all(action = 'DESELECT')
	#obj_A.select = True
	bev = obj.modifiers.new('MyBevel', 'BEVEL')
	bev.width = width
	bev.segments = segments
	bev.angle_limit = angle_limit
	# often forgotten: needs to be active!!
	scn.objects.active = obj
	if apply==True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyBevel')
	obj.name = 'Bevel('+obj.name+')'   
	return obj

# playing with arguments...
def round_edgesTEST2( *pargs):
	for a in pargs: 
		print(a)
	
#round_edges(obj=cube([15,4,1]) )
#round_edgesTEST2( 0.1,w=2, cube([15,4,3]) )



# testbed to emulate some minkowski like behavior
# see: http://blenderartists.org/forum/showthread.php?282214-door-frame-disaster-how-do-I-make-one&p=2310204&viewfull=1#post2310204
def minkowskiLike():
	translate([4,0,0] , cube([15,4,1]) )
	rotate([0,90,0] ,cylinder(r=3,h=1))

#minkowskiLike()

def dummy():
	difference( sphere(r=15),
	   #cylinder(r1=10,r2=20,h=20)  
	   translate( (3,3,3) , cylinder(r1=10,r2=20,h=20,center=true)  )
	)
	hull ( union (
		   color(green, cube((12,12,4),center=true) ), 
		   color(blue, cube((6,6,9),center=false) )
		   ))
		
#dummy()	
#cylinder(r=10,h=20)	
#cylinder(r=10,h=20, center=true)   

 
#Now in a for loop, we create the five objects like this (In the screenshot above, I used another method) Press ENTER-KEY twice after entering the command at the shell prompt.   
def Test1():
	for index in range(0, 5):
		#add_cylinder(location =(index*5, 0, index*5), radius=index+5 , depth=index*2+10 , vertices=64, layers=mylayers)
		#myC = bpy.data.objects['Cylinder']
		#myC.name='MyCylinder'+str(index)
		add_cube(location=(index*3, 5, index*4), layers=mylayers)   
		myC = bpy.data.objects['Cube']
		myC.name='MyCube'+str(index)
		# translate
		bpy.ops.transform.translate(value=(0, index*15, 0))
		# scale
		bpy.ops.transform.resize(value=(3+index*5, 3+index*5, 12))
		bpy.ops.object.transform_apply(scale=True)
		# set def material and enable object color (red)
		myC.data.materials.append(mat)
		# bpy.context.object.data.materials.append(mat)
		# bpy.context.object.color = (1,0,0,0)
		myC.color = (1,0,0,0)
	
#  MM: working code to set the native color of an object to display...
##   via a Material...
def Test3():
	mat=bpy.data.materials.new('useObjectColor')
	mat.use_object_color=1
	bpy.context.object.data.materials.append(mat)
	# set red...
	bpy.context.object.color = (1,0,0,0)

  ###bpy.ops.mesh.select_all(action='TOGGLE') #maybe needed?
  #cd.vertices[0].select = True   
  #cd.vertices[5].select = True
  #tmp = [el.select for el in cd.vertices]
  ##c.update(bpy.context.scene)
  #for el in cd.vertices:
  # print (el.select)
  #   bpy.ops.mesh.convex_hull(delete_unused_vertices=True, use_existing_faces=True)


def ScreenAreaExperiment():
	#make a dict of areas keyed by their type 
	areas = {a.type:a for a in bpy.context.screen.areas}
	#get the one we want, or None if not available
	area = areas.get("VIEW_3D",None)
	#if there is one of that kind
	if area:
		space = area.spaces.active
		print (space)
	#view3d.pivot_point='CURSOR'
	#view3d.cursor_location = (0.0, 0.0, 0.0)
	#
	print(bpy.context.area.type)
## found this one after long search: http://blender.stackexchange.com/questions/5810/repeat-a-python-function-multiple-times	
## simply force right context: bpy.context.area.type = 'VIEW_3D'



############################################################
# HUGE todo: auto convert and exec .scad files :-)
# from:
# http://timhatch.com/projects/pybraces/#example

def braces_decode(input, errors='strict'):  
	##global indent_width, current_depth
	current_depth = 0
	indent_width = 4
	#
	if not input: return (u'', 0)
	length = len(input)
	# Deal with chunked reading, where we don't get
	# data containing a complete line of source
	if not input.endswith('\n'):
		length = input.rfind('\n') + 1
	input = input[:length]
	#
	acc = []
	lines = input.split('\n')
	for l in [x.strip().replace('++', '+=1') for x in lines]:
		if l.endswith(';'):
			l = l[:-1]

		if l.endswith('{'):
			acc.append(' ' * current_depth + l[:-1].strip() + ':')
			current_depth += indent_width
		elif l.endswith('}'):
			acc.append(' ' * current_depth + l[:-1].strip())
			current_depth -= indent_width
		else:
			acc.append(' ' * current_depth + l)
	return (u'\n'.join(acc)+'\n', length)


def convertOpenSCAD():
	filenameSCAD = "O:/BlenderStuff/demo.scad"
	filenameConverted = "O:/BlenderStuff/demo.scad.py"
	##clearAllObjects()
	txt = open(filenameSCAD).read()
	#print (txt)
	decodedTxt = braces_decode(txt)  
	#print (decodedTxt)
	myFile = open(filenameConverted, 'w')
	myFile.write(decodedTxt[0])
	myFile.close()
	#exec(compile( decodedTxt, filename, 'exec'))

#convertOpenSCAD()
