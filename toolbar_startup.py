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

filepath ="O:/BlenderStuff/blenderscad/toolbar.py"

global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file: 
	exec(compile(file.read(), filepath, 'exec'), global_namespace);
