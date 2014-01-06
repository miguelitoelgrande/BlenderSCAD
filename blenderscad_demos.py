# blenderscad.shapes
# Color name definitions as defined in OpenSCAD (and SVG)
# by Michael Mlivoncic, 2013
#

# if your blenderscad is NOT in the Blender module dir...
#  ( <path>/blender-2.69-windows64/2.69/scripts/modules/blenderscad)
# change this line to where your blenderscad is located (as a subdir)
##import sys
##sys.path.append("O:/BlenderStuff") 

from mathutils import *  # using Vector type below...

import blenderscad 
from blenderscad import *  # contains blenderscad core, primitives, math and colors
from blenderscad.shapes import *   # optional 

## List loaded blenderscad related (sub)modules
#for mod in sys.modules.values():
#	str1 = "|"+str(mod) + "|"
#	#if str1.startswith("<module 'blenderscad") is True:
#	if str1.find("blenderscad") >= 0:
#		print (mod)


# This block is just for debugging: to reload all blenderscad module 
#  which might have changed externally...
# can be commented out or removed if you do not modify blenderscad libs during this blender session.
# This was a bit easier when this all was in a single file ;-)
#import imp
#imp.reload(blenderscad)
#imp.reload(blenderscad.math)
#imp.reload(blenderscad.core)
#imp.reload(blenderscad.primitives)
#imp.reload(blenderscad.shapes)
#imp.reload(blenderscad.colors)
#### need to also redo the "import *" part...
#from blenderscad import *  # contains blenderscad core, primitives, math and colors
#from blenderscad.shapes import *   # optional 
###################


#str1 = "this is string example....wow!!!";
#str2 = "exam";
#
#print str1.find(str2);
#print str1.find(str2, 10);
#print str1.find(str2, 40);


#################################################################
## Tests
#################################################################   



clearAllObjects()


# changing global "environment variables"
#
blenderscad.fn=32  # emulate OpenSCAD's $fn
blenderscad.defColor=yellow


# TODO: search()
# http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#Search
# The search() function is a general-purpose function to find one or more (or all) occurrences of a value or list of values in a vector, string or more complex list-of-list construct.
#  search( match_value , string_or_vector [, num_returns_per_match [, index_col_num ] ] ); 

def search( match_value , string_or_vector , num_returns_per_match=1 , index_col_num=0 ):
	listindex = []
	i = string_or_vector.find(match_value)
	while i >= 0:
		listindex.append(i)
		i = string_or_vector.find(match_value, i + 1) 
	return listindex


echo (search("a","abcdabcd",0));  #--->   [[0,4]]
#  search(3,[ ["a",1],["b",2],["c",3],["d",4],["a",5],["b",6],["c",7],["d",8],["e",3] ], 0, 1);  -->  [2,8]




#	
# A few OpenSCAD like operations... need to substitute brackets
# note that operators like translate,color,scale,etc. can also be called on active object 
def OpenSCADtests():
	c0 = cube((5,7,4),center=true) 
	translate(v=(-8,-5,0))
	c1 = cube((5,10,4),center=true)
	translate(v=(10,20,20))
	color('blue') # note: color as string
	color(red,c0)  # note: color as variable plus object reference
	scale((5,9,4),c0)
	#   
	c0 = cube((12,12,4),center=true)
	c1 = cube((6,6,4),center=true)  
	color([0.0, 1, 0])  # green as value
	difference(c0,c1)
	translate(v=(1,2,2))
	#  and almost OpenSCAD like...
	translate([-20,-20,0] , cylinder(d1=10, d2=14, h=20, center=true) )
	difference (
			   color(purple,cube((12,12,4),center=true)), 
			   cube((6,6,4),center=true)
			   )
	translate([55,45,0])			
	#
	union (
			   color(green, cube((12,12,4),center=true) ), 
			   color(blue, cube((6,6,9),center=false) )
			   )
	translate([-55,45,0])			
	#
	color(lime, translate([50,0,-10] ,cylinder(h=10,r=2)))
	#
	translate([-50,20,10], cylinder(r=10,h=20) )
	translate([25,40,6], cylinder(r=10,h=20, center=true) )

#OpenSCADtests()

def HullDemo():
    return hull (
        translate([0,0,0], cylinder(r=4,h=4) )
        ,translate([20,0,0], cylinder(r=4,h=4) )
        ,translate([10,20,0], cylinder(r=4,h=4) )
    )    
#HullDemo() 



def HullDemo2():
	return scale( (0.5,0.5,0.5) ,rotate( (90,0,90) , hull ( union( sphere(r=4),
	#cylinder(r1=10,r2=20,h=20) 
	translate( (20,20,-10) , cylinder(r1=4,r2=8,h=20,center=true)   )
))))
#HullDemo2()


def Demo1():
	scale([5,5,5], translate([0,0,5],
		union(
			rotate( [90,0,90], cylinder(h=10,r=3,center=true) )   
		,   rotate( [90,0,0], cylinder(h=10,r=3, center=true) )  
		,   rotate( [0,0,90], cylinder(h=10,r=3, center=true) )   
	  )
	)) 

