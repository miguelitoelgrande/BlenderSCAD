## Adding a BlenderSCAD QuickAccess panel to the 3D view.
## by Michael Mlivoncic
## E.g. create to primitives and perform Boolean Difference with 3 clicks!
## Plus, to test some "Modifier" Macros
##
## To ease the tasks for beginners, all operations _appear_ to happen in
## Object mode, so no explicit mode switiching required. I.e. each "click"
## will end up in Object-Mode, even if started in Edit-Mode! :)
##
## TODO: should probably go to the scripts/startup folder
# for the moment, I use a script within the .blend file to call this.
import bpy


## Location: %USERPROFILE$\AppData\Roaming\Blender Foundation\Blender\2.69\scripts\startup\toolbar.py
#import sys
#sys.path.append("O:/BlenderStuff") 

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

###############################
class VIEW3D_OT_blenderscad_color(bpy.types.Operator):
	bl_idname = "view3d.blenderscad_color"
	bl_label = "color"
	bl_description = "Shortcut to init material to object color"
	
	def execute(self, context):
		o = context.object
#		if blenderscad.mat.name not in o.data.materials.keys():
#			o.data.materials.append(blenderscad.mat)
		blenderscad.core.color(rands(0,1,3),o)
		return {'FINISHED'}

class VIEW3D_OT_blenderscad_remesh(bpy.types.Operator):
	bl_idname = "view3d.blenderscad_remesh"
	bl_label = "remesh"
	bl_description = "Shortcut to remesh"	
	def execute(self, context):
		o = context.object
		blenderscad.core.remesh(o)
		return {'FINISHED'}

class VIEW3D_OT_blenderscad_subdivide(bpy.types.Operator):
	bl_label = "subdivide"; bl_idname = "view3d.blenderscad_subdivide"
	bl_description = "Shortcut to subdivide operator"	
	def execute(self, context):
		o = context.object
		blenderscad.core.cleanup_object(o, subdivide=True)
		return {'FINISHED'}

class VIEW3D_OT_blenderscad_beautify(bpy.types.Operator):
	bl_label = "remesh";	bl_idname = "view3d.blenderscad_beautify"
	bl_description = "Blender's beautify operator"	
	def execute(self, context):
		o = context.object
		blenderscad.core.cleanup_object(o, beautify=True)
		return {'FINISHED'}


class VIEW3D_OT_blenderscad_dissolve(bpy.types.Operator):
	bl_label = "dissolve";	bl_idname = "view3d.blenderscad_dissolve"
	bl_description = "Try to cleanup geometry using 'limited dissolve'"	
	def execute(self, context):
		o = context.object
		blenderscad.core.dissolve(o)
		return {'FINISHED'}

class VIEW3D_OT_blenderscad_decimate(bpy.types.Operator):
	bl_label = "decimate";	bl_idname = "view3d.blenderscad_decimate"
	bl_description = "Shortcut to decimate"	
	def execute(self, context):
		o = context.object
		blenderscad.core.decimate(o)
		return {'FINISHED'}
	
class VIEW3D_OT_blenderscad_hull(bpy.types.Operator):
	bl_label = "hull"; bl_idname = "view3d.blenderscad_hull"
	bl_description = "Use Hull-operator and swallow all selected objects..."	
	def execute(self, context):
		o = context.object
		sel=bpy.context.selected_objects
		blenderscad.core.hull(sel[0],*sel[1:])
		return {'FINISHED'}	

class VIEW3D_OT_blenderscad_debug(bpy.types.Operator):
	bl_label = "debug"; bl_idname = "view3d.blenderscad_debug"
	bl_description = "Show all edges in object mode (toggle)"	
	def execute(self, context):
		o = context.object
		if bpy.context.active_object.mode is not 'OBJECT': 
			bpy.ops.object.mode_set(mode = 'OBJECT')	
		o.show_wire = False if o.show_wire else True
		o.show_all_edges = True
		o.show_name = True
		o.show_x_ray = False
		return {'FINISHED'}	

