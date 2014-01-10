# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 


import blenderscad 

# import imp
# imp.reload(blenderscad)
# imp.reload(blenderscad.core)
# imp.reload(blenderscad.primitives)
# imp.reload(blenderscad.impexp)

blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
#clearAllObjects()

###### End of Header ##############################################################################


## example012.stl is Mblock.stl, (c) 2009 Will Langford
## licensed under the Creative Commons - GNU GPL license.
## http://www.thingiverse.com/thing:753

import os
# use folder where the .dxf fuile is located
os.chdir("O:/BlenderStuff/examples")


difference(

    sphere(20)
  ,  
    translate([ -2.92, 0.5, +20 ], rotate([180, 0, 180],
    import_("example012.stl", convexity = 5)
    ))
)


	
###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)


