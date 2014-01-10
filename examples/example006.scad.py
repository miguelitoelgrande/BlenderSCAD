# OpenSCAD example, ported by Michael Mlivoncic
# a beautiful dice...
# an interesting test case, to get the Boolean operations somehow fixed (TODO)


#import sys
#sys.path.append("O:/BlenderStuff") 


import blenderscad 

import imp
imp.reload(blenderscad)
imp.reload(blenderscad.core)
imp.reload(blenderscad.primitives)


blenderscad.initns( globals() ) # try to add BlenderSCAD names to current namespace .. as if they would be in this file...


## Clear the open .blend file!!!
clearAllObjects()

###### End of Header ##############################################################################


def example006():
	#
	def edgeprofile():
		objs = []
		# render(convexity = 2) 
		# difference BEGIN		
		o = cube([20, 20, 120], center = true) # instead of 150!!
#		objs.append( translate([-10, -10, 0],
#				cylinder(h = 100, r = 10.0, center = true)))	# align cylinder to sphere faces!!
#		
		objs.append( translate([-10, -10, 0],
				cylinder(h = 80.1, r = 10.0, center = true)))	# align cylinder to sphere faces!!
		objs.append( translate([-10, -10, +40], # fix: wireframe showed, 39 instead of 40 :-)  fixes also boolean prob
				sphere(r = 10)))	
		objs.append( translate([-10, -10, -40],  # 10.5 instead 10 , 39.999 instead -40 !!!
				sphere(r = 10)))	# instead 10..					
		o = difference(o,*objs,apply=True)			
		#o = union(o,*objs,apply=True)		
		# difference END	
		o.name="ep"
		return o
	#edgeprofile()
	#rttggthg
	#		
	#difference(	
	objs = [] ;
	o= cube(100, center = true)
	wiggle=0.0001 
	for rot in [ [0, 0, 0], [1, 0, 0], [0, 1, 0] ]:
		for p in [[+1, +1, 0], [-1, +1, 90], [-1, -1, 180], [+1, -1, 270]] :
			objs.append ( rotate(90, rot , translate([ p[0]*(50+wiggle), p[1]*(50+wiggle), 0 ], #49.999 instead 50
				rotate(p[2], [0, 0, 1],
					edgeprofile()))) 
			)			
	#import code
	#code.interact(local=locals())
	# Dice "spots"
	for i in [	[ 0, 0, [ [0, 0] ] ],
				[ 90, 0, [ [-20, -20], [+20, +20] ] ],
				[ 180, 0, [ [-20, -25], [-20, 0], [-20, +25], [+20, -25], [+20, 0], [+20, +25] ] ],
				[ 270, 0, [ [0, 0], [-25, -25], [+25, -25], [-25, +25], [+25, +25] ] ],
				[ 0, 90, [ [-25, -25], [0, 0], [+25, +25] ] ],
				[ 0, -90, [ [-25, -25], [+25, -25], [-25, +25], [+25, +25] ] ]
				] :
		for j in i[2]:
			objs.append(rotate(i[0], [0, 0, 1], rotate(i[1], [1, 0, 0], translate([0, -50, 0],
				translate([j[0], 0, j[1]], sphere(10))))) 
			)
	o = difference(o,*objs, apply=True)
	#o = union(o,*objs, apply=True)
	# "visual" ready: color change when finished...
	#o = union(o,*objs, apply=True)
	# end difference		

# careful: with this model, it seems to cause trouble with bools!
blenderscad.fn=24 #36

example006()

#cylinder(h = 80, r = 10, center = true)	# align cylinder to sphere faces!!
#sphere(r = 10)


###### Begin of Footer ##############################################################################
color(rands(0,1,3)) # random color last object. to see "FINISH" :-)

# print timestamp and finish - sometimes it is easier to see differences in console then :-)
import time
import datetime
st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
echo ("FINISH", st)

