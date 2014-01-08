############################################################
# This is just a SEMI-automated converter.
# Just help with indention instead of curled braces.
# The rest is manual work :-)

# pybraces / braces_decode 
# from: http://timhatch.com/projects/pybraces/#example
def braces_decode(input, errors='strict'):  
	##global indent_width, current_depth
	current_depth = 0
	indent_width = 4
	#
	if not input: return (u'', 0)
	length = len(input)
	# Deal with chunked reading, where we don't get
	# data containing a complete line of source
	if not input.endswith('\n'):
		length = input.rfind('\n') + 1
	input = input[:length]
	#
	acc = []
	lines = input.split('\n')
	for l in [x.strip().replace('++', '+=1') for x in lines]:
		if l.endswith(';'):
			l = l[:-1]

		if l.endswith('{'):
			#acc.append(' ' * current_depth + l[:-1].strip() + ':')  # not interested in the ":"...
			acc.append(' ' * current_depth + l[:-1].strip() )
			current_depth += indent_width
		elif l.endswith('}'):
			acc.append(' ' * current_depth + l[:-1].strip())
			current_depth -= indent_width
		else:
			acc.append(' ' * current_depth + l)
	return (u'\n'.join(acc)+'\n', length)

def convertOpenSCAD(filenameSCAD):
	import re
	#filenameSCAD = "O:/BlenderStuff/demo.scad"
	filenameConverted = filenameSCAD + ".py" # "O:/BlenderStuff/demo.scad.py"
	##clearAllObjects()
	txt = open(filenameSCAD).read()
	#print (txt)
	decodedTxt = braces_decode(txt)  
	source = decodedTxt[0]
	## some quick and dirty fixes to save manual work later...
    ## 1. module .... )" -> def ....):"
	#line = re.sub(r"(?i)^(.*)module(.*)$", "\\1def\\2 " % decodedTxt, line)
	#print(source)
	#source = re.sub("^(.*)module(.*)$", "def():", source)
	source = re.sub(r'module(.*)\)$'   ,r'def\1):'  , source, flags=re.MULTILINE)
	#####
	#print (decodedTxt)
	myFile = open(filenameConverted, 'w')
	myFile.write(source)
	myFile.close()
	#exec(compile( decodedTxt, filename, 'exec'))
	
def bulkConvert(startDir):
	import os
	for root, dirs, files in os.walk(startDir): # Walk directory tree
		for f in files:
			import os.path
			extension = os.path.splitext(f)[1].lower()			
			if extension == '.scad':
				#print(root+"/"+f)
				convertOpenSCAD(root+"/"+f)
	return "Done" 	
	
def convertOpenSCADTest():
	filenameSCAD = "O:/BlenderStuff/demo.scad"
	filenameConverted = "O:/BlenderStuff/demo.scad.py"
	##clearAllObjects()
	txt = open(filenameSCAD).read()
	#print (txt)
	decodedTxt = braces_decode(txt)  
	#print (decodedTxt)
	myFile = open(filenameConverted, 'w')
	myFile.write(decodedTxt[0])
	myFile.close()
	#exec(compile( decodedTxt, filename, 'exec'))

#convertOpenSCADTest()
bulkConvert("O:/BlenderStuff/OpenSCAD_convert")