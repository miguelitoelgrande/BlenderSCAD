#####################################################################
## BlenderSCAD Import/Export functions -  including "surface()"
# 
## by Michael Mlivoncic, 2013
#

import bpy 
import blenderscad
#from blenderscad import *  # contains blenderscad core, primitives, math and colors


#mat = blenderscad.mat
	
	
# OpenSCAD: import_stl("filename.stl", convexity = <val>);
# TODO: implement convexity...
def import_stl(file , layer="", convexity=10):
	bpy.ops.import_mesh.stl(filepath=file)
	o = bpy.context.active_object
	o.data.materials.append(blenderscad.mat)
	o.color = blenderscad.defColor
	return o

#import_stl("O:/BlenderStuff/demo.stl")

#helper to fill imported dxf -> before linear extrude?
def fill_object(o):
	if bpy.context.active_object.mode is not 'EDIT':
		bpy.ops.object.mode_set(mode = 'EDIT')	
	for el in o.data.vertices: el.select = True
	for el in o.data.edges: el.select = True
	try:  # not a clean implementation, but should work for triangular shapes, holes, squares,etc
		bpy.ops.mesh.fill_grid()
	except RuntimeError:
		bpy.ops.mesh.fill() 	
	bpy.ops.mesh.flip_normals()
	#bpy.ops.mesh.edge_face_add() # add face...wrong results for polygones with holes...
	bpy.ops.object.mode_set(mode = 'OBJECT')
	return o

# OpenSCAD: import_dxf() ...
def import_dxf(file, layer="", convexity=10, fill=True):
	import io_import_scene_dxf
	io_import_scene_dxf.theCodec = 'ascii'
	sections = io_import_scene_dxf.readDxfFile(file)
	print("Building geometry")
	io_import_scene_dxf.buildGeometry(sections['ENTITIES'].data)
	o = bpy.context.scene.objects.active
	if fill is True:
		fill_object(o)
	return o

#o = import_dxf("O:/BlenderStuff/test.dxf")
#linear_extrude(10, o)

#todo: 
# OpenSCAD: import(file)
# A string containing the path to the STL or DXF file.
# TODO: convexity, layer?
def import_(file, convexity=10, layer=""):
	import os.path
	extension = os.path.splitext(file)[1].lower()
	o =None
	if extension == '.dxf':
		return import_dxf(file)
	if extension == '.stl':
		return import_stl(file)
	return None

#import_("O:/BlenderStuff/test.dxf")
#import_("O:/BlenderStuff/test.stl")
		
	
# extra function, not OpenSCAD
# export object as STL.
def export_stl(filename, o=None, ascii=False):
	if o is None:
		o = bpy.context.active_object
	bpy.ops.export_mesh.stl(filepath=filename, ascii=ascii)
	return o

#export_stl("O:/BlenderStuff/demo.stl", cube([10,20,15]) )


def export_dxf(filename, o=None, ascii=False):
	if o is None:
		o = bpy.context.active_object
	import io_export_dxf.export_dxf
	# 	### TODO TODO: these settings dont lead to an export...
	# http://fossies.org/dox/blender-2.69/export__dxf_8py_source.html
	settings = {'onlySelected': False , 'verbose': True, 'projectionThrough': None , 'entitylayer_from':'obj.name'
				, 'entitycolor_from': 'obj.color' , 'entityltype_from':'BYBLOCK', 'mesh_as': True}
	#
	io_export_dxf.export_dxf.exportDXF( bpy.context, filePathDXF, settings )
	return o

	
def export(file, o=None):
	if o is None:
		o = bpy.context.active_object
	import os.path
	extension = os.path.splitext(file)[1].lower()
	if extension == '.dxf':
		return export_dxf(file)
	if extension == '.stl':
		return export_stl(file)

#export("O:/BlenderStuff/export.dxf")
#export("O:/BlenderStuff/export.stl")
		

