# blenderscad.core
# Color name definitions as defined in OpenSCAD (and SVG)
#
# by Michael Mlivoncic, 2013
#


## OpenSCAD like Blender programming
## This is just a proof of concept implementation - Work in Progress.
## It will enhance Blender with additional Python definitions for convenience. 
## Should help in making scripting as easy as in OpenSCAD. 
##
## in a later phase, simple OpenSCAD could be transformed into something that evaluates in Blender
##  might be a way to join projects and overcome OpenSCAD performance problems?
## written by Michael Mlivoncic, December 2013

# TODOs
# - minkowski sum emulation?

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

#from blenderscad import *
#################################################################
## BlenderSCAD core functionality
#################################################################   
import bpy
import bpy_types

import sys

import math
from mathutils import Vector  # using Vector type below...

import blenderscad # for "global" variables fn, defColor,...
#from blenderscad.math import *  # true, false required...

# need to setup/reference our default material
mat=blenderscad.mat
#mat = bpy.data.materials.get('useObjectColor')
#if mat is None:
#	mat=bpy.data.materials.new('useObjectColor')
#	mat.use_object_color=1

#Emulate OpenSCAD Special variables  blenderscad.{fs,fa,fn}
#fa - minimum angle  $fn = 360 / $fa    / default: $fa = 12 -> segments = 30
#fs - minimum size   default: 1 
#fn - number of fragments  | override of $fa/$fs , default = 0 , example: 36-> every 10 degrees

#	get_fragments_from_r() - ported from OpenSCAD to emulate special variables $fs,$fa,$fn
#	Returns the number of subdivision of a whole circle, given radius and
#	the three special variables $fn, $fs and $fa
def get_fragments_from_r(r, fn=None, fs=None, fa=None):
	GRID_COARSE = 0.001;
	GRID_FINE   = 0.000001;
	if fn is None: fn=blenderscad.fn
	if fs is None: fs=blenderscad.fs
	if fa is None: fa=blenderscad.fa
    # if r== ... well need to provide some radius
	if r < GRID_FINE: return 3;
	if fn > 0.0: return int(fn if fn >= 3 else 3);
	return int(math.ceil(max(min(360.00 / fa,  r*2*math.pi / fs ) , 5)  )  );

########	
#	if (r < GRID_FINE) return 3;
#	if (fn > 0.0) return (int)(fn >= 3 ? fn : 3);
#	return (int)ceil(fmax(fmin(360.0 / fa, r*2*M_PI / fs), 5));
########
	
	
# clearAllObjects(): empty whole scene, useful during development
# It tries to really remove the objects, not only unlink, so the .blend files won't grow with the garbage.
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
#clearAllObjects()


# list all Blender objects for debugging purposes
def listAllObjects():
	for obj in bpy.data.objects:
 		print(obj.name)	


#########################################3
## echo() and str()
try:
    import __builtin__
except ImportError:
    import builtins as __builtin__ #Python 3.0

# almost OpenSCAD echo, but concatenating param output without colons and whitespaces.
# use explicitly if wanted.
def echo(*args):
	sys.stdout.write('ECHO: ')  # like print, but no newline to prefix...
	for a in args:
		sys.stdout.write(__builtin__.str(a))
	sys.stdout.write('\n')
		
def str(*args):	
	res=""
	for a in args:
		res = res + (__builtin__.str(a))
	return res

#tests...		
#echo("Value: ", 123, 'mm')
#echo(pow(2,2))
#number=4;
#echo (str("This is ",number,3," and that's it."));


# OpenSCAD: color()
# applies to given object o or the current context object the given color
# color is either a float vector with 3 or 4 components (rgb , rgba) or a color name
# from blenderscad.colors - no need to quote the string, as all colors defined as variables.
def color( rgba=(1.0,1.0,1.0, 0), o=None): 
	if type(rgba)== type('SomeString'):
		rgba = getattr(blenderscad.colors, rgba)		
		#echo("newCol:" , rgba)
	if o is None:
		o = bpy.context.object
	if len(rgba) == 3:
		rgba=(rgba[0],rgba[1],rgba[2],0)
	o.color = rgba
	return o

