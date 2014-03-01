# blenderscad.shapes
# Additional Shape library, a subset of "MCAD" and OpenSCAD library folder. extend as needed.
#
# by Michael Mlivoncic, 2013
#


import blenderscad


blenderscad.initns(globals()) # to avoid prefixing all calls, we make "aliases" in current namespace


#################################################################
## some additional library functions
#################################################################   
#TODO: translate more lib functions and eventually pack into separate files

# translated from "shapes.scad"
## size is the XY plane size, height in Z
def hexagon(size, height):
    boxWidth = size/1.75
    o = None
    for r in [-60, 0, 60]:
        tmp=rotate([0,0,r], cube([boxWidth, size, height], true))
        o=union(tmp,o) # trick to overcome OpenSCADs implicit union :-)
    return o

#hexagon(10,30)

# size is the XY plane size, height in Z
def octagon(size, height):
  intersection(
    cube([size, size, height], true)
    , rotate([0,0,45], cube([size, size, height], true))
  )

#octagon(size=10,height=25)

def ellipsoid(w, h, center = False):
    scale([1, h/w, 1], sphere(r=w/2, center=center) )

#ellipsoid(w=10,h=5, center=true)
	
# roundedBox -> only sides!!
# size is a vector [w, h, d]
def roundedBox(width, height, depth, radius):
  o1= cube([width-2*radius,height,depth], true)
  o2= cube([width,height-2*radius,depth], true)
  o = union(o1,o2)
  for x in [radius-width/2, -radius+width/2] :
       for y in [radius-height/2, -radius+height/2] :
            ot= translate([x,y,0] , cylinder(r=radius, h=depth, center=true))
            o = union(o,ot)

#roundedBox(width=10, height=5, depth=20, radius=2)


#" official" rcube module from thingiverse rounded primitives
def rcube(Size=[20,20,20],b=0.5,center=True):
    tmp = None
    for x in [-(Size[0]/2-b),(Size[0]/2-b)]:
       for y in [-(Size[1]/2-b),(Size[1]/2-b)]:
            for z in [-(Size[2]/2-b),(Size[2]/2-b)]:
                tmp= union(translate([x,y,z], sphere(b) ), tmp)                
    hull(tmp)


#rcube([10,20,10],1)

# based on "rounded Primitives" from Thingiverse
def rcylinder(r=1, h=1, b=0.5, r1=-1, r2=-1):
	if r1 == -1 or r2 == -1:
		r1 = r
		r2 = r
		print([r1,r2])
	return translate([0,0,-h/2],
			hull(
			   rotate_extrude(translate([r1-b, b, 0], circle(r = b)))
	  		 , rotate_extrude(translate([r2-b, h-b, 0], circle(r = b)))			
            )
         )

#rcylinder(8, 24, b=2)

# TODO: Alternative: rounded Cylinder Caps...
#intersection( translate([0,0,-70],sphere(r=80)), cylinder(r=10,h=30))
#intersection( translate([0,0,-5],sphere(r=15)), cylinder(r=10,h=30))
#difference(intersection( translate([0,0,-5],sphere(r=15)), cylinder(r=10,h=30)), translate([0,0,33],cube([20,20,50],center=true)) )