class VIEW3D_OT_blenderscad_difference(bpy.types.Operator):
	bl_label = "difference"; bl_idname = "view3d.blenderscad_difference"
	bl_description = "Apply boolean DIFFERENCE operation to selected objects"		
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=bpy.context.active_object
		o1.select=False
		sel=bpy.context.selected_objects
		blenderscad.core.difference(o1,*sel,apply=True)
		return {'FINISHED'}	

class VIEW3D_OT_blenderscad_intersection(bpy.types.Operator):
	bl_label = "intersection"; bl_idname = "view3d.blenderscad_intersection"
	bl_description = "Apply boolean INTERSECTION operation to selected objects"
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=bpy.context.active_object
		o1.select=False
		sel=bpy.context.selected_objects
		blenderscad.core.intersection(o1,*sel,apply=True)
		return {'FINISHED'}	

class VIEW3D_OT_blenderscad_union(bpy.types.Operator):
	bl_label = "union"; bl_idname = "view3d.blenderscad_union"
	bl_description = "Apply boolean UNION operation to selected objects"	
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=bpy.context.active_object
		o1.select=False
		sel=bpy.context.selected_objects
		blenderscad.core.union(o1,*sel,apply=True)
		return {'FINISHED'}	

class VIEW3D_OT_blenderscad_group(bpy.types.Operator):
	bl_label = "group"; bl_idname = "view3d.blenderscad_group"
	bl_description = "Shortcut to group objects"	
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=bpy.context.active_object
		o1.select=False
		sel=bpy.context.selected_objects
		blenderscad.core.group(o1,*sel)
		return {'FINISHED'}	
	
class VIEW3D_OT_blenderscad_ungroup(bpy.types.Operator):
	bl_label = "ungroup"; bl_idname = "view3d.blenderscad_ungroup"
	bl_description = "Shortcut to ungroup objects"	
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=bpy.context.active_object
		o1.select=False
		sel=bpy.context.selected_objects
		print("not implemented yet: VIEW3D_OT_blenderscad_ungroup")
		#blenderscad.core.ungroup(o1)
		return {'FINISHED'}	

class VIEW3D_OT_blenderscad_copy(bpy.types.Operator):
	bl_label = "copy"; bl_idname = "view3d.blenderscad_copy"
	bl_description = "Copy/Paste = CTRL+C , CTRL+V, maybe more touch device friendly :-)"	
	def execute(self, context):
		bpy.ops.view3d.copybuffer() # CTRL+C
		bpy.ops.view3d.pastebuffer() # CTRL+V
		return {'FINISHED'}	



########################################################
bpy.utils.register_class(VIEW3D_OT_blenderscad_color)
bpy.utils.register_class(VIEW3D_OT_blenderscad_remesh)
bpy.utils.register_class(VIEW3D_OT_blenderscad_subdivide)
bpy.utils.register_class(VIEW3D_OT_blenderscad_beautify)
bpy.utils.register_class(VIEW3D_OT_blenderscad_dissolve)
bpy.utils.register_class(VIEW3D_OT_blenderscad_decimate)
bpy.utils.register_class(VIEW3D_OT_blenderscad_hull)
bpy.utils.register_class(VIEW3D_OT_blenderscad_union)
bpy.utils.register_class(VIEW3D_OT_blenderscad_difference)
bpy.utils.register_class(VIEW3D_OT_blenderscad_intersection)
bpy.utils.register_class(VIEW3D_OT_blenderscad_group)
bpy.utils.register_class(VIEW3D_OT_blenderscad_ungroup)
bpy.utils.register_class(VIEW3D_OT_blenderscad_debug)
bpy.utils.register_class(VIEW3D_OT_blenderscad_copy)
########################################################
#menu_func = (lambda self, context: self.layout.operator('OBJECT_OT_monkify'))
#bpy.types.VIEW3D_PT_tools_objectmode.prepend(menu_func)

