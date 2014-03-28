# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "BlenderSCAD toolbar",
    "author": "Michael Mlivoncic",
    "version": (0, 0, 2),
    "blender": (2, 70, 0),
    "location": "Tools Panel",
    "description": "Proof of concept UI mod for Thinkercad/OpenSCAD like operations",
    "wiki_url": "https://github.com/miguelitoelgrande/BlenderSCAD",
    "tracker_url": "https://github.com/miguelitoelgrande/BlenderSCAD",
    "category": "Object"}


import bpy
import os

# uncomment the following two lines to the path where your "blenderscad" module folder will be
# (other than Blender's default location for modules)
import sys
#sys.path.append("O:/BlenderStuff") 


#filepath ="O:/BlenderStuff/blenderscad/toolbar.py"
#global_namespace = {"__file__": filepath, "__name__": "__main__"}
#with open(filepath, 'rb') as file: 
#	exec(compile(file.read(), filepath, 'exec'), global_namespace);

	
settings = {
    }	


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
import blenderscad.colors
import blenderscad.math
import blenderscad.core	
import blenderscad.primitives
import blenderscad.impexp
#from blenderscad.shapes import *	# optional 

#blenderscad.initns(globals()) # to avoid prefixing all calls, we make "aliases" in current namespace

###############################
class VIEW3D_OT_blenderscad_select_bsgroup(bpy.types.Operator):
	bl_idname = "view3d.blenderscad_select_bsgroup"
	bl_label = "select_bsgroup"
	bl_description = "Select a whole (BlenderSCAD) grouping when any child is selected (i.e. redirect to root)"
	

	def invoke(self, context, event):
		#context.window_manager.modal_handler_add(self)
		location=( event.mouse_region_x , event.mouse_region_y );
		#print (location);
		oldsel=bpy.context.selected_objects;
		#print(oldsel);
		bpy.ops.view3d.select(location=location, toggle=False, extend=False, deselect=False,  center=False, enumerate=False, object=False )
		change=bpy.context.selected_objects;
		#print(change);
		for o in oldsel: # restore old selection in addition
			o.select = True		
		for o in change:
			root=blenderscad.core.get_root(o);		
			if root != o: # real root											
				#print (("root=",root,"o=",o));
				o.select=False
				root.select = (root not in oldsel); # toggle selection 
			else:
				o.select = (o not in oldsel); # toggle selection
			context.scene.objects.active = bb = root
		return {'RUNNING_MODAL'}	
		
# iteratively traverse tree.. not required anymore.				
#			nlist=[]
#			nlist.append(root)
#			while len(nlist)>0:
#				node=nlist.pop()
#				node.select=selState
#				#print(node.name);
#				for c in node.children:
#					nlist.insert(0,c);
#			#if o.parent is not None: o.parent.select=True

#	def execute(self, context):
#		cursorLoc = bpy.context.scene.cursor_location
#		bpy.ops.view3d.select(extend=False, deselect=False, toggle=False, center=False, enumerate=False, object=False, location=(0, 0))
#		for o in bpy.context.selected_objects:
#			if o.parent is not None: o.parent.select=True
#		#######################		
#		#blenderscad.core.apply2objects(bpy.context.selected_objects, colorize_func, True)				
#		return {'FINISHED'}

###################################