# color('orange', cube(20) )
# color(lime, cube(20) )	
# color((1.0,0,0))


# OpenSCAD: translate(v = [x, y, z]) { ... }
def translate( v=(0.0,0.0,0.0), o=None):
	if len(v)==2: # 2D case where only 2 components provided
		v.append(0.0)
	if o is None:
		o = bpy.context.object
	bpy.ops.object.select_all(action = 'DESELECT')
	o.select = True
	#bpy.ops.transform.translate(value=v) # gives error: "convertViewVec: called in an invalid context"  as ops uses the view...
	o.location += Vector(v)
	#
    # not sure if those updates are useful	
#	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)
#	bpy.context.scene.update()	
	bpy.ops.object.transform_apply(location=True) # Apply the object's transformation to its data
	return o

		
# OpenSCAD: rotate(a = deg, v = [x, y, z]) { ... }
# !!! "When a rotation is specified for multiple axes then the rotation is applied in the following order: x, y, z."
# rotate(a=[0,180,0]) { ... }  # will rotate your object 180 degrees around the 'y' axis.
# rotate(a=45, v=[1,1,0]) { ... }  # The optional argument 'v' allows you to set an arbitrary axis about which the object will be rotated.
#
#TODO: fully implement  http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#rotate
# Rotation in Blender: http:#pymove3d.sudile.com/stationen/kc_objekt_rotation/rotation.html#eulerrotation
# Rotates its child "a" degrees about the origin of the coordinate system or around an arbitrary axis. 
#
# todo: need to implement more rotate param compatibility
#		rotate(360*i/4 , translate([10+random_vect[i],0,0] ,

def rotate( a=[0.0,0.0,0.0], v=[0,0,0], *args):
	o = None
	for arg in args: # look for object in args...	    
		if type(arg) is  bpy_types.Object:
			o=arg
	if type(a) == int or type(a) == float:    # support for single size value argument
		a=[a*v[0],a*v[1],a*v[2]]		
	#old code	
	if o is None:
		o = bpy.context.object	
	bpy.ops.object.select_all(action = 'DESELECT')
	o.select = True
	cos = math.cos
	sin = math.sin
	radians= math.radians
	#
	ax=radians(a[0]) # a[0]*deg # one degree is 2*pi/360	
	ay=radians(a[1]) # a[1]*deg
	az=radians(a[2]) # a[2]*deg
	#echo(['rotate', a,[ax,ay,az],o.location])		
	#o.rotation_euler = ( old[0]+ax , old[1]+ay, old[2]+ az)
	bpy.ops.transform.rotate(value = ax, axis = (1, 0, 0), constraint_axis = (True, False, False), constraint_orientation = 'GLOBAL')
	bpy.ops.transform.rotate(value = ay, axis = (0, 1, 0), constraint_axis = (False, True, False), constraint_orientation = 'GLOBAL')
	bpy.ops.transform.rotate(value = az, axis = (0, 0, 1), constraint_axis = (False, False, True), constraint_orientation = 'GLOBAL')
    # not sure if those updates are useful	
#	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)
#	bpy.context.scene.update()	
	bpy.ops.object.transform_apply(rotation=True) # Apply the object’s transformation to its data 
#	
	# OpenSCAD emulation: need to also rotate location vector.
	# some relocation via matrix multiplications (hopefully correct)
	# have a look at e.g. http://www.cs.mtu.edu/~shene/COURSES/cs3621/NOTES/geometry/geo-tran.html
	x = o.location[0]; 	y = o.location[1];	z = o.location[2];
	#     x Transform 
	o.location[1] = ( cos(ax)*y -sin(ax)*z )
	o.location[2] = ( sin(ax)*y +cos(ax)*z ) 
	y = o.location[1]
	z = o.location[2]
	for i in range(0,2):	o.location[i]=round(o.location[i] , 2); 	
	#     y-Transform   
	o.location[0] = (cos(ay)*x +sin(ay)*z) 
	o.location[2] = (-sin(ay)*x +cos(ay)*z)
	x = o.location[0]
	z = o.location[2]
	for i in range(0,2):	o.location[i]=round(o.location[i] , 2); 	
	#     z-Transform  
	o.location[0] = (cos(az)*x -sin(az)*y) 
	o.location[1] = (sin(az)*x +cos(az)*y)            
	x = o.location[0]
	y = o.location[1]
	for i in range(0,2):	o.location[i]=round(o.location[i] , 2); 	
	bpy.ops.object.transform_apply(location=True)
	# combined rotations...