##################
# BlenderSCAD: surface operator
# ported from OpenSCAD by Michael Mlivoncic
## ------------------------------------------
# Credits: surface is ported from surface code of OpenSCAD
def surface(file, center=False, convexity=1):	
	l=0 ; data=[]; rows=0; cols=0; 
	min_val=0.0;
	ins = open( file , "r" )
	for line in ins:
		row = []
		vals = line.split()
		l+=1
		for val in vals :
			if val[0] == "#":
				l -= 1
				break
			row.append(float(val))
			min_val = min(float(val)-1, min_val);
			# TODO: will only work if comments are first line token...
			if len(vals)>cols: cols=len(vals)
		if val[0] != "#":
			data.append(row); rows +=1;
	ins.close()
	print("importing surface ",file,": rows=",rows," cols=",cols)
	ox = -(cols-1)/2.0 if center else 0;
	oy = -(rows-1)/2.0 if center else 0;
	#
	points=[]; faces=[]; pc=0; # pointCounter
	# Block 1: Surface (top) of object
	for i in range(1, rows):  # 1.. rows-1
		#echo(str("row",i));
		for j in range(1, cols):			
			v1 = data[i-1][j-1];
			v2 = data[i-1][j];
			v3 = data[i][j-1];
			v4 = data[i][j];
			vx = (v1 + v2 + v3 + v4) / 4.0;
			#
			faces.append( [pc+2,pc+1,pc] );	pc+=3; # polyhedron has clockwise orientation (OpenSCAD)	
			points.append( [ox + j-1, oy + i-1, v1] );
			points.append( [ox + j, oy + i-1, v2] );
			points.append( [ox + j-0.5, oy + i-0.5, vx] );
			#
			faces.append( [pc+2,pc+1,pc] );	pc+=3; 		
			points.append( [ox + j, oy + i-1, v2] );
			points.append( [ox + j, oy + i, v4] );
			points.append( [ox + j-0.5, oy + i-0.5, vx] );
			#
			faces.append( [pc+2,pc+1,pc] );	pc+=3; 	
			points.append( [ox + j, oy + i, v4] );
			points.append( [ox + j-1, oy + i, v3] );
			points.append( [ox + j-0.5, oy + i-0.5, vx] );
			#
			faces.append( [pc+2,pc+1,pc] );	pc+=3;
			points.append( [ox + j-1, oy + i, v3] );
			points.append( [ox + j-1, oy + i-1, v1] );
			points.append( [ox + j-0.5, oy + i-0.5, vx] );
	# Block 2: left and right side walls
	for i in range(1, rows):  # 1.. rows-1  # left wall
		faces.append( [pc+3,pc+2,pc+1,pc] ); pc+=4; # clockwise orientation!
		points.append( [ox + 0, oy + i-1, min_val]);        
		points.append( [ox + 0, oy + i-1, data[i-1][0] ]);
		points.append( [ox + 0, oy + i,  data[i][0] ]);
		points.append( [ox + 0, oy + i, min_val] );
		#
		faces.append( [pc,pc+1,pc+2,pc+3] ); pc+=4;
		points.append( [ox + cols-1, oy + i-1, min_val] );
		points.append( [ox + cols-1, oy + i-1, data[i-1][cols-1] ] );
		points.append( [ox + cols-1, oy + i, data[i][cols-1] ] );
		points.append( [ox + cols-1, oy + i, min_val ] ); 
	# Block 3: front and back side walls
	for i in range(1, cols):  # 1.. cols-1   # front wall
		faces.append( [pc,pc+1,pc+2,pc+3] ); pc+=4; # p->append_poly();
		points.append( [ox + i-1, oy + 0, min_val] );
		points.append( [ox + i-1, oy + 0, data[0][i-1] ] );
		points.append( [ox + i, oy + 0, data[0][i] ]);
		points.append( [ox + i, oy + 0, min_val] );
		#
		faces.append( [pc+3,pc+2,pc+1,pc] ); pc+=4; # back wall, clockwise orient.!!
		points.append( [ox + i-1, oy + rows-1, min_val] );
		points.append( [ox + i-1, oy + rows-1, data[rows-1][i-1] ] );
		points.append( [ox + i, oy + rows-1, data[rows-1][i] ] );
		points.append( [ox + i, oy + rows-1, min_val ] );
	# Block 4: bottom side of  the object	(z-Axis is on "min_val")	
	# need to connect all floor edge points to make the shape "watertight", not just four corners.
	ptsOld=len(points) # num points so far
	for i in range(0, cols-1):  # i=0.. <cols-1
		points.append( [ox + i, oy + 0, min_val ] );
	for i in range(0, rows-1):  # i=0.. <rows-1
		points.append( [ox + cols-1, oy + i, min_val ] );
	for i in range(cols-1,0,-1):
		points.append( [ox + i, oy + rows-1, min_val ] );
	for i in range(rows-1,0,-1):
		points.append( [ox + 0, oy + i, min_val ] );
	pts = len(points)-ptsOld #number of points inserted in last block
	# should be 2x (rows-1) + 2* (cols-1)
	#print("pts:",pts)
	faces.append( list(range(pc,pc+pts)) )
	#faces.append( range(pc+pts-1,pc-1,-1) ) # test reverse order -> wrong orientation of bottom
	#
	# result reuses the polyhedron implementation...
	# 
	#polyhedron(points = [ [0, -10, 60], [0, 10, 60], [0, 10, 0] ], faces = [ [0,3,2] ]  )
	o = blenderscad.primitives.polyhedron(points , faces)
	#cleanup_object(o,removeDoubles=False)	
	#blenderscad.core.remove_duplicates()
	return o

## ------------------------------------------

# use folder where the .dxf fuile is located
#import os; os.chdir("O:/BlenderStuff/examples")

#surface.scad
#surface(file = "../surface.dat", center = true, convexity = 5);
#translate([0,0,5])cube([10,10,10], center =true);

#surface(file = "example010.dat", center = true, convexity = 5)

