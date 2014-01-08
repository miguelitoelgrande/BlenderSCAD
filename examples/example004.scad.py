# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 

from mathutils import Vector  # using Vector type below...

import blenderscad 
from blenderscad import *  # contains blenderscad core, primitives, math and colors

## Clear the open .blend file!!!
#clearAllObjects()

## ------------------------------------------


def example004():

    difference(
        cube(30, center = true)
      , sphere(20)
    )    
    

example004()