# All in one...
#	o.location[0] = ( cos(radians(a[1])) + cos(radians(a[2]))  )*x + (  -sin(radians(a[2]))  )*y + (  sin(radians(a[1]))  )*z
#	o.location[1] = ( sin(az)  )*x + (  cos(ax) + cos(az)  )*y + (  -sin(ax)  )*z
#	o.location[2] = ( -sin(ay) )*x + (  sin(ax)  )*y + ( cos(ax) + cos(ay)  )*z
	#echo(['AFTERrotate', a,[ax,ay,az],o.location])	
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



# OpenSCAD: mirror([ x, y, z ]) {...}
# Mirrors the child element on a plane through the origin. 
# The argument to mirror() is the normal vector of a plane intersecting the origin through which to mirror the object.
def mirror(a=[1,0,0], o=None):
	if o is None:
		o = bpy.context.object
	bpy.ops.object.select_all(action = 'DESELECT')
	o.select = True
	axis = (a[0]==1, a[1]==1, a[2]==1)
	bpy.ops.transform.mirror( constraint_axis = axis, constraint_orientation = 'GLOBAL')
	#.ops.transform.mirror( constraint_axis = (False, True, False), constraint_orientation = 'GLOBAL')
	return o

#color(red, rotate([0,0,10], cube([3,2,1])));
#mirror([1,0,0], translate([1,0,0], rotate([0,0,10], cube([3,2,1]))));


# OpenSCAD: scale(v = [x, y, z]) { ... }
def scale(v=[1.0,1.0,1.0], o=None):
	if len(v)==2: # 2D case where only 2 components provided
		v.append(0.0)
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
#	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)
#	bpy.context.scene.update()	
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
#	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)
#	bpy.context.scene.update()	
	bpy.ops.object.transform_apply(scale=True) # Apply the object’s transformation to its data
	return o
	
#resize([15,5,20], cube(size=5)	)


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

# saw a hint that remesh may fix some boolean ops probs..
def remesh( o=None, apply=True):
	if o is None:	
		o = bpy.context.scene.objects.active
	else:
		bpy.context.scene.objects.active = o
	#bpy.ops.object.select_all(action = 'DESELECT')
	#o.select = True
	rem = o.modifiers.new('Remesh', 'REMESH')
	rem.mode = "SHARP"  # BLOCKS, SMOOTH
	rem.scale = 0.9
	rem.octree_depth = 8.0
	rem.sharpness = 1.000
	rem.threshold = 1.000
	rem.use_smooth_shade = False
	rem.use_remove_disconnected = True
	# often forgotten: needs to be active!!
	bpy.context.scene.objects.active = o
	if apply==True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Remesh')
	o.name = 'rm('+o.name+')'
	o.data.name = 'rm('+o.data.name+')'	
	return o

# wrapper for decimate Modifier
def decimate( o=None, apply=True ):
	import bpy
	if o is None:   
		o = bpy.context.scene.objects.active
	else:
		bpy.context.scene.objects.active = o	
	de = o.modifiers.new('MyDecimate', 'DECIMATE')
	#de.angle_limit = 0
	de.iterations = 4
	# often forgotten: needs to be active!!
	bpy.context.scene.objects.active = o
	if apply==True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyDecimate')	
	return o	
	
# wrapper for limited dissolve (attempt to cleanup model after bool op.)
def dissolve(o=None):
	import bpy
	if o is None:   
		o = bpy.context.scene.objects.active
	else:
		bpy.context.scene.objects.active = o
	if bpy.context.active_object.mode is not 'EDIT':	
		bpy.ops.object.mode_set(mode = 'EDIT' )
	bpy.ops.mesh.select_all(action="SELECT")
	# Dissolve selected edges and verts, limited by the angle of surrounding geometry
	bpy.ops.mesh.dissolve_limited(angle_limit=0.00000001, use_dissolve_boundaries=True)
	bpy.ops.object.mode_set(mode = 'OBJECT' )			
	return o

