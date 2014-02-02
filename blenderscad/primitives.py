#####################################################################
## BlenderSCAD Primitives
#
## by Michael Mlivoncic, 2013
#
import bpy
#import bpy_types

from mathutils import Vector

import blenderscad # for "global" variables fn, defColor,...
#from blenderscad.math import *  # true, false required...

mylayers=blenderscad.mylayers
#mat=blenderscad.mat
	
# Construct a cube mesh 
# bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def cube(size=(1.0,1.0,1.0), center=False):
	if type(size) == int:    # support for single size value argument
		size=(size,size,size)
	if type(size) == float:    # support for single size value argument
		size=(size,size,size)		
	bpy.ops.mesh.primitive_cube_add(location=(0.0,0.0,0.0), layers=mylayers)
	#o = bpy.data.objects['Cube']  # not safe enough if an earlier object named 'Cube' exists...
	o = bpy.context.active_object
	o.select = True
	o.dimensions=size
	bpy.ops.object.transform_apply(scale=True)  
	o.name='cu' # +str(index)
	o.data.name='cu'
	# simple color will only display via my def. Material setting
	o.data.materials.append(blenderscad.mat)
	# just some default color
	o.color = blenderscad.defColor
	o.draw_type='SOLID'
	# scale
	#bpy.ops.transform.resize(value=size)
	#bpy.ops.object.transform_apply(scale=True)
	if (center==False):
		#bpy.ops.transform.translate(value=(size[0]/2.0,size[1]/2.0,size[2]/2.0)) # causes "convertViewVec: called in an invalid context"
		o.location += Vector( (size[0]/2.0,size[1]/2.0,size[2]/2.0) )
		bpy.ops.object.transform_apply(location=True) 
	return o

# Construct a cylinder mesh
# bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=2.0, end_fill_type='NGON', view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def _cylinder(h=1, r=1, segments=36):
	#segments = fn if fn != -1 else blenderscad.fn # globals()["fn"]
	bpy.ops.mesh.primitive_cylinder_add(location=(0.0,0.0,0.0), radius=r , depth=h , vertices=segments, layers=mylayers)  
	#o = bpy.data.objects['Cylinder'] # not safe enough if an earlier object named 'Cylinder' exists...
	o = bpy.context.active_object
	o.name='cy' # +str(index)   
	o.data.name='cy'
	return o

# Construct a conic mesh 
#  bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=1.0, radius2=0.0, depth=2.0, end_fill_type='NGON', view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def _cone(h=1, r1=1, r2=2, segments=36):
	#segments = fn if fn != -1 else blenderscad.fn # globals()["fn"]
	bpy.ops.mesh.primitive_cone_add(location=(0.0,0.0,0.0), radius1=r1, radius2=r2, depth=h , vertices=segments, layers=mylayers)
	#o = bpy.data.objects['Cone'] # not safe enough if an earlier object named 'Cone' exists...
	o = bpy.context.active_object
	o.name='cn' # +str(index)
	o.data.name='cn'
	return o

# OpenSCAD: cylinder(h = <height>, r1 = <bottomRadius>, r2 = <topRadius>, center = <boolean>);
#	   cylinder(h = <height>, r = <radius>);
def cylinder(h = 1, r=1, r1 = -1, r2 = -1, center = False, d=-1, d1=-1, d2=-1, fn=None, fs=None, fa=None):
	if d != -1:
		r = d / 2.0;
	if d1 != -1 and d2 != -1 :
		r1 = d1 / 2.0 ; r2 = d2 / 2.0;				
	if r1 != -1 and r2 != -1 :
		segments=blenderscad.core.get_fragments_from_r( r=min(r1,r2), fn=fn, fs=fs, fa=fa )
		o =_cone(h,r1,r2,segments)
	else:
		segments=blenderscad.core.get_fragments_from_r( r=r, fn=fn, fs=fs, fa=fa )
		o =_cylinder(h,r,segments)
	# just a suitable default material and some default color
	o.data.materials.append(blenderscad.mat)
	o.color = blenderscad.defColor
	o.draw_type='SOLID'
	if center==False:
		#bpy.ops.transform.translate(value=(0.0,0.0,h/2.0))  # causes "convertViewVec: called in an invalid context"
		o.location += Vector( (0.0,0.0,h/2.0)  )
		bpy.ops.object.transform_apply(location=True) 
	return o


