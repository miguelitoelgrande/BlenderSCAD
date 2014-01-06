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

import sys

import math
from mathutils import *  # using Vector type below...
import blenderscad
from blenderscad.math import *  # true, false required...

# need to setup/reference our default material
mat = bpy.data.materials.get('useObjectColor')
if mat is None:
	mat=bpy.data.materials.new('useObjectColor')
	mat.use_object_color=1
	

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

	
# OpenSCAD: import_stl("filename.stl", convexity = <val>);
# TODO: implement convexity...
def import_stl(filename ,convexity=10):
	bpy.ops.import_mesh.stl(filepath=filename)
	o = bpy.context.active_object
	o.data.materials.append(mat)
	o.color = blenderscad.defColor
	return o

import_stl("O:/BlenderStuff/demo.stl")


#color(green, import_stl("C:/Users/Nora/Desktop/Michi_Temp/Clips innen Magnetband.stl"))
#color(yellow, import_stl("C:/Users/Nora/Desktop/Michi_Temp/Clips Netzbefestigung aussen.stl"))
#color(purple, import_stl("C:/Users/Nora/Desktop/Michi_Temp/Clips Netzbefestigung innen.stl"))
#color(lime, import_stl("C:/Users/Nora/Desktop/Michi_Temp/Halter Magnet.stl"))
#color(blue, import_stl("C:/Users/Nora/Desktop/Michi_Temp/Profile Aussen unten Rot.stl"))
#color(red, import_stl("C:/Users/Nora/Desktop/Michi_Temp/Profil_1200mm.stl"))


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
	#bpy.ops.transform.translate(value=v) # gives error: "convertViewVec: called in an invalid context"  as ops uses the view...
	o.location += Vector(v)
	#
    # not sure if those updates are useful	
#	bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)
#	bpy.context.scene.update()	
	bpy.ops.object.transform_apply(location=True) # Apply the object’s transformation to its data
	return o

		
# OpenSCAD: rotate(a = deg, v = [x, y, z]) { ... }
# !!! "When a rotation is specified for multiple axes then the rotation is applied in the following order: x, y, z."
# rotate(a=[0,180,0]) { ... }  # will rotate your object 180 degrees around the 'y' axis.
# rotate(a=45, v=[1,1,0]) { ... }  # The optional argument 'v' allows you to set an arbitrary axis about which the object will be rotated.
#
#TODO: fully implement  http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#rotate
# todo: implement optional v?
# Rotation in Blender: http:#pymove3d.sudile.com/stationen/kc_objekt_rotation/rotation.html#eulerrotation
# Rotates its child "a" degrees about the origin of the coordinate system or around an arbitrary axis. 
#
# todo: need to implement more rotate param compatibility
#		rotate(360*i/4 , translate([10+random_vect[i],0,0] ,

def rotate( a=[0.0,0.0,0.0], o=None):
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
	echo(['rotate', a,[ax,ay,az],o.location])		
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
	#     y-Transform   
	o.location[0] = (cos(ay)*x +sin(ay)*z) 
	o.location[2] = (-sin(ay)*x +cos(ay)*z)
	x = o.location[0]
	z = o.location[2]
	#     z-Transform  
	o.location[0] = (cos(az)*x -sin(az)*y) 
	o.location[1] = (sin(az)*x +cos(az)*y)            
	x = o.location[0]
	y = o.location[1]
	# combined rotations...
# All in one...
#	o.location[0] = ( cos(radians(a[1])) + cos(radians(a[2]))  )*x + (  -sin(radians(a[2]))  )*y + (  sin(radians(a[1]))  )*z
#	o.location[1] = ( sin(az)  )*x + (  cos(ax) + cos(az)  )*y + (  -sin(ax)  )*z
#	o.location[2] = ( -sin(ay) )*x + (  sin(ax)  )*y + ( cos(ax) + cos(ay)  )*z
	echo(['AFTERrotate', a,[ax,ay,az],o.location])	
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
	#bpy.context.active_object.data.update(calc_edges=True, calc_tessface=True)	
	bpy.context.scene.update()	
	return o	

# booleanOp is used by union(), difference() and intersection()
# TODO: apply=False will require a fix to allow for later scaling, etc.
def booleanOp(objA, objB, boolOp='DIFFERENCE', apply=True):		
	#bpy.ops.object.select_all(action = 'DESELECT')
	#obj_A.select = True
	# circumvent problem with "CSG failed, exception degenerate edge, Unknown internal error in boolean"
	echo(["boolOp", boolOp])
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
	echo("boolOpEND")
	return objA

	
def union(o1,*objs, apply=True):
	res = o1
	for obj in objs:
		if obj != None:
			res = booleanOp(res,obj, boolOp='UNION', apply=apply)
	return res
		
# TODO: write some "debug" mode grouping instead of really diffing sub-tree
def difference(o1,o2,*objs, apply=True):
	return booleanOp(o1,union(o2,*objs), boolOp='DIFFERENCE', apply=apply)

#def difference(o1,*objs, apply=True):
#	res = o1
#	for obj in objs:
#		if obj != None:
#			res = booleanOp(res,obj, boolOp='DIFFERENCE', apply=apply)
#	return res

def intersection(o1,*objs, apply=True):
## Remark: cannot use union here!! need to intersect all...
	res = o1
	for obj in objs:
		if obj != None:
			res = booleanOp(res,obj, boolOp='INTERSECT', apply=apply)
	return res
	
# join as a (better?) alternative to union()
# apply is dummy to mock full union syntax
def join(o1,*objs, apply=True):
	bpy.ops.object.select_all(action = 'DESELECT')
	o1.select = True
	#cleanup_object(o1)
	o1.name = 'J('+o1.name
	bpy.context.scene.objects.active = o1
	for obj in objs:
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

# OpenSCAD: rotate_extrude(convexity = <val>[, $fn = ...]){...}
# This emulation would also swallow 3D objects ;-)
# params to emulate rotate_extrude of OpenSCAD, 2D object in XY plane
# Wiki on Blender Spin: http://de.wikibooks.org/wiki/Blender_Dokumentation:_Spin_und_SpinDup
def rotate_extrude(o=None, fn=-1):	
	segments = fn if fn != -1 else blenderscad.fn # globals()["fn"]
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
	#	o.color = blenderscad.defColor
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