#	Left Mouse Multiselect - For tablet devices :-)
class VIEW3D_OT_blenderscad_multiselect(bpy.types.Operator):
	bl_idname = "view3d.blenderscad_multiselect"
	bl_label = "multiselect"
	bl_description = "Override select behaviour to 'toggle' to  allow for multi-object-selections"
	
	def execute(self, context):
		#keyMap = bpy.context.window_manager.keyconfigs.active.keymaps['3D View'] # does not activate changes?
		keyMap = bpy.context.window_manager.keyconfigs.user.keymaps['3D View']
		for item in keyMap.keymap_items:
			#if item.id==99:
			#	print( [item.active, item.id, item.name, item.idname, item.map_type, item.type, item.propvalue] );
			#	# [True, 99, 'Activate/Select', 'view3d.select', 'MOUSE', 'SELECTMOUSE', 'NONE']
			#	print( [item.any, item.shift, item.ctrl, item.alt, item.oskey ] );
			#	# [False, False, False, False, False]
			#	dict(item.properties)
			#	# {'toggle': 0, 'deselect': 0, 'extend': 0, 'center': 0, 'object': 0, 'enumerate': 0}			
			if [item.name, item.idname, item.map_type, item.type, item.propvalue] == [ 'Activate/Select', 'view3d.select', 'MOUSE', 'SELECTMOUSE', 'NONE'] and [item.any, item.shift, item.ctrl, item.alt, item.oskey ] ==  [False, False, False, False, False]:
					#print("BINGO!");
					setattr(item.properties, 'toggle', False==getattr(item.properties,'toggle') )	
					#dict(item.properties)
					#item.active=False
		return {'FINISHED'}					
	
			

class VIEW3D_OT_blenderscad_colorTEST(bpy.types.Operator):
	bl_idname = "view3d.blenderscad_color"
	bl_label = "color"
	bl_description = "Shortcut to init material to object color"
	
	def execute(self, context):
		if blenderscad.mat is None:
			blenderscad.main()		
		#o = context.object		
#	  if blenderscad.mat.name not in o.data.materials.keys():
#		  o.data.materials.append(blenderscad.mat)
		#blenderscad.core.color(blenderscad.math.rands(0,1,3),o)
		global rndcol
		rndcol=blenderscad.math.rands(0,1,3)
		#######################
		def colorize_func(o):
			global rndcol
			blenderscad.core.color(rndcol,o)
			return o;
		#######################		
		blenderscad.core.apply2objects(bpy.context.selected_objects, colorize_func, True)				
		return {'FINISHED'}

class VIEW3D_OT_blenderscad_color(bpy.types.Operator):
	bl_idname = "view3d.blenderscad_color"
	bl_label = "color"
	bl_description = "Shortcut to init material to object color"
	
	def execute(self, context):
		if blenderscad.mat is None:
			blenderscad.main()		
		#o = context.object		
#	  if blenderscad.mat.name not in o.data.materials.keys():
#		  o.data.materials.append(blenderscad.mat)
#
		# new paradigm: handle selections in operator, groupings in core functions
		# as they should behave caller side as "atomic" objects. The specific knows how to handle it.
		rgba=blenderscad.math.rands(0,1,3);
		for o in context.selected_objects:
			blenderscad.core.color(rgba,o);
		return {'FINISHED'}

		
class VIEW3D_OT_blenderscad_hole(bpy.types.Operator):
	bl_label = "hole"; bl_idname = "view3d.blenderscad_hole"
	bl_description = "Declare selected objects/groupings as being 'holes' in future groupings"  
	def execute(self, context):		
		for o in context.selected_objects:
			blenderscad.core.hole(o);
		return {'FINISHED'}  		

			
class VIEW3D_OT_blenderscad_group(bpy.types.Operator):
	bl_label = "group"; bl_idname = "view3d.blenderscad_group"
	bl_description = "Shortcut to group objects" 
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=bpy.context.active_object
		o1.select=False
		sel=bpy.context.selected_objects
		# TODO: rework group with "empty" object as bounding box/parent -> resolves cyclic dependencies with bool modifiers...
		blenderscad.core.group(o1,*sel)
		return {'FINISHED'}  
	
class VIEW3D_OT_blenderscad_ungroup(bpy.types.Operator):
	bl_label = "ungroup"; bl_idname = "view3d.blenderscad_ungroup"
	bl_description = "Shortcut to ungroup objects"  
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=bpy.context.active_object
		#o1.select=False
		#sel=bpy.context.selected_objects
		blenderscad.core.ungroup(o1)
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
	bl_label = "remesh"; bl_idname = "view3d.blenderscad_beautify"
	bl_description = "Blender's beautify operator"  
	def execute(self, context):
		o = context.object
		blenderscad.core.cleanup_object(o, beautify=True)
		return {'FINISHED'}