# OpenSCAD: sphere(r=1, d=-1)   
# bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, size=1.0, view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False,   
def sphere(r=1, d=-1, center=True,  fn=None, fs=None, fa=None):
	if d != -1 :
		  r= d/2;
	segments=blenderscad.core.get_fragments_from_r( r=r, fn=fn, fs=fs, fa=fa )
	bpy.ops.mesh.primitive_uv_sphere_add(size=r , segments=segments, ring_count=segments,location=(0.0,0.0,0.0), layers=mylayers)
	#o = bpy.data.objects['Sphere'] # not safe enough if an earlier object named 'Sphere' exists...
	o = bpy.context.active_object
	o.name='sp' # +str(index)
	o.data.name='sp'
	# simple color will only display via my def. Material setting
	o.data.materials.append(blenderscad.mat)
	# just some default color
	o.color = blenderscad.defColor
	o.draw_type='SOLID'
	# scale
	#bpy.ops.transform.resize(value=size)
	#bpy.ops.object.transform_apply(scale=True)
	return o

# Construct a circle
## OpenSCAD: circle(r = <val>);
def circle(r=10.0, d=-1, fill=False, center=True, fn=None, fs=None, fa=None):
	if d != -1 :
		  r= d/2;
	segments=blenderscad.core.get_fragments_from_r( r=r, fn=fn, fs=fs, fa=fa )
	if fill is False:    
		fill_type = 'NOTHING'
	else:
		fill_type = 'NGON'	 #  fill_type (enum in [
	bpy.ops.mesh.primitive_circle_add(vertices=segments, radius=r, fill_type=fill_type, location=(0.0,0.0,0.0), layers=mylayers)
	#bpy.ops.curve.primitive_bezier_circle_add(radius=r, location=(0.0,0.0,0.0), layers=mylayers)
	#o = bpy.data.objects['Cube']  # not safe enough if an earlier object named 'Cube' exists...
	o = bpy.context.active_object
	o.name='ci' # +str(index)
	o.data.name='ci'
	o.data.materials.append(blenderscad.mat)
	o.color = blenderscad.defColor
	o.draw_type='SOLID'
	return o
	

# OpenSCAD: polygon(points = [[x, y], ... ], paths = [[p1, p2, p3..], ... ], convexity = N);
# TODO: http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects
# fill seems to cause probs with rotate_extrude in some cases. ->faces at start/end
def polygon(points, paths=[], fill=True):
	# Create mesh and object
	me = bpy.data.meshes.new('p')
	o = bpy.data.objects.new('p', me)
	o.data.materials.append(blenderscad.mat)
	o.color = blenderscad.defColor
	o.draw_type='SOLID'
	o.location = (0.0,0.0,0.0)
	o.show_name = True
	bpy.context.scene.objects.link(o) 	# Link object to scene
	verts=[] 
	for p in points:
		verts.append([p[0],p[1],0])
	edges = []
	if len(paths)== 0: # need to create path, opposite order to display correctly in Blender.
		edges.append([0,len(points)-1])		
		for i in range (len(points)-2,-1,-1): # range (0, len(points)-1):
			edges.append([i+1,i])
	else:
		for p in paths:
			edges.append([p[0],p[len(p)-1]])		
			#print([p[0],p[i+1]])
			for i in range(len(p)-2,-1,-1):
				edges.append([p[i+1],p[i]])		
				#print([p[i+1],p[i]])	
#			for i in range(0, len(p)-1):
#				#print([p[i],p[i+1]])
#				edges.append([p[i],p[i+1]])		
#			#print([p[i],p[0]])
#			edges.append([p[i+1],p[0]])							
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
#	me.update(calc_edges=True)		
	bpy.context.scene.objects.active = o
	o.select = True
	# Note: switching mode would fail before mesh is defined and object selected...
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')	
#	for el in o.data.vertices: el.select = True
#	for el in o.data.edges: el.select = True
	if fill is True:
		bpy.ops.mesh.fill()
