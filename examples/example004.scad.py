# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 

import blenderscad 

blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
#clearAllObjects()

###### End of Header ##############################################################################

def example004():

    difference(
        cube(30, center = true)
      , sphere(20)
    )    
    

example004()

###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)