class VIEW3D_OT_blenderscad_dissolve(bpy.types.Operator):
	bl_label = "dissolve";  bl_idname = "view3d.blenderscad_dissolve"
	bl_description = "Try to cleanup geometry using 'limited dissolve'"  
	def execute(self, context):
		o = context.object
		blenderscad.core.dissolve(o)
		return {'FINISHED'}

class VIEW3D_OT_blenderscad_round(bpy.types.Operator):
	bl_label = "round";  bl_idname = "view3d.blenderscad_round"
	bl_description = "Utilize bevel operator to round corners of selected object" 
	def execute(self, context):
		o = context.object 
		round_edges(width=5.0, segments=8, verts_only=False, angle_limit=math.radians(45),o=o, apply=True )
		return {'FINISHED'}
		
		
class VIEW3D_OT_blenderscad_decimate(bpy.types.Operator):
	bl_label = "decimate";  bl_idname = "view3d.blenderscad_decimate"
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
		o1=context.active_object
		o1.select=False
		sel=bpy.context.selected_objects
		if len(sel)<1 or o1 is None:			
			return  {'FINISHED'}		
		res=blenderscad.core.difference(o1,*sel,apply=False)
		#res.select=True; # to be on the safe side...
		return {'FINISHED'}  

class VIEW3D_OT_blenderscad_intersection(bpy.types.Operator):
	bl_label = "intersection"; bl_idname = "view3d.blenderscad_intersection"
	bl_description = "Apply boolean INTERSECTION operation to selected objects"
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=context.active_object
		o1.select=False # removes o1 from objs list
		sel=context.selected_objects
		if len(sel)<1 or o1 is None:			
			return  {'FINISHED'}
		res=blenderscad.core.intersection(o1,*sel,apply=False)
		#res.select=True; # to be on the safe side...
		return {'FINISHED'}  

class VIEW3D_OT_blenderscad_union(bpy.types.Operator):
	bl_label = "union"; bl_idname = "view3d.blenderscad_union"
	bl_description = "Apply boolean UNION operation to selected objects" 
	def execute(self, context):
		# we need the active object of selection separately as "main" object"
		o1=context.active_object
		o1.select=False
		sel=context.selected_objects
		if len(sel)<1 or o1 is None:			
			return  {'FINISHED'}		
		res=blenderscad.core.union(o1,*sel,apply=False)
		#res.select=True; # to be on the safe side...
		return {'FINISHED'}  



class VIEW3D_OT_blenderscad_clone(bpy.types.Operator):
	bl_label = "clone"; bl_idname = "view3d.blenderscad_clone"
	bl_description = "Clone all selected objects incl. groups/hierarchies"  
	def execute(self, context):
		#bpy.ops.view3d.copybuffer() # CTRL+C
		#bpy.ops.view3d.pastebuffer() # CTRL+V
		blenderscad.core.clone(bpy.context.selected_objects);
		return {'FINISHED'}  

class VIEW3D_OT_blenderscad_destruct(bpy.types.Operator):
	bl_label = "destruct"; bl_idname = "view3d.blenderscad_destruct"
	bl_description = "DELETE all selected objects incl. groups/hierarchies"  
	def execute(self, context):
		for o in context.selected_objects:
			blenderscad.core.destruct(o);
		return {'FINISHED'}  

		

########################################################
bpy.utils.register_class(VIEW3D_OT_blenderscad_multiselect)
bpy.utils.register_class(VIEW3D_OT_blenderscad_color)
bpy.utils.register_class(VIEW3D_OT_blenderscad_debug)
bpy.utils.register_class(VIEW3D_OT_blenderscad_dissolve)
bpy.utils.register_class(VIEW3D_OT_blenderscad_round)
bpy.utils.register_class(VIEW3D_OT_blenderscad_remesh)
bpy.utils.register_class(VIEW3D_OT_blenderscad_decimate)
bpy.utils.register_class(VIEW3D_OT_blenderscad_beautify)
bpy.utils.register_class(VIEW3D_OT_blenderscad_subdivide)