#		seems like the more complicated version not needed after properly defining edge direction..		
#		try:  # not a clean implementation, but should work for triangular shapes, holes, squares,etc
#			bpy.ops.mesh.fill_grid()
#		except RuntimeError:
#			bpy.ops.mesh.fill() 	
	#bpy.ops.mesh.flip_normals() ## want to avoid this for higher level functions (extrude...)
	#bpy.ops.mesh.edge_face_add() # add face...wrong results for polygones with holes...
	bpy.ops.object.mode_set(mode = 'OBJECT')
	#bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
	#bpy.context.scene.cursor_location = (5,5,0)
	# having this as a curve to reuse in rotate_extrude...
	#bpy.ops.object.convert(target='CURVE')
	return o

## triangle
#polygon(points=[ [8,-8],[8,8],[-8,8] ])
# triangle with two triangular holes...
#polygon(points=[[0,0],[100,0],[0,100],[5,5],[30,5],[5,30],[25,25],[25,60],[60,25]], paths=[[3,4,5],[0,1,2],[6,7,8]], fill=true)



# OpenSCAD 2D convenience  square(size,center) ,  square([width,height],center)
def square(size=(1.0,1.0), center=False, fill=False):
	if type(size) == int:    # support for single size value argument
		size=(size,size)
	if type(size) == float:    # support for single size value argument
		size=(size,size)
	if center== True:
		x1=-size[0]/2.0; y1=-size[1]/2.0; x2=size[0]/2.0; y2=size[1]/2.0; 
	else:
		x1=0; y1=-0; x2=size[0]; y2=size[1]; 
	points=[ [x1,y1],[x2,y1],[x2,y2],[x1,y2] ]				
	return polygon(points, paths=[[0,1,2,3]], fill = fill)

#square ([2,2],center = true);
#square (2,center = false, fill=true);
#square ([2,6],center = true);


#OpenSCAD polyhedron()
#polyhedron(points = [ [x, y, z], ... ], faces = [ [p1, p2, p3..], ... ], convexity = N);
#polyhedron(points = [ [x, y, z], ... ], triangles = [ [p1, p2, p3..], ... ], convexity = N);
#DEPRECATED: polyhedron(triangles=[]) will be removed in future releases. Use polyhedron(faces=[]) instead
def polyhedron(points, faces=[], triangles=[], fill=False):
	if len(triangles)>0 and len(faces) == 0:
		print("DEPRECATED: polyhedron(triangles=[]) will be removed in future releases. Use polyhedron(faces=[]) instead")
		faces=triangles
	# Create mesh and object
	me = bpy.data.meshes.new('p')
	o = bpy.data.objects.new('p', me)
	o.data.materials.append(blenderscad.mat)
	o.color = blenderscad.defColor
	o.draw_type='SOLID'
	o.location = (0.0,0.0,0.0)
	o.show_name = True
	bpy.context.scene.objects.link(o) 	# Link object to scene
	#print({'points': points} ,  {'faces': faces} )	
	for face in faces: # need to reverse polygon vertex order from OpenSCAD->Blender logic...
		face.reverse()
	me.from_pydata(points, [], faces) # Create mesh fromverts, edges, faces. Use edges OR faces to avoid problems  
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
		bpy.ops.mesh.fill() 
#		try:  # not a clean implementation, but should work for triangular shapes, holes, squares,etc
#			bpy.ops.mesh.fill_grid()
#		except RuntimeError:
#			bpy.ops.mesh.fill() 	
#	bpy.ops.mesh.flip_normals()  # blender treats normals the other way around than OpenSCAD...
	#bpy.ops.mesh.edge_face_add() # add face...wrong results for polygones with holes...
	bpy.ops.object.mode_set(mode = 'OBJECT')
	return o


	
	