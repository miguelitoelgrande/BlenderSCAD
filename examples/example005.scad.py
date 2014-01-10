# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 


import blenderscad 

blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
#clearAllObjects()

###### End of Header ##############################################################################

def example005():
	def sub():
		res=None
		for i in range (0,6):
			echo(360*i/6, sin(360*i/6)*80, cos(360*i/6)*80)
			o=translate([sin(360*i/6)*80, cos(360*i/6)*80, 0 ],
				cylinder(h = 200, r=10) )
			res=union(o,res)
		return res

	translate([0, 0, -120],
		union(	
	        difference(
	            cylinder(h = 50, r = 100)
	          , translate([0, 0, 10], cylinder(h = 50, r = 80) )
	          , translate([100, 0, 35], cube(50, center = true) )
	        )    
	        , sub() # need to factor the for loop out.
	        ,translate([0, 0, 200],
		        cylinder(h = 80, r1 = 120, r2 = 0) )
		)	        
     ) 

example005()

###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)

