#!/usr/bin/python
from config import *
import string , os, sys

opprefix = sys.argv[1]
brlcadipfile = "work_" + opprefix + ".txt"
stadipfile = "stad_" + opprefix + ".anl"
feltipfile = "felt_" + opprefix + ".flt"
# Removes any previously generated compiled python file
os.system('rm config.pyc')

# Process to calculate spans 
# 2@200+500+3@100
def span_process(span_string):
	span_st=string.strip(span_string)
	span_sp=string.split(span_st, '+')
	index=0	
	list=[]
	while index < len(span_sp):
		if string.find(span_sp[index], '@')==-1:
			list.append(float(span_sp[index]))
		else:		
			in_sp=string.split(span_sp[index], '@')
			count=0		
			while count < int(in_sp[0]):
				list.append(float(in_sp[1]))
				count+=1
		index+=1
	return list

# BRL-CAD input file
f = open(brlcadipfile, 'w+')

# Arrays for BRL-CAD Comb command
beamlengthlist = ["r beamlengthwise.r"]
beamwidthlist = ["r beamwidthwise.r"]
foundationplanelist = ["r foundationplane.r"]
plinthplanelist = ["r plinthplane.r"]
columnslist = ["r columns.r"]
slablist = ["r slabs.r"]

# Box function for beams, columns and slab
def make_box(name,length,width,height,base_vector):
	xmax = base_vector[0] + length
	ymax = base_vector[1] + width
	zmax = base_vector[2] + height
	data = "in " + str(name) + " rpp " + str(base_vector[0])  + " " + str(xmax)+ " " + str(base_vector[1]) + " " + str(ymax) + " " + str(base_vector[2])+ " " +str(zmax) + "\n"
	f.write(data)

# Cylinder for round column
def make_cylinder(name,radius,height,base_vector):
	data = "in " + str(name) + " rcc " + str(base_vector[0])  + " " + str(base_vector[1]) + " " + str(base_vector[2]) + " 0 0 "+ str(height) + " " + str(radius) + "\n"
	f.write(data)
	
# Creates an array of lengths
dis_span_len=span_process(rep_span_len)

# Creates an array of widths
dis_span_wid=span_process(rep_span_wid)

# Number of lengths
no_spans_len=len(dis_span_len)

# Number of widths
no_span_wid=len(dis_span_wid)

# Creates an array of heights
clear_height = span_process(clearh)

# Number of stories
stories = len(clear_height)

#raytracing function for BRL-CAD
def raytrace():
	beamwidthstring = ''.join(beamwidthlist)
	beamlengthstring = ''.join(beamlengthlist)
	foundationplanestring = ''.join(foundationplanelist)
	plinthplanestring = ''.join(plinthplanelist)
	columnsstring = ''.join(columnslist)
	slabstring = ''.join(slablist)

	f.write(beamwidthstring)
	f.write('\n')
	f.write(beamlengthstring)
	f.write('\n')
	f.write(foundationplanestring)
	f.write('\n')
	f.write(plinthplanestring)
	f.write('\n')
	f.write(columnsstring)
	f.write('\n')
	f.write(slabstring)
	f.write('\n')
	f.write('mater beamlengthwise.r plastic 255 0 0 n')
	f.write('\n')
	f.write('mater beamwidthwise.r plastic 0 0 255 n')
	f.write('\n')
	f.write('mater foundationplane.r plastic{tr=1} 255 255 0 n')
	f.write('\n')
	f.write('mater plinthplane.r plastic{tr=0.9} 255 105 180 n')
	f.write('\n')
	f.write('mater columns.r plastic 0 255 0 n')
	f.write('\n')
	f.write('mater slabs.r plastic{tr=1} 0 255 255 n')
	f.write('\n')
	f.write('B *.r')
	f.write('\n')
	f.write('comb building u beamlengthwise.r u beamwidthwise.r u columns.r u slabs.r u foundationplane.r u plinthplane.r ')
	f.write('\n')
	f.write('ae 0 0')
	f.write('\n')
	f.write('saveview front')
	f.write('\n')
	f.write('ae 270 0')
	f.write('\n')
	f.write('saveview side')
	f.write('\n')
	f.write('ae -90 90')
	f.write('\n')
	f.write('saveview top')
	f.write('\n')
	f.write('ae 30 30')
	f.write('\n')
	f.write('saveview iso')
	f.write('\n')