# BlenderSCAD QuickAccessToolbar :-)
class VIEW3D_PT_blenderscad_qat(bpy.types.Panel):
	"""BlenderSCADPanel for the Viewport Toolbar"""
	bl_label = "BlenderSCAD Quick Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'

	def draw(self, context):
		layout = self.layout

		row = layout.row()
		row.label(text="Add Objects:")

		split = layout.split()
		col = split.column(align=True)

		col.operator("mesh.primitive_cube_add", text="Cube", icon='MESH_CUBE')
		col.operator("mesh.primitive_cylinder_add", text="Cylinder", icon='MESH_CYLINDER')
		col2 = split.column(align=True)
		col2.operator("mesh.primitive_uv_sphere_add", text="Sphere", icon='MESH_UVSPHERE')
		col2.operator("mesh.primitive_cone_add", text="Cone", icon='MESH_CONE')
#	 col.operator("mesh.primitive_torus_add", text="Torus", icon='MESH_TORUS')

		#################################################
		row = layout.row()
		row.label(text="Operations:")
		split = layout.split()
		col = split.column(align=True)
		col2 = split.column(align=True)

		col.operator("view3d.blenderscad_color", text="Colorize", icon='COLOR')
		col.operator("view3d.blenderscad_debug", text="ShowEdges", icon='WIRE')  # WIRE
		col.operator("view3d.blenderscad_dissolve", text="CleanUp", icon='SAVE_PREFS') # MOD_BOOLEAN
		col.operator("view3d.blenderscad_remesh", text="Remesh", icon='MOD_REMESH')
		col.operator("view3d.blenderscad_decimate", text="Decimate", icon='MOD_DECIM')
		col.operator("view3d.blenderscad_beautify", text="Beautify", icon='SCENE_DATA')
		col.operator("view3d.blenderscad_subdivide", text="Subdivide", icon='OUTLINER_OB_LATTICE')		
		col2.operator("view3d.blenderscad_hull", text="Hull", icon='MOD_SUBSURF')
		col2.operator("view3d.blenderscad_union", text="Union", icon='ROTATECOLLECTION')
		col2.operator("view3d.blenderscad_difference", text="Difference", icon='ROTACTIVE')
		col2.operator("view3d.blenderscad_intersection", text="Intersect", icon='ROTATECENTER')

		col2.operator("view3d.blenderscad_group", text="Group", icon='GROUP')
		col2.operator("view3d.blenderscad_ungroup", text="UnGroup", icon='STICKY_UVS_DISABLE')

		#join, group, Difference , Union, 
		col2.operator("view3d.blenderscad_copy", text="Duplicate", icon='GHOST')
		#col.operator("wm.console_toggle()", text="Console (Win)", icon='CONSOLE')
# Icons and ideas for further functions:
#RETOPO , CONSOLE, WIRE,  MOD_BEVEL  SCENE_DATA
# group/ungroup: STICKY_UVS_LOC, STICKY_UVS_DISABLE LINK_AREA
#MOD_SKIN, CONSTRAINT_DATA  MOD_MIRROR  MOD_ARRAY MOD_BOOLEAN
#WORLD_DATA   MOD_SCREW  ORTHO MOD_LATTICE MOD_SOLIDIFY
#Link: CONSTRAINT_DATA
#Project, Mirror,  MOD_UVPROJECT   MOD_MIRROR
# cleanup/repair:  HELP RECOVER_AUTO SAVE_PREFS
#Struktur... MESH_ICOSPHERE MOD_LATTICE  OUTLINER_OB_MESH
# Undo/Redo: LOOP_BACK  LOOP_FORWARDS

		#################################################	

		row = layout.row()
		#type = ob.type.capitalize()	
		#row = col.row()
		ob = context.object
		if ob is not None:
			row.label(text="Selected Object: "+ob.name)
			row = layout.row()
			#row = col.row()		
			if ob.type == 'MESH':
				row.label(text="Verts: "+str(len(ob.data.vertices))+" / Faces: "+str(len(ob.data.polygons)) )
			else:
				row.label(text="it is a "+str(type)+".")


def register():
	import blenderscad
	bpy.utils.register_class(VIEW3D_PT_blenderscad_qat)
	#bpy.utils.unregister_class(BlenderSCADPanel)

def unregister():
	bpy.utils.unregister_class(VIEW3D_PT_blenderscad_qat)

if __name__ == "__main__":
	register()