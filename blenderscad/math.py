# blenderscad.math
# This submodule  covers OpenSCAD's mathematical function area
#
# by Michael Mlivoncic, 2013
#

import math 

########################################################
# Math library functions
#
#OpenSCAD has sin, cos, tan, etc based on DEGREES
#

# OpenSCAD "constants"
true=True
false=False
pi=math.pi  #3.141592


def sin(deg):
	return math.sin(math.radians(deg))

def cos(deg):
	return math.cos(math.radians(deg))

def tan(deg):
	return math.tan(math.radians(deg))

def acos(deg):
	return math.acos(math.radians(deg))

def asin(deg):
	return math.asin(math.radians(deg))

def atan(deg):
	return math.atan(math.radians(deg))

def atan2(deg):
	return math.atan2(math.radians(deg))

def sign(x):
	return ((x > 0) - (x < 0)) 

#echo(sign(-5.0))	

def rands(min_value, max_value, value_count, seed_value=-1):
	import random
	#min_value 
	#    Minimum value of random number range
	#max_value 
	#    Maximum value of random number range
	#value_count 
	#    Number of random numbers to return as a vector
	#seed_value (optional) 
	#    Seed value for random number generator for repeatable results. 
	if seed_value != -1:
		random.seed(seed_value)
	res=[]
	for i in range(0,value_count):
		res.append( random.uniform( min_value, max_value) )
	return res

#echo("single rands: ",rands(0,10,1)[0])
#echo("multi rands: ",rands(0,10,8))

#OpenSCAD: lookup(key, [[key,value],[key,value],...] )
# "Look up value in table, and linearly INTERPOLATE if there's no exact match. 
# The first argument is the value to look up. The second is the lookup table -- a vector of key-value pairs."
# http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#lookup
def lookup(skey, sarray):
	d = dict(sarray)
	res = d.get(skey);
	if res is not None:
		return  res
	# need to interpolate...
	kl = 0  # will store the nearest key lower than search key (skey)
	kh = 0 #len(sarray)-1 # will store the nearest key higher than search key (skey)	
	for i in range (1, len(sarray)):		
		if (sarray[i][0] < skey) and (abs( skey - sarray[i][0] ) < abs( skey - sarray[kl][0] )) :
			kl = i
			#echo('new kl:',kl)
		if (sarray[i][0] > skey) and (abs(skey - sarray[i][0]) < abs(skey - sarray[kh][0] )) :
			kh = i	
			#echo('new kh:',kh)				
	vl = sarray[kl][1]; vh = sarray[kh][1];
	kl = sarray[kl][0]; kh = sarray[kh][0]; # kl, kh was just the index before, not the key itself!!!
	#echo(['found:',[kl,vl],[kh,vh]])
	res = vl + (vh-vl)*((skey-kl)/(kh-kl))
	return res

#echo (lookup(4.1,[[86,1],[5,77.55],[66,21],[2,108]])); # -> "ECHO: 86.685" in OpenSCAD.


# just exporting native "math" implementation...
ceil=math.ceil
exp=math.exp
floor=math.floor
ln=math.log # the natural logarithm
log=math.log # log(x,y)
sqrt=math.sqrt

## Already builtin to python:
# abs, max, min doesnt require math module
#abs=math.fabs
#len -> len("abc")
#mod --> %
# pow=math.pow  built-in python ...
# round, built-in -> round(x) or round(x,y) 
#echo(round(5.4)) #-> 5
#echo(round(5.6)) #-> 6


#TODO:
#norm=math.norm # eucledian norm
#norm=numpy.linalg.norm
#echo(norm([ 1,2,3,4] ))	#5.47723