bpy.utils.register_class(VIEW3D_OT_blenderscad_group)
bpy.utils.register_class(VIEW3D_OT_blenderscad_ungroup)
bpy.utils.register_class(VIEW3D_OT_blenderscad_hole)
bpy.utils.register_class(VIEW3D_OT_blenderscad_hull)
bpy.utils.register_class(VIEW3D_OT_blenderscad_union)
bpy.utils.register_class(VIEW3D_OT_blenderscad_difference)
bpy.utils.register_class(VIEW3D_OT_blenderscad_intersection)

bpy.utils.register_class(VIEW3D_OT_blenderscad_clone)
bpy.utils.register_class(VIEW3D_OT_blenderscad_destruct)

bpy.utils.register_class(VIEW3D_OT_blenderscad_select_bsgroup)


########################################################
#menu_func = (lambda self, context: self.layout.operator('OBJECT_OT_monkify'))
#bpy.types.VIEW3D_PT_tools_objectmode.prepend(menu_func)

# BlenderSCAD QuickAccessToolbar :-)
class VIEW3D_PT_blenderscad_qat(bpy.types.Panel):
	"""BlenderSCADPanel for the Viewport Toolbar"""
	bl_label = "BlenderSCAD Quick Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	## Own Tab for Blender 2.70
	bl_category = "BlenderSCAD"
	
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
#	col.operator("mesh.primitive_torus_add", text="Torus", icon='MESH_TORUS')

		#################################################
		row = layout.row()
		row.label(text="Operations:")
		split = layout.split()
		col = split.column(align=True)
		col2 = split.column(align=True)
		
		col.operator("ed.undo", text="Undo", icon='LOOP_BACK')		
		col2.operator("ed.redo", text="Redo", icon='LOOP_FORWARDS')		
		
		col.operator("view3d.blenderscad_multiselect", text="MultiSelect", icon='STICKY_UVS_LOC' )
		#col2.prop(scn, 'MyInt', icon='STICKY_UVS_LOC', toggle=True) # TODO: Toggle-Button would be nicer...
		col.operator("view3d.blenderscad_color", text="Colorize", icon='COLOR')		
		col.operator("view3d.blenderscad_debug", text="ShowEdges", icon='WIRE')  # WIRE
		col.operator("view3d.blenderscad_dissolve", text="CleanUp", icon='SAVE_PREFS') # MOD_BOOLEAN
		col.operator("view3d.blenderscad_round", text="Round", icon='MOD_BEVEL') # MOD_BOOLEAN
		col.operator("view3d.blenderscad_remesh", text="Remesh", icon='MOD_REMESH')
		col.operator("view3d.blenderscad_decimate", text="Decimate", icon='MOD_DECIM')
		col.operator("view3d.blenderscad_beautify", text="Beautify", icon='SCENE_DATA')
		col.operator("view3d.blenderscad_subdivide", text="Subdivide", icon='OUTLINER_OB_LATTICE')		
			
		col2.operator("view3d.blenderscad_hole", text='"Hole"', icon='UGLYPACKAGE')	# TODO: better icon for "hole"
		col2.operator("view3d.blenderscad_group", text="Group", icon='GROUP')
		col2.operator("view3d.blenderscad_ungroup", text="UnGroup", icon='STICKY_UVS_DISABLE')
		
		col2.operator("view3d.blenderscad_hull", text="Hull", icon='MOD_SUBSURF')
		col2.operator("view3d.blenderscad_union", text="Union", icon='ROTATECOLLECTION')
		col2.operator("view3d.blenderscad_difference", text="Difference", icon='ROTACTIVE')
		col2.operator("view3d.blenderscad_intersection", text="Intersect", icon='ROTATECENTER')
		
		col2.operator("view3d.blenderscad_clone", text="Clone", icon='GHOST')		
		col2.operator("view3d.blenderscad_destruct", text="Destruct", icon='RADIO')	

		#join, group, Difference , Union, 
		#col.operator("wm.console_toggle()", text="Console (Win)", icon='CONSOLE')
