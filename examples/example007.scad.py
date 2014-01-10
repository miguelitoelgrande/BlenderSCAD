# OpenSCAD example, ported by Michael Mlivoncic

#import sys
#sys.path.append("O:/BlenderStuff") 


import blenderscad 

import imp
imp.reload(blenderscad)
imp.reload(blenderscad.core)
imp.reload(blenderscad.primitives)

blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
#clearAllObjects()

###### End of Header ##############################################################################

import os
# use folder where the .dxf fuile is located
os.chdir("O:/BlenderStuff/examples")

def cutout():
	return intersection(	
			rotate(90, [1, 0, 0],
			translate([0, 0, -50],
			linear_extrude(height = 100, convexity = 1, o=
				import_dxf(file = "example007.dxf", layer = "cutout1")
			)))		
			,
			rotate(90, [0, 0, 1],
			rotate(90, [1, 0, 0],
			translate([0, 0, -50],
			linear_extrude(height = 100, convexity = 2, o=
				import_dxf(file = "example007.dxf", layer = "cutout2")
			))))
		)

def clip():
	def for_sub():
		tmp = None
		for r in range(0, 91):
			o = rotate(r, [0, 0, 1], cutout() )
			tmp = union(o,tmp)
		return tmp
			
	return difference(
		# NB! We have to use the deprecated module here since the "dorn"
		# layer contains an open polyline, which is not yet supported
		# by the import() module.
		rotate_extrude(import_dxf(
			file = "example007.dxf",
			layer="dorn",
			convexity = 3))
		, for_sub()
	)		
	

def cutview():
	return difference(	
		difference(		
			translate([0, 0, -10], clip())			
			, rotate(20, [0, 0, 1],
				rotate(-20, [0, 1, 0],
					translate([18, 0, 0],
						cube(30, center = true))))
		)			
		#render(convexity = 5) 
		,intersection(
			translate([0, 0, -10], clip())
			, rotate(20, [0, 0, 1],
				rotate(-20, [0, 1, 0],
					translate([18, 0, 0],
						cube(30, center = true))))
		)
	)	
	
		
	
translate([0, 0, -10], clip() )

#cutview()


###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)