#Demo1()


# OpenJSCAD.org Logo :-)	  
def Demo2():  
	scale([10,10,10], 
	   translate([0,0,1.5] 
		 , group(   
			 color(purple, difference(
				 cube([3,3,3], center=true)
			   , sphere(r=2, center=true)
			 ))
		   , color(yellow, intersection(
				 sphere(r=1.3, center=true)
			   , cube([2.1,2.1,2.1], center=true)
		   ))	 
		 )
	 )
	)

Demo2()


# OpenJSCAD.org Logo :-)	  
def Demo2b_tripleGrouping():  
	scale([10,10,10], 
	   translate([0,0,1.5] 
		 , group(   
			 color(purple, difference(
				 cube([3,3,3], center=true)
			   , sphere(r=2, center=true)
			 ))
		   , color(yellow, intersection(
				 sphere(r=1.3, center=true)
			   , cube([2.1,2.1,2.1], center=true)
		   ))	 
		   , color(lime, cylinder(r=0.1,h=5,center=true))
		 )
	 )
	)
	  
#Demo2b_tripleGrouping()



def polygon_demo():
	# triangle
	polygon(points=[ [8,-8],[8,8],[-8,8] ])
	# single square, centered around origin
	polygon( points=[ [8,-8],[8,8],[-8,8],[-8,-8] ] , paths=[[0,1,2,3]])
	# some profile
	polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] )
	rotate([90,0,0],  polygon( points=[[0,0],[20,10],[10,20],[10,30],[30,40],[0,50]] ))
	# OpenSCAD example: double Triangle, using two paths...
	polygon(points=[[0,0],[50,0],[0,50],[5,5],[40,5],[5,40]], paths=[[0,1,2],[3,4,5]])
	# "Fish"
	polygon(points=[[0,0],[100,0],[0,100],[5,5],[40,5],[5,40],[45,45],[45,80],[80,45]], paths=[[3,4,5],[0,1,2],[6,7,8]])
	# triangle with two triangular holes...
	polygon(points=[[0,0],[100,0],[0,100],[5,5],[30,5],[5,30],[25,25],[25,60],[60,25]], paths=[[3,4,5],[0,1,2],[6,7,8]], fill=true)
	
#polygon_demo()



# 
def polyhedron_demo():
	return polyhedron(points = [
		[0, -10, 60], [0, 10, 60], [0, 10, 0], [0, -10, 0], [60, -10, 60], [60, 10, 60], 
		[10, -10, 50], [10, 10, 50], [10, 10, 30], [10, -10, 30], [30, -10, 50], [30, 10, 50]
		], 
	faces = [
		[0,3,2],  [0,2,1],  [4,0,5],  [5,0,1],  [5,2,4],  [4,2,3],
			[6,8,9],  [6,7,8],  [6,10,11],[6,11,7], [10,8,11],
			[10,9,8], [3,0,9],  [9,0,6],  [10,6, 0],[0,4,10],
			[3,9,10], [3,10,4], [1,7,11], [1,11,5], [1,8,7],  
			[2,8,1],  [8,2,11], [5,11,2]
		]
	)

#polyhedron_demo()

def pyramid_demo():
	return polyhedron(
		points=[ [10,10,0],[10,-10,0],[-10,-10,0],[-10,10,0], # the four points at base
			[0,0,10]  ],                                 # the apex point 
		triangles=[ [0,1,4],[1,2,4],[2,3,4],[3,0,4],     #  each triangle side
			[1,0,3],[2,1,3] ]                         # two triangles for square base
 )

#pyramid_demo()


# source: http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#color	
def MulticolorSin3D():
	for i in range (0,36):
		for j in range(0,36):
			color([0.5+sin(10*i)/2, 0.5+sin(10*j)/2, 0.5+sin(10*(i+j))/2] ,
			translate([i,j,0],
				cube(size=[1, 1, 11+10*cos(10*i)*sin(10*j)] )
			))

#MulticolorSin3D()


# ported from sample at: http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#lookup 
def lookup_demo():
	# helper, inner def
	def get_cylinder_h(p):
		return lookup(p, [
			[ -200, 5 ],
			[ -50, 20 ],
			[ -20, 18 ],
			[ +80, 25 ],
			[ +150, 2 ]
		])	
	for i in range (-100, +100, 5):  # note: range increment is middle param in OpenSCAD, in python, it is the third param!!
		# echo(i, get_cylinder_h(i));
		translate([ i, 0, -30 ] , cylinder(r1 = 6, r2 = 2, h = get_cylinder_h(i)*3) )
		
#lookup_demo()

	
def pow_demo():
	for i in range(0,5): 
		translate([i*25,0,0],
			cylinder(h = pow(2,i)*5, r=10))
		echo (i," : ",pow(2,i))

#pow_demo()

def demo_random_spheres():
	seed=42
	random_vect=rands(5,15,4,seed) # get a vector of 4 numbers
	echo( "Random Vector: ",random_vect)
	sphere(r=5)
	for i in range(0,3):