# Icons and ideas for further functions:
#RETOPO , CONSOLE, WIRE,  MOD_BEVEL  SCENE_DATA
# group/ungroup: STICKY_UVS_LOC, STICKY_UVS_DISABLE LINK_AREA
#MOD_SKIN, CONSTRAINT_DATA  MOD_MIRROR  MOD_ARRAY MOD_BOOLEAN
#WORLD_DATA	MOD_SCREW  ORTHO MOD_LATTICE MOD_SOLIDIFY
#Link: CONSTRAINT_DATA
#Project, Mirror,  MOD_UVPROJECT	MOD_MIRROR
# cleanup/repair:  HELP RECOVER_AUTO SAVE_PREFS
#Structure... MESH_ICOSPHERE MOD_LATTICE  OUTLINER_OB_MESH

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



# # Funktioniert:
# import io_import_scene_dxf
# bpy.types.INFO_MT_file_import.remove(io_import_scene_dxf.menu_func)
# import io_export_dxf
# bpy.types.INFO_MT_file_export.remove(io_export_dxf.menu_func)
# import io_scene_3ds
# bpy.types.INFO_MT_file_import.remove(io_scene_3ds.menu_func_import)
# bpy.types.INFO_MT_file_export.remove(io_scene_3ds.menu_func_export)
# # Test: add entry to different Menu
# bpy.types.VIEW3D_MT_object.append(io_scene_3ds.menu_func_import)
# bpy.types.VIEW3D_MT_object.append(io_scene_3ds.menu_func_import)
# # Test: add _ALL_ entries from help menu directly into Object menu..
# bpy.types.VIEW3D_MT_object.append( bpy.types.INFO_MT_help.draw)
# #bpy.types.VIEW3D_MT_object.append(bl_ui.space_view3d.VIEW3D_MT_object_quick_effects.draw)
# bpy.types.VIEW3D_MT_object.append(bpy.types.VIEW3D_MT_object_quick_effects.draw)
# ## remove again:
# bpy.types.VIEW3D_MT_object.remove(bl_ui.space_view3d.VIEW3D_MT_object_quick_effects.draw)
# bpy.types.VIEW3D_MT_object.remove( bpy.types.INFO_MT_help.draw)
# # !! Empty Game menu...
# bpy.types.VIEW3D_MT_object_game.remove( bpy.types.VIEW3D_MT_object_game.draw)
# # mehrmals aufrufen: leert komplettes Objects menu:
# bpy.types.VIEW3D_MT_object.remove(  bpy.types.VIEW3D_MT_object._dyn_ui_initialize()[0] )
# # !!! clear(),pop()) auf liste -> macht menu auch leer
# bpy.types.VIEW3D_MT_select_object.draw._draw_funcs.clear()
# print(bpy.types.VIEW3D_MT_view.draw._draw_funcs.pop())
# >>> print(bpy.types.VIEW3D_MT_view.draw._draw_funcs.pop())
# <function VIEW3D_MT_view.draw at 0x00000000084FE8C8>


# bpy.types.VIEW3D_MT_object.remove( bpy.ops.object.move_to_layer)

# bpy.types.VIEW3D_MT_select_object.remove(bpy.types.VIEW3D_OT_select_border)
# bpy.types.VIEW3D_MT_select_object.remove(VIEW3D_OT_select_menu.draw)


# print ( getattr( bpy.types.VIEW3D_MT_object.draw, "_draw_funcs").remove() )

# for f in  getattr( bpy.types.VIEW3D_MT_view.draw, "_draw_funcs"): print (f);	