# eliminate a given polygon/face of an object
# found: http://yorik.uncreated.net/guestblog.php?2013=314
def deletePolygon(obj, faceIdx):
	#obj = bpy.context.active_object
	if bpy.context.active_object.mode is not 'EDIT':	
		bpy.ops.object.mode_set(mode = 'EDIT' )
	bpy.ops.mesh.select_all(action="DESELECT")
	bpy.ops.object.mode_set(mode = 'OBJECT' )
	obj.data.polygons[faceIdx].select = True
	bpy.ops.object.mode_set(mode = 'EDIT' )
	bpy.ops.mesh.delete(type="FACE")
	bpy.ops.object.mode_set(mode = 'OBJECT' )
	return {'FINISHED'}

	
#-----------------------------------------------------------------------------
# from: http://blenderartists.org/forum/archive/index.php/t-278694.html
#remove duplicates v1.3
#best way to remove duplicates, just select the objects you want the duplicates removed, then run this scrpit
def remove_duplicates():
	for obj in bpy.context.selected_objects:
		if obj.type == 'MESH':
			bpy.data.scenes[0].objects.active = obj # make obj active to do operations on it
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False) # set 3D View to Object Mode (probably redundant)
			bpy.ops.object.mode_set(mode='EDIT', toggle=False) # set 3D View to Edit Mode
			bpy.context.tool_settings.mesh_select_mode = [False, False, True] # set to face select in 3D View Editor
			bpy.ops.mesh.select_all(action='SELECT') # make sure all faces in mesh are selected
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False) # very silly, you have to be in object mode to select faces!!

			found = set([]) # set of found sorted vertices pairs

			for face in obj.data.polygons:
				facevertsorted = sorted(face.vertices[:]) # sort vertices of the face to compare later
				if str(facevertsorted) not in found: # if sorted vertices are not in the set
					found.add(str(facevertsorted)) # add them in the set
					obj.data.polygons[face.index].select = False # deselect faces i want to keep

			bpy.ops.object.mode_set(mode='EDIT', toggle=False) # set to Edit Mode AGAIN
			bpy.ops.mesh.delete(type='FACE') # delete double faces
			bpy.ops.mesh.select_all(action='SELECT')
			bpy.ops.mesh.normals_make_consistent(inside=False) # recalculate normals
			bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False) #remove doubles
			bpy.ops.mesh.normals_make_consistent(inside=False) # recalculate normals (this one or two lines above is redundant)
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False) # set to Object Mode AGAIN
	return obj
	
def cleanup_object(o=None,removeDoubles=False,subdivide=False, normalsRecalcOut=False):
	#echo("cleanup", [removeDoubles, subdivide, normalsRecalcOut])		
	if o is None:	
		o = bpy.context.scene.objects.active
	else:
		bpy.context.scene.objects.active = o
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.ops.mesh.select_all(action="SELECT")
	if removeDoubles:
		bpy.ops.mesh.remove_doubles(threshold=0.01)
	bpy.ops.mesh.select_all(action="SELECT")		
	if normalsRecalcOut:	
		bpy.ops.mesh.normals_make_consistent(inside=False) #recalc normals on outside
	#bpy.ops.mesh.fill_holes()
	bpy.ops.mesh.select_all(action="SELECT")
#	if subdivide:  # could fix probs with boolean Difference modifier..
#		bpy.ops.mesh.subdivide(number_cuts=p) # 4 pieces in each direction
	# TODO: subdivide:
	#    number_cuts (int in [1, inf], (optional)) – Number of Cuts
	#    smoothness (float in [0, inf], (optional)) – Smoothness, Smoothness factor.
	#    fractal (float in [0, inf], (optional)) – Fractal, Fractal randomness factor.
	#    corner_cut_pattern (enum in ['PATH', 'INNER_VERTEX', 'FAN'], (optional)) – Corner Cut Pattern, Topology pattern to use to fill a face after cutting across its corner
	#		
	# found: https://github.com/CGCookie/script-bakery/blob/master/scripts/tests/exportMeshProBuilder.py
	# select nGons
	#bpy.ops.mesh.select_by_number_vertices(number=4, type='GREATER')
	#bpy.ops.mesh.select_by_number_vertices(type='OTHER')
	# convert nGons to triangles