def z_sum(i):
	zsum = 0
	index=0
	while index <= i-1 and i!=0:
		zsum = zsum + clear_height[index] + dep_slab - dep_beam/2.0 + ((dep_beam/2.0)*index)
		index = index+1	 
	return zsum

def x_sum(i):
	xsum = 0
	index=0
	while index <= i-1 and i!=0:
		xsum = xsum + dis_span_len[index]
		index = index+1
	return xsum

def y_sum(i):
	ysum = 0
	index=0
	while index <= i-1 and i!=0:
		ysum = ysum + dis_span_wid[index]
		index = index+1
	return ysum

#staad pro file function
def write_stadpro_file():
	stadfile = open(stadipfile, 'w+')
	stadfile.write('STAAD SPACE\r\nSTART JOB INFORMATION\r\nENGINEER DATE ')
	stadfile.write('31-May-10')
	stadfile.write('\r\nEND JOB INFORMATION\r\nINPUT WIDTH 79\r\nUNIT METER KN\r\n')
	stadfile.write('JOINT COORDINATES\r\n')
	sr_no=0
	while sr_no < len(nodes):
		coord_str = str(sr_no +1)+' '+str(nodes[sr_no][0])+' '+str(nodes[sr_no][1])+' '+str(nodes[sr_no][2])+'; '
		stadfile.write(coord_str)
		sr_no +=1
	stadfile.write('\r\nMEMBER INCIDENCES\r\n')
	sr_no=0
	while sr_no < len(members):
		mem_str=str(sr_no+1)+' '+str(members[sr_no][0] + 1)+' '+str(members[sr_no][1] + 1)+'; '	
		stadfile.write(mem_str)
		sr_no +=1
	stadfile.write('\r\nMEMBER PROPERTY\r\n')
	sr_no=0
	while sr_no < len(members):
		if members[sr_no][2]=='circle':
			mem_prop=str(sr_no +1)+' PRIS YD '+str(members[sr_no][4])+'\r\n'
		else:
			mem_prop=str(sr_no +1)+' PRIS YD '+str(members[sr_no][5])+' ZD '+str(members[sr_no][4])+'\r\n'
		stadfile.write(mem_prop)
		sr_no +=1		
	stadfile.write('FINISH')
	stadfile.close()