# stripped down Object menu from draw() in class VIEW3D_MT_object(Menu) / space_view3d.py
def MyObjectMenu_draw(self, context):
	layout = self.layout
	layout.operator("ed.undo")
	layout.operator("ed.redo")
	layout.operator("ed.undo_history")

	layout.separator()

	layout.menu("VIEW3D_MT_transform_object")
	layout.menu("VIEW3D_MT_mirror")
	layout.menu("VIEW3D_MT_object_clear")
	layout.menu("VIEW3D_MT_object_apply")
	layout.menu("VIEW3D_MT_snap")

	#layout.separator()
	#layout.menu("VIEW3D_MT_object_animation")

	layout.separator()

	layout.operator("object.duplicate_move")
	layout.operator("object.duplicate_move_linked")
	layout.operator("object.delete", text="Delete...")
	layout.operator("object.proxy_make", text="Make Proxy...")
	layout.menu("VIEW3D_MT_make_links", text="Make Links...")
	layout.operator("object.make_dupli_face")
	#layout.operator_menu_enum("object.make_local", "type", text="Make Local...")
	#layout.menu("VIEW3D_MT_make_single_user")

	layout.separator()

	layout.menu("VIEW3D_MT_object_parent")
	layout.menu("VIEW3D_MT_object_track")
	layout.menu("VIEW3D_MT_object_group")
	layout.menu("VIEW3D_MT_object_constraints")

	layout.separator()
	#layout.menu("VIEW3D_MT_object_quick_effects")
	#layout.separator()
	#layout.menu("VIEW3D_MT_object_game")
	#layout.separator()
	layout.operator("object.join")
	layout.separator()
	#layout.operator("object.move_to_layer", text="Move to Layer...")
	layout.menu("VIEW3D_MT_object_showhide")

	layout.operator_menu_enum("object.convert", "target")
	
# Same as the Panel, just as menu (to assign shortcuts..)	
class VIEW3D_MT_blenderscad(bpy.types.Menu):
	bl_label = "BlenderSCAD"
	def draw(self, context):	
		# My stuff...
		layout = self.layout
		layout.operator("mesh.primitive_cube_add", text="Cube", icon='MESH_CUBE')
		layout.operator("mesh.primitive_cylinder_add", text="Cylinder", icon='MESH_CYLINDER')
		layout.operator("mesh.primitive_uv_sphere_add", text="Sphere", icon='MESH_UVSPHERE')
		layout.operator("mesh.primitive_cone_add", text="Cone", icon='MESH_CONE')
		#	col.operator("mesh.primitive_torus_add", text="Torus", icon='MESH_TORUS')
		layout.separator()
		layout.separator()
		#row.label(text="Operations:")
		layout.operator("view3d.blenderscad_color", text="Colorize", icon='COLOR')
		layout.operator("view3d.blenderscad_debug", text="ShowEdges", icon='WIRE')  # WIRE
		layout.operator("view3d.blenderscad_dissolve", text="CleanUp", icon='SAVE_PREFS') # MOD_BOOLEAN
		layout.operator("view3d.blenderscad_round", text="Round", icon='MOD_BEVEL') # MOD_BOOLEAN
		layout.operator("view3d.blenderscad_remesh", text="Remesh", icon='MOD_REMESH')
		layout.operator("view3d.blenderscad_decimate", text="Decimate", icon='MOD_DECIM')
		layout.operator("view3d.blenderscad_beautify", text="Beautify", icon='SCENE_DATA')
		layout.operator("view3d.blenderscad_subdivide", text="Subdivide", icon='OUTLINER_OB_LATTICE')		
		layout.operator("view3d.blenderscad_copy", text="Duplicate", icon='GHOST')	 
		layout.operator("view3d.blenderscad_hull", text="Hull", icon='MOD_SUBSURF')
		layout.operator("view3d.blenderscad_union", text="Union", icon='ROTATECOLLECTION')
		layout.operator("view3d.blenderscad_difference", text="Difference", icon='ROTACTIVE')
		layout.operator("view3d.blenderscad_intersection", text="Intersect", icon='ROTATECENTER')

		layout.operator("view3d.blenderscad_group", text="Group", icon='GROUP')
		layout.operator("view3d.blenderscad_ungroup", text="UnGroup", icon='STICKY_UVS_DISABLE')
#################

