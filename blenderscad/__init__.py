# blenderscad - Init the core functionality
# by Michael Mlivoncic, 2013

#import os
import bpy


#default layers for all objects
mylayers = [False]*20
mylayers[0] = True

# need to setup our default material
mat = bpy.data.materials.get('useObjectColor')
if mat is None:
	mat=bpy.data.materials.new('useObjectColor')
	mat.use_object_color=1
	

# some colors... 
#black = (0.00,0.00,0.00,0)
#yellow = (1.00,1.00,0.00,0)
# for full color list:
#sys.path.append("<path to>/BlenderSCAD") 
#from blenderscad_colors import *

# default color for object creators below...
defColor = (1.0,1.0,0.1,0)

# emulate OpenSCAD $fn
fn=36  # default precision: every 10 degrees a segment..

#TODO: OpenSCAD Special variables
#$fa - minimum angle  $fn = 360 / $fa    / default: $fa = 12 -> segments = 30
#$fs - minimum size   default: 1 
#$fn - number of fragments  | override of $fa/$fs , default = 0 


if bpy.context.active_object is not None:
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')
	
# from blenderscad.colors import *
# from blenderscad.math import * 
# from blenderscad.core import *
# from blenderscad.primitives import *
# from blenderscad.impexp import * # import, export, surface

# "reload()" is not reliable, especially with "from ... import *"
# better using exec(compile(...)) instead while developing the modules..
# import imp
# imp.reload(blenderscad.core)
# imp.reload(blenderscad.primitives)

# from blenderscad.core import *
# from blenderscad.primitives import *


# init blenderscad in current namespace, so no need to type blenderscad.cube()
# similar to exported functions of a module....
def initns(nsdict):
	import sys
	import blenderscad
	import blenderscad.colors
	import blenderscad.math
	import blenderscad.core	
	import blenderscad.primitives
	import blenderscad.impexp
	#import blenderscad.shapes
	try:
		import __builtin__
	except ImportError:
		import builtins as __builtin__ #Python 3.0
	
	# all colors -> expecting nothing private in color file..
	for name in dir(blenderscad.colors):
		if name.find("__") < 0 and name !="bpy":
			nsdict.update({name: getattr(blenderscad.colors, name)  })			
	#
	# >>> print( dir(blenderscad.primitives))
	public_prim = [ 'circle', 'cube', 'cylinder', 'mat', 'mylayers', 'polygon', 'polyhedron', 'sphere', 'square']
	for name in public_prim:
		nsdict.update({name: getattr(blenderscad.primitives, name)  })	
	#
	public_core = [  'listAllObjects', 'clearAllObjects', 'color', 'echo', 'str'
	                 ,  'difference', 'union', 'intersection', 'join', 'group'
					 , 'resize', 'rotate', 'mirror', 'translate', 'round_edges', 'scale'
	                 , 'hull', 'linear_extrude', 'rotate_extrude', 'remesh'	, 'remove_duplicates'
					# 'booleanOp', 'cleanup_object'
				]
	for name in public_core:		    
		nsdict.update({name: getattr(blenderscad.core, name)  })
	#>>> print( dir(blenderscad.math))
	public_math = [  'true','false', 'rands','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'exp', 'floor', 'ln'
					, 'log', 'lookup', 'math', 'pi', 'sign', 'sin', 'sqrt', 'tan']
	for name in public_math:	
		nsdict.update({name: getattr(blenderscad.math, name)  })
	#		
	public_impexp = [  'export', 'export_dxf', 'export_stl', 'fill_object', 'import_', 'import_dxf', 'import_stl', 'surface']
	for name in public_impexp:	
		nsdict.update({name: getattr(blenderscad.impexp, name)  })					
	#
	#print("Registered all public BlenderSCAD functions to namespace")
	
			 
			 

	
	
	