def write_felt_file():
	feltfile = open(feltipfile, 'w+')

	#problem description
	feltfile.write('problem description \n')
	feltfile.write('title="Building analysis" nodes=' + str(len(nodes)) + ' elements=' + str(len(members)) + ' analysis=static\n')
	feltfile.write('nodes \n')
	
	#nodes defining
	sr_no=0
	while sr_no < len(firstnodes):
		coord_str = str(sr_no +1)+' x='+str(nodes[sr_no][0])+' y='+str(nodes[sr_no][1])+' z='+str(nodes[sr_no][2])+' constraint=' + foundationnodes + '\n' # 
		feltfile.write(coord_str)
		sr_no +=1
	
	for sr_no in range(len(firstnodes) , len(nodes)):
		coord_str = str(sr_no +1)+' x='+str(nodes[sr_no][0])+' y='+str(nodes[sr_no][1])+' z='+str(nodes[sr_no][2])+' constraint=free\n' # 
		feltfile.write(coord_str)	
	
	#beam is defined
	feltfile.write('beam3d elements \n')
	sr_no=0

	while sr_no < len(members):
		if(members[sr_no][3]=='beam'):
			mem_str=str(sr_no+1)+' nodes=['+str(members[sr_no][0] + 1)+','+str(members[sr_no][1] + 1)+'] material='+ members[sr_no][6] +' load='+members[sr_no][7] + '\n'	
			feltfile.write(mem_str)
		sr_no +=1
		
	sr_no=0
	while sr_no < len(members):
		mem_str = ''
		if(members[sr_no][3]=='column' and members[sr_no][2]=='rect'):
			mem_str=str(sr_no+1)+' nodes=['+str(members[sr_no][0] + 1)+','+str(members[sr_no][1] + 1)+'] material='+ members[sr_no][6] +'\n' #' load='+members[sr_no][7] + 	
		if(members[sr_no][3]=='column' and members[sr_no][2]=='circle'):
			mem_str=str(sr_no+1)+' nodes=['+str(members[sr_no][0] + 1)+','+str(members[sr_no][1] + 1)+'] material='+ members[sr_no][5] +'\n' #' load='+members[sr_no][6] + 
		feltfile.write(mem_str)
		sr_no +=1

	#material properties
	feltfile.write('material properties \n')
	feltfile.write(materialforbeam +' A=' + str(a) +' E=' + str(e) +' Ix=' + str(ix) +' Iy=' + str(iy) + ' Iy=' + str(iy) + ' Iz = ' + str(iz) + ' J=' + str(j) + ' G=' + str(g) + '\n')
	if(materialforbeam==materialforcolumn):
		print "hi"
	else:
		feltfile.write(materialforcolumn +' A=' + str(cola) +' E=' + str(cole) +' Ix=' + str(colix) + '\n')
	
	#distributed loads
	feltfile.write('distributed loads \n')
	feltfile.write('lsl direction=' + lslloaddir + ' values=(1,'+ str(lengthwiseweight) + ') (2,' + str(lengthwiseweight) + ')\n')
	feltfile.write('wsl direction=' + wslloaddir + ' values=(1,' + str(widthwiseweight) + ') (2,' + str(widthwiseweight) + ')\n')
	#if column taken into consideration
	#feltfile.write('csl direction=perpendicular values=(1,'+ str(columnweight) + ') (2,' + str(columnweight)+ ')\n')

	#constraints
	feltfile.write('constraints \n')
	feltfile.write('pin Tx=C Ty=C Tz=C Rx=U Ry=U Rz=U\n')
	feltfile.write('free Tx=U Ty=U Tz=U Rx=U Ry=U Rz=U\n')
	feltfile.write('fixed Tx=C Ty=C Tz=C Rx=C Ry=C Rz=C\n')
	
	#ending felt file
	feltfile.write('end')
	feltfile.close()

i=0
j=0
k=0
nodes = []
members = []
firstnodes = []
z=0
strutmembers = []
beammembers = []
lengthspanbeams = []
widthspanbeams = []