def default_keymap(enable=False):
	keyMap = bpy.context.window_manager.keyconfigs.active.keymaps['3D View'] # does not activate changes?
	#keyMap = bpy.context.window_manager.keyconfigs.user.keymaps['3D View']
	for item in keyMap.keymap_items:
		#if item.id==99:
		#	print( [item.active, item.id, item.name, item.idname, item.map_type, item.type, item.propvalue] );
		#	# [True, 99, 'Activate/Select', 'view3d.select', 'MOUSE', 'SELECTMOUSE', 'NONE']
		#	print( [item.any, item.shift, item.ctrl, item.alt, item.oskey ] );
		#	# [False, False, False, False, False]
		#	dict(item.properties)
		#	# {'toggle': 0, 'deselect': 0, 'extend': 0, 'center': 0, 'object': 0, 'enumerate': 0}			
		if [item.name, item.idname, item.map_type, item.type, item.propvalue] == [ 'Activate/Select', 'view3d.select', 'MOUSE', 'SELECTMOUSE', 'NONE'] and [item.any, item.shift, item.ctrl, item.alt, item.oskey ] ==  [False, False, False, False, False]:
			#print("BINGO!");
			setattr(item.properties, 'toggle', False==getattr(item.properties,'toggle') )	
			#dict(item.properties)
			item.active=enable
			return item;

# store keymap item here to access after registration
kmi=None
orig_obj_menu=None		
		
def register():
	import blenderscad
	bpy.utils.register_class(VIEW3D_PT_blenderscad_qat)
	#bpy.utils.unregister_class(BlenderSCADPanel)
	#TODO:
    #bpy.types.VIEW3D_MT_object.append(menu_func)
	#
	#disable default keymap for Mouse-Select in 3D view first...
	default_keymap(enable=False);
	# handle the keymap
	global kmi;
	km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
	kmi = km.keymap_items.new(VIEW3D_OT_blenderscad_select_bsgroup.bl_idname, 'SELECTMOUSE', 'PRESS', ctrl=False, shift=False)	
	# TODO: define my own properties here
	#kmi.properties.toggle = True 
	#
	# As a goodie, try to cleanup "Object"-Menu..
	global orig_obj_menu;
	orig_obj_menu = bpy.types.VIEW3D_MT_object.draw;
	bpy.types.VIEW3D_MT_object.remove(  bpy.types.VIEW3D_MT_object.draw )
	bpy.types.VIEW3D_MT_object.draw._draw_funcs.clear()	
	#bpy.types.VIEW3D_MT_object.remove(  MyObjectMenu_draw )	
	bpy.types.VIEW3D_MT_object.append(  MyObjectMenu_draw )		

def unregister():
	bpy.utils.unregister_class(VIEW3D_PT_blenderscad_qat)
	#TODO:
	#bpy.types.VIEW3D_MT_object.remove(menu_func)
	#
	# handle the keymap
	global kmi;
	km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']	
	km.keymap_items.remove(kmi)
	#enable default keymap for Mouse-Select in 3D view first...
	default_keymap(enable=True);
	#
	# restore original "Object"-Menu:
	global orig_obj_menu;
	bpy.types.VIEW3D_MT_object.remove(  MyObjectMenu_draw )	
	bpy.types.VIEW3D_MT_object.append( orig_obj_menu )	

	
# for faster testing of enable/disable addon:
#bpy.ops.wm.addon_enable(module="blenderscad_toolbar")
#bpy.ops.wm.addon_disable(module="blenderscad_toolbar")

#bpy.ops.wm.addon_disable(module="blenderscad_toolbar"); bpy.ops.wm.addon_enable(module="blenderscad_toolbar"); 

	
if __name__ == "__main__":
	register()
#	bpy.types.VIEW3D_MT_object.remove(  bpy.types.VIEW3D_MT_object.draw )
#	bpy.types.VIEW3D_MT_object.draw._draw_funcs.clear()	
#	#bpy.types.VIEW3D_MT_object.remove(  MyObjectMenu_draw )	
#	bpy.types.VIEW3D_MT_object.append(  MyObjectMenu_draw )	
# TODO: Own Blenderscad Menu?
#	bpy.utils.register_class(VIEW3D_MT_blenderscad)
#	bpy.types.VIEW3D_HT_header.remove(  VIEW3D_MT_blenderscad.draw )
#	bpy.types.VIEW3D_HT_header.prepend( VIEW3D_MT_blenderscad.draw )