#	bpy.ops.mesh.quads_convert_to_tris(use_beauty=True)
	# convert triangles to quads, not pretty but is better than holes in the mesh.
#	bpy.ops.mesh.tris_convert_to_quads(limit=0.698132, uvs=False, vcols=False, sharp=False, materials=False)
	# return to object mode
	#
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')	
	#bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)	
	bpy.context.scene.update()	
	return o	

# join as a (better?) alternative to union()
# apply is dummy to mock full union syntax
def join(o1,*objs, apply=True):
	bpy.ops.object.select_all(action = 'DESELECT')
	o1.select = True
	#cleanup_object(o1)
	o1.name = 'J('+o1.name
	bpy.context.scene.objects.active = o1
	for obj in objs:
		if obj is not None:			
			#cleanup_object(obj)		
			o1.name = o1.name +','+obj.name
			obj.select = True
			#bpy.context.scene.objects.active = o1
			bpy.ops.object.join()
			cleanup_object(o1)		
	o1.name = o1.name + ')'
	o1.data.name = o1.name
	#objA.data.name = boolOp[0]+'('+objA.data.name+','+objB.data.name+')'
    # 
	cleanup_object(o1)
	return o1

#join(cube(10), cylinder(r=5,h=15), cylinder(r=2.5,h=20))
#cylinder(r=5,h=15)
	
# booleanOp is used by union(), difference() and intersection()
# TODO: apply=False will require a fix to allow for later scaling, etc.
def booleanOp(objA, objB, boolOp='DIFFERENCE', apply=True):		
	#bpy.ops.object.select_all(action = 'DESELECT')
	#obj_A.select = True
	# circumvent problem with "CSG failed, exception degenerate edge, Unknown internal error in boolean"
	#echo(["boolOp", boolOp])
#	if boolOp=='DIFFERENCE':
#		cleanup_object(objA, subdivide=False)	
#	else:
#		cleanup_object(objA)
	#remesh(o=objA)
#	cleanup_object(objB)
	#remesh(o=objB)
	#
	boo = objA.modifiers.new('MyBool', 'BOOLEAN')
	boo.object = objB
	boo.operation = boolOp  #  { 'DIFFERENCE', 'INTERSECT' , 'UNION' }
	# often forgotten: needs to be active!!
	bpy.context.scene.objects.active = objA
	#objA.name = boolOp[0]+'('+objA.name+','+objB.name+')'
	#objA.data.name = boolOp[0]+'('+objA.data.name+','+objB.data.name+')'
	if apply is True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyBool')
		mesh = objB.data
		bpy.context.scene.objects.unlink(objB)	
		bpy.data.objects.remove(objB)
		bpy.data.meshes.remove(mesh)
	else:
		objB.hide_select = True
		objB.hide = True
#	cleanup_object(objA, removeDoubles=True)
	#echo("boolOpEND")
	#bpy.context.scene.update()	
	return objA

	
def union(o1,*objs, apply=True):
	res = o1
	#cleanup_object(res, removeDoubles=True, subdivide=False)
	tmp=res.name
	for obj in objs:
		if obj != None:
			tmp=tmp+","+obj.name
			#cleanup_object(obj, removeDoubles=True, subdivide=False)			
			res = booleanOp(res,obj, boolOp='UNION', apply=apply)	
	res.name = 'u('+tmp+')'
	res.data.name = 'u('+tmp+')'
	#cleanup_object(res, removeDoubles=True, subdivide=False)
	return res
		
# TODO: write some "debug" mode grouping instead of really diffing sub-tree
#def difference(o1,o2,*objs, apply=True):
#	return booleanOp(o1,union(o2,*objs), boolOp='DIFFERENCE', apply=apply)