while z <= stories:
	x = 0
	while x <= no_spans_len:
		y = 0
		while y <= no_span_wid:
			coords = [x_sum(x), y_sum(y), z_sum(z)]
			if z==0:
				nodes.append([coords[0],coords[1],coords[2]- dep_of_foun - plinth_lev])
				firstnodes.append([coords[0],coords[1],coords[2]- dep_of_foun - plinth_lev])
			else:
				nodes.append(coords)
			if z==1:
				col_name = "Column" + str(i)
				i = i + 1
				if col_type==1:
					make_box(col_name, len_col,wid_col, dep_of_foun + plinth_lev + z_sum(z) - z_sum(z-1), [coords[0] - len_col/2.0, coords[1] - wid_col/2.0, dep_of_foun + plinth_lev - 2*(dep_of_foun + plinth_lev)])
					mem=[nodes.index([coords[0],coords[1],0 - dep_of_foun - plinth_lev]),len(nodes) -1,'rect','column',len_col,wid_col,materialforcolumn,'csl']
					lol = " u " + col_name
					columnslist.append(lol)
				else:
					make_cylinder(col_name, radius_col, dep_of_foun + plinth_lev + z_sum(z) - z_sum(z-1), [coords[0], coords[1], dep_of_foun + plinth_lev - 2*(dep_of_foun + plinth_lev)])
					mem=[nodes.index([coords[0],coords[1],0 - dep_of_foun - plinth_lev]),len(nodes) -1,'circle','column',radius_col,materialforcolumn,'csl']
					lol = " u " + col_name
					columnslist.append(lol)
				members.append(mem)
	
			if z!=0 and z!=1:
				col_name = "Column" + str(i)
				i = i + 1
				if col_type==1:			
					make_box(col_name, len_col, wid_col, z_sum(z) - z_sum(z-1), [coords[0] - len_col/2.0, coords[1] - wid_col/2.0, z_sum(z-1)])
					mem=[nodes.index([coords[0],coords[1],z_sum(z-1)]),len(nodes) -1,'rect','column',len_col,wid_col,materialforcolumn,'csl']
					lol = " u " + col_name
					columnslist.append(lol)
				else:
					make_cylinder(col_name, radius_col, z_sum(z) - z_sum(z-1), [coords[0], coords[1], z_sum(z-1)])
					mem=[nodes.index([coords[0],coords[1],z_sum(z-1)]),len(nodes) -1,'circle','column',radius_col,materialforcolumn,'csl']
					lol = " u " + col_name
					columnslist.append(lol)
				members.append(mem)
			
			if y !=0 and z!=0:
				beam_name = "Beam" + str(j)
				j = j + 1			
				make_box(beam_name, wid_beam, y_sum(y) - y_sum(y-1), dep_beam, [coords[0] - wid_beam/2.0, y_sum(y-1), z_sum(z) - dep_beam/2.0])
				mem=[nodes.index([coords[0],y_sum(y-1),coords[2]]),len(nodes) -1,'rect','beam',dep_beam,wid_beam,materialforbeam,'wsl']
				members.append(mem)
				lol = " u " + beam_name
				beamlengthlist.append(lol)

			if x != 0 and z!=0:
				beam_name = "Beam" + str(j)
				j = j + 1			
				make_box(beam_name, x_sum(x) - x_sum(x-1), wid_beam, dep_beam, [x_sum(x-1), coords[1] - wid_beam/2.0, z_sum(z) - dep_beam/2.0])
				mem=[nodes.index([x_sum(x-1),coords[1],coords[2]]),len(nodes) -1,'rect','beam',dep_beam,wid_beam,materialforbeam,'lsl']
				members.append(mem)
				lol = " u " + beam_name
				beamwidthlist.append(lol)

			y=y+1
		x=x+1
	if z!=0:
		slab_name = "Slab" + str(k)
		k = k + 1			
		make_box(slab_name, x_sum(no_spans_len), y_sum(no_span_wid), dep_slab, [0, 0, z_sum(z) + dep_beam/2.0 - dep_slab])
		lol = " u " + slab_name
		slablist.append(lol)		
	z=z+1

#foundationbox
foundationbase = [ -500 ,-500 , -1*(plinth_lev + dep_of_foun)]
foundationlen = sum(dis_span_len) + 1000
foundationwid = sum(dis_span_wid) + 1000
foundationhei = dep_of_foun
make_box("foundation",foundationlen,foundationwid,foundationhei,foundationbase)
lol = " u foundation"
foundationplanelist.append(lol)

#plinthbox
plinthbase = [0 , 0 , -1*plinth_lev]
plinthlen = sum(dis_span_len)
plinthwid = sum(dis_span_wid)
plinthhei = plinth_lev
make_box("plinth",plinthlen,plinthwid,plinthhei,plinthbase)
lol = " u plinth"
plinthplanelist.append(lol)

write_stadpro_file()
write_felt_file()
raytrace()