# todo: need to implement more rotate param compatibility
#		rotate(360*i/4 , translate([10+random_vect[i],0,0] ,
		rotate([360*i/4,0,0] , translate([10+random_vect[i],0,0] ,
	     sphere(r=random_vect[i]/2) ))

	 
#demo_random_spheres()

def pacman():
	blenderscad.fn=128
	return scale([2,2,2], translate([0,0,6],rotate([90,45,0],
	    difference(
	        sphere(r=6)        
	    ,   translate([1,1,-6], cube([6,6,12]))
	    ,   translate([-1,4,+2], cylinder (r=1, h=3  ) )
	    ,   translate([-1,4,-5], cylinder (r=1, h=3  ) )
	 ))))

#pacman()

# compare result to OpenSCAD:
def rotate_test():
	#OpenSCAD version:
	#cylinder(h=10,r=3);
	#rotate( [90,0,90]) cylinder(h=10,r=3)  ;
	#rotate([0,0,90])  rotate( [90,0,0]) cylinder(h=10,r=3)     ;
	#rotate([90,0,0]) rotate( [0,0,90]) cylinder(h=10,r=3)    ;
	cylinder(h=10,r=3)
	rotate( [90,0,90], cylinder(h=10,r=3) ) 
	rotate([0,0,90],  rotate( [90,0,0], cylinder(h=10,r=3) )   ) 
	rotate([90,0,0], rotate( [0,0,90], cylinder(h=10,r=3) )   )

#rotate_test()


# My Filament Holder (rough version without rounded corners)
# my original OpenSCAD version: http://www.thingiverse.com/thing:198859
def FilamentHolderSimple(D,A,b) :
   return union(
	difference(
			union(
			   cylinder(r1 = D/2, r2=D/2-1 , h = b, center = true)
			 , translate([0,0,-b/2+1] , cylinder(r1 = D/2+2, r2=D/2+1.5,h = 2, center = true))
			)
		  , cylinder(r = D/2-3, h = b, center = true)
		)  
	, difference(
			union(
				cylinder(r = A/2+4, h = b, center = true)
			  , cube([D-4,4,b],center=true) 
			  , cube([4,D-4,b],center=true) 
			)
		  , cylinder(r = A/2, h = b, center = true)
		) 
	)
  
# Drumm inner diameter in mm
D = 52
# axis diameter
A = 7  #Actually 6mm
b=14 # holder height
#FilamentHolderSimple(D,A,b)




#TODO: Fix error if "union" instead of "group":
#CSG failed, exception degenerate edge
#Unknown internal error in boolean

# a fischertechnik helper
def ft_nut(L=1.0,A=4.0,SLOT=3.0,H=30.0):
	return union(
	   translate([(L-A)/2.0,0,0],
          color(red,
			cylinder(r = (A/2.0), h = H*1.2,center = true)))
#	The following line causes probs in console and final object...		
# added translate to fix. seems to be a precision problem with my rotate calculations...
# STRANGE...			
#	,	translate([L/2.0 , 0,0],cylinder(r=SLOT/2,h=H+2,center=true))
#	,	translate([L/2.0 , 0,0], cube([A,SLOT,H*1.2],center=true))  # leads to: CSG failed, exception extern\carve\lib\triangulator.cpp:899  "didn't manage to link up hole!"
	,	translate([L/2.0 +000000000000000000000000000.1, 0, 0],
#		  color(blue,
			cube([A,SLOT,H*1.2],center=true))
#			)	
	)


# a fischertechnik basic block. incomplete, but serves as a demo for the
# fixed rotate() behavior: also rotating the location around the center.
def makeFtBlock():
	L = 15.0 # Laenge in mm
	B = 15.0 # Breite in mm
	H = 30.0 # Hoehe in mm
	A = 4.0 # axis diameter
	SLOT = 3.0 
	return translate ([0,0,0],
		difference(
			cube([L,B,H],center=true)
			, union(
				   rotate([0,0,0]  , ft_nut(L,A,SLOT,H) )
				 , rotate([0,0,90] , ft_nut(L,A,SLOT,H) )
				 , rotate([0,0,180], ft_nut(L,A,SLOT,H) )
#	The following line causes probs in console and final object...		
# added translate to fix. seems to be a precision problem with my rotate calculations...		
				, rotate([0,0,270] , ft_nut(L,A,SLOT,H) )
#				, translate([0.001,0,0],rotate([0,0,270] , ft_nut(L,A,SLOT,H) ))
				 # bottom:
				 , translate([0,0,-7.5] , rotate([90,90,0],  ft_nut(L,A,SLOT,H) ))
			)
		,apply=True)
	 )	

#color(red, makeFtBlock() )

#L = 15 # Laenge in mm
#B = 15 # Breite in mm
#H = 30 # Hoehe in mm
#A = 4 # axis diameter
#SLOT = 3 		
#rotate([0,0,270] , ft_nut(L,A,SLOT,H) )					
						