def difference(o1,*objs, apply=True):
	res = o1
	cleanup_object(o1, subdivide=True)	
	tmp=res.name	
	to = None
	for obj in objs:
		if obj != None:
			tmp=tmp+","+obj.name
			cleanup_object(obj, removeDoubles=True, subdivide=False)	
			#res = booleanOp(res,obj, boolOp='DIFFERENCE', apply=apply)
			if to is None:
				to = obj
			else:
				to = join(to,obj)
				#to = booleanOp(obj,to, boolOp='UNION', apply=apply)	
	res = booleanOp(res,to, boolOp='DIFFERENCE', apply=apply)			
	res.name = 'd('+tmp+')'
	res.data.name = 'd('+tmp+')'
	cleanup_object(res, removeDoubles=True, subdivide=False)
	return res

	
def intersection(o1,*objs, apply=True):
## Remark: cannot use union here!! need to intersect all...
	res = o1
	#cleanup_object(res, removeDoubles=True, subdivide=False)
	tmp=res.name
	for obj in objs:
		if obj != None:
			tmp=tmp+","+obj.name
			#cleanup_object(obj, removeDoubles=True, subdivide=False)
			res = booleanOp(res,obj, boolOp='INTERSECT', apply=apply)
	res.name = 'i('+tmp+')'
	res.data.name = 'i('+tmp+')'
	#cleanup_object(res, removeDoubles=True, subdivide=False)	
	return res
	

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
	#bpy.ops.mesh.convex_hull(join_triangles=True, make_holes=True, limit=3.14159,delete_unused=True, use_existing_faces=False)
	# TODO: optimize params to keep shapes clean?
    #delete_unused (boolean, (optional)) – Delete Unused, Delete selected elements that are not used by the hull
    #use_existing_faces (boolean, (optional)) – Use Existing Faces, Skip hull triangles that are covered by a pre-existing face
    #make_holes (boolean, (optional)) – Make Holes, Delete selected faces that are used by the hull
    #join_triangles (boolean, (optional)) – Join Triangles, Merge adjacent triangles into quads
    #limit (float in [0, 3.14159], (optional)) – Max Angle, Angle Limit
	bpy.ops.mesh.remove_doubles()
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')
	o.name= "hull(" + o.name + ")"
	o.data.name= "hull(" + o.data.name + ")"
	cleanup_object(o)
	return o



#OpenSCAD: "projection() creates 2d drawings from 3d models, to be exported to the dxf format. 
#		   It works by projecting a 3D model to the (x,y) plane, with z at 0. 
#		   If cut=true, only points with z=0 will be considered (effectively cutting the object), 
#		   with cut=false, points above and below the plane will be considered as well (creating a proper projection)."
# Well, not really projection, buy a cut through the object OpenSCAD projection(cut=true)
def projection(o=None,cut=False):
	if o is None:   
		o = bpy.context.scene.objects.active
	else:
		bpy.context.scene.objects.active = o
	if cut:							 
		if bpy.context.active_object.mode is not 'EDIT':
			bpy.ops.object.mode_set(mode = 'EDIT')	  
		bpy.ops.mesh.bisect(plane_co=(0.0, 0.0, 0.0), plane_no=(0.0, 0.0, 1.0), use_fill=cut, clear_inner=True, clear_outer=True, threshold=0.00000)
		bpy.ops.mesh.flip_normals()  # blender treats normals the other way around than OpenSCAD...
		if bpy.context.active_object.mode is not 'OBJECT': 
			bpy.ops.object.mode_set(mode = 'OBJECT')		
	else: #if cut is False:
		# "Flatten" whole object to zero in Z-Axis -> almost projection
		blenderscad.core.dissolve(o)				
		o.dimensions[2]=0.0 ; o.location[2]=0.0
		bpy.ops.object.transform_apply(scale=True, location=True) # Apply the object’s transformation to its data
		###### deselcting all meshes first...
		if bpy.context.active_object.mode is not 'EDIT':	
			bpy.ops.object.mode_set(mode = 'EDIT' )
		bpy.ops.mesh.select_all(action="DESELECT")
		bpy.context.tool_settings.mesh_select_mode = [False, False, True] # set to face select in 3D View Editor
		bpy.ops.object.mode_set(mode = 'OBJECT' )		
		for i in range(len(o.data.polygons)-1,-1,-1):  #for p in o.data.polygons:	
			p = o.data.polygons[i];
			if p.normal[2] <= 0.0: # dirty hack: all faces pointing "down" will be removed
				# p.select will only select the right things if select_mode above set (in EDIT mode)
				p.select = True # needs to happen in OBJECT mode.. faces to be deleted
		bpy.ops.object.mode_set(mode = 'EDIT' )
		bpy.ops.mesh.delete(type="FACE") #  {‘VERT’, ‘EDGE’, ‘FACE’, ‘EDGE_FACE’, ‘ONLY_FACE’]
