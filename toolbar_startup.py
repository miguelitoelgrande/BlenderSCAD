# obsolete and will be removed with next cleanup.
# put addons/blenderscad_toolbar.py in Blender scripts/addons folder instead

# This stub runs a python script relative to the currently open
# blend file, useful when editing scripts externally.

import bpy
import os

#############################################################
## Quick and Dirty: Click "Run Script" for the time being to 
## register the Panel!!!
#############################################################


# uncomment the following two lines to the path where your "blenderscad" module folder will be
# (other than Blender's default location for modules)
import sys
sys.path.append("O:/BlenderStuff") 

#see: http://www.blender.org/documentation/blender_python_api_2_61_0/info_tips_and_tricks.html
bpy.app.debug=True

filepath ="O:/BlenderStuff/blenderscad/toolbar.py"

global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file: 
	exec(compile(file.read(), filepath, 'exec'), global_namespace);

