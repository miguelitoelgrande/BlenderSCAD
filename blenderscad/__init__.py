# blenderscad - Init the core functionality
# by Michael Mlivoncic, 2013

#import os
import bpy


#default layers for all objects
mylayers = [False]*20
mylayers[0] = True

mat = None

def main():
	global mat, matTrans, defColor, fa, fs, fn
	# need to setup our default material
	mat = bpy.data.materials.get('useObjectColor')
	if mat is None:
		mat=bpy.data.materials.new('useObjectColor')
		mat.use_object_color=1		
	# for Grouping, "invisible", but selectable :-)
	# need to be in "Texture" Display mode...
	matTrans = bpy.data.materials.get('Transparent')
	if matTrans is None:
		matTrans=bpy.data.materials.new('Transparent')
		matTrans.use_transparency=True
		matTrans.transparency_method='Z_TRANSPARENCY'
		matTrans.alpha = 0.0	
	# some colors... 
	#black = (0.00,0.00,0.00,0)
	#yellow = (1.00,1.00,0.00,0)
	# for full color list:
	#sys.path.append("<path to>/BlenderSCAD") 
	#from blenderscad_colors import *
	# default color for object creators below...
	defColor = (1.0,1.0,0.1,0)
	#Emulate OpenSCAD Special variables  blenderscad.{fs,fa,fn}
	#$fa - minimum angle  $fn = 360 / $fa    / default: $fa = 12 -> segments = 30
	fa=12;
	#$fs - minimum size   default: 1 
	fs=1;
	#$fn - number of fragments  | override of $fa/$fs , default = 0 , example: 36-> every 10 degrees
	fn=0;
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
# ####################################################################
# # This block helps during developmentas it reloads the blenderscad modules which are already present
# # and may have changed...
# # can be commented out or removed if you do not modify blenderscad libs during this blender session.
# import imp; import sys
# rel = ['blenderscad','blenderscad.math',
# 'blenderscad.core', 'blenderscad.primitives','blenderscad.impexp', 'blenderscad.shapes']
# for mo in rel:
	# if mo in sys.modules.keys():
		# print ('reloading: '+mo+' -> '+ sys.modules[mo].__file__)
		# imp.reload(sys.modules[mo])
# ####################################################################


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
	if blenderscad.mat is None:	
		blenderscad.main()
	# >>> print( dir(blenderscad.primitives))		
	public_prim = [ 'circle', 'cube', 'cylinder', 'mylayers', 'polygon', 'polyhedron', 'sphere', 'square']		
	for name in public_prim:
		nsdict.update({name: getattr(blenderscad.primitives, name)  })	
	#
	public_core = [  'listAllObjects', 'clearAllObjects', 'color', 'echo', 'str'
	                 ,  'difference', 'union', 'intersection', 'join', 'group'
					 , 'resize', 'rotate', 'mirror', 'translate', 'scale'
	                 , 'hull', 'linear_extrude', 'rotate_extrude', 'projection'
					 , 'remove_duplicates', 'round_edges', 'cut'
					# call those more explicitly... blendercad.core.* 
					# ,'booleanOp', 'remesh','cleanup_object', 'dissolve', ''
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
	
			 
			 
if __name__ == "__main__":
	main()
	
	