#		bpy.ops.mesh.remove_doubles(threshold=0.01)
		bpy.ops.object.mode_set(mode = 'OBJECT' )
		##########
	#o.data.update(calc_edges=True, calc_tessface=True)
#	if cut is False:
#		#blenderscad.core.cleanup_object(o=o,removeDoubles=True,subdivide=False, normalsRecalcOut=True)
#		#blenderscad.core.remove_duplicates()		
	print("num vertices: "+str(len(o.data.vertices)))
	print("num polygons: "+str(len(o.data.polygons)))
	return o	

#o=projection( cut=true, o=translate([0,0,-5], rotate([45,0,45], cube(20))));
#o=projection( cut=false, o=translate([0,0,-5], rotate([45,0,45], cube(20))));

# OpenSCAD: linear_extrude(height = <val>, center = <boolean>, convexity = <val>, twist = <degrees>[, slices = <val>, $fn=...,$fs=...,$fa=...]){...}
# see WIKI: http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion
# TODO: convexity and center currently ignored...
def linear_extrude(height, o=None , center=True, convexity=-1, twist=0):
	if o is None:
		o = bpy.context.object
	bpy.context.scene.objects.active = o
	o.select = True
	# TODO: center object...
	#bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
	#bpy.context.scene.cursor_location = (5,5,0)
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.ops.mesh.select_all(action="SELECT")
	bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0.0,0.0,height)})
	#bpy.ops.mesh.extrude_region_move(MESH_OT_extrude=None, TRANSFORM_OT_translate=None)
	#TODO: causes a "convertViewVec: called in an invalid context"	
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')
	if twist != 0:	
		mod1 = o.modifiers.new('Mod1', 'SIMPLE_DEFORM')
		mod1.angle = twist	* (math.pi/180)
		#bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Mod1')				
	#o.data.materials.append(mat)
	#o.color = blenderscad.defColor
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

#, fn=None, fs=None, fa=None):
#segments=blenderscad.core.get_fragments_from_r( r=r, fn=fn, fs=fs, fa=fa )

# OpenSCAD: rotate_extrude(convexity = <val>[, $fn = ...]){...}
# This emulation would also swallow 3D objects ;-)
# params to emulate rotate_extrude of OpenSCAD, 2D object in XY plane
# Wiki on Blender Spin: http://de.wikibooks.org/wiki/Blender_Dokumentation:_Spin_und_SpinDup
# example007.scad shows params file= and layer= -> not implemented, using import_dxf() instead
def rotate_extrude(o=None, fn=None, fs=None, fa=None):	
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
def round_edges(width=1.0, segments=4, verts_only=False, angle_limit=180,o=None, apply=True ):
	if o is None:	
		o = bpy.context.scene.objects.active
	else:
		bpy.context.scene.objects.active = o	
	#bpy.ops.object.select_all(action = 'DESELECT')
	#o.select = True
	bev = o.modifiers.new('MyBevel', 'BEVEL')
	bev.width = width
	bev.segments = segments
	bev.use_only_vertices= verts_only
	bev.angle_limit = angle_limit
	# often forgotten: needs to be active!!
	bpy.context.scene.objects.active = o
	if apply==True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyBevel')
	o.name = 'rnd('+o.name+')'
	o.data.name = 'le('+o.data.name+')'	
	return o

#rotate_extrude (translate([10,10,0],polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] )),fn=16)
#round_edges(width=5, segments=64, o=rotate_extrude (translate([10,10,0],polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] ))))


