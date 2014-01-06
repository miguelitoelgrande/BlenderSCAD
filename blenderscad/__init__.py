# blenderscad - Init the core functionality
# by Michael Mlivoncic, 2013

#import os


import bpy

# some colors... 
#black = (0.00,0.00,0.00,0)
#yellow = (1.00,1.00,0.00,0)
# for full color list:
#sys.path.append("<path to>/BlenderSCAD") 
#from blenderscad_colors import *

# default color for object creators below...
defColor = (1.0,1.0,0.1,0)

# emulate OpenSCAD $fn
fn=32  # default precision: every 10 degrees a segment..

if bpy.context.active_object is not None:
	if bpy.context.active_object.mode is not 'OBJECT': 
		bpy.ops.object.mode_set(mode = 'OBJECT')

		
from blenderscad.colors import *
from blenderscad.math import * 
from blenderscad.core import *
from blenderscad.primitives import *

import imp
imp.reload(blenderscad.core)
imp.reload(blenderscad.primitives)

from blenderscad.core import *
from blenderscad.primitives import *




