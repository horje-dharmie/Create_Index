#!/bin/python3

"""
	ATTENTION: Make sure input configuration is UNWRAPPED !!!!
"""

import numpy as np
import sys

if __name__=='__main__':
        
        NArguments = len(sys.argv)
        
        if (not NArguments==2):
                sys.exit('Please give .gro file')
	
        gro_file = sys.argv[1]

        try:
                input_file=open(gro_file,'r')
        except:
                sys.exit('Could not read file ' + gro_file)

        lineList = input_file.readlines()
        input_file.close()
        natoms = int(lineList[1])
        nmer=47
        no_of_chains= 300
        natoms_per_chain=nmer*9+2 #no of atoms per chain, 2 for the two end atoms

	# Read box information from last line
        box = np.zeros((3))
        box_string =lineList[-1]
        box[0] = float(box_string[0:10])
        box[1] = float(box_string[10:20])
        box[2] = float(box_string[20:30])

	# Make a list from 3rd line of input (first two are comments, number of atomistic sites)
        newlinelist = lineList[2:-1]
        group1=[]
        group2=[]

        for chain  in range(0,len(newlinelist),natoms_per_chain): #iterate over each chain
                group1index =[]
                group2index =[]
                atoms_in_each_chain = newlinelist[chain:chain+natoms_per_chain] # takes each chain
                for index, iline in enumerate(atoms_in_each_chain): #iterate over atoms in each chain
                    if float(iline[28:36]) < 0.5*box[1]:
                        group1index.append(chain+index+1)

                    else:
                        group2index.append(chain+index+1)
                
                if (natoms_per_chain+1)//2 < len(group1index) < natoms_per_chain+1: #check if group1 has more than half the total no of atoms in a chain
                    group1+=group1index
                else:
                    group2+=group1index   #if atoms in group1 are less that half the number of atoms in a chain, add to group2

                if (natoms_per_chain+1)//2 < len(group2index) < natoms_per_chain+1:
                    group2+=group2index
                else:
                    group1+=group2index


###### Write index file ########################################################################
        outfile='new_index.ndx'
        out_file=open(outfile,'w')
        out_file.write('[ System ] \n')

        
        system_list = np.arange(1, natoms+1,1)
        system=''
        for index in system_list:
            if index%15 == 0:
                system+=str(index)+'\n'
            else:
                system+=str(index)+' '
        out_file.write(system)
        
        out_file.write('[ Other ] \n')
        out_file.write(system)
        
        out_file.write('[ iPPHT ] \n')
        out_file.write(system)
        
        out_file.write('[ group1 ] \n')
        group1_atoms=''
        for index,atom_no in enumerate(group1):
            if (index+1)%15 == 0:
                group1_atoms+=str(atom_no)+'\n'
            else:
                group1_atoms+=str(atom_no)+' '
        out_file.write(group1_atoms)

        out_file.write('[ group2 ] \n')
        group2_atoms=''
        for index,atom_no in enumerate(group2):
            if (index+1)%15 == 0:
                group2_atoms+=str(atom_no)+'\n'
            else:
                group2_atoms+=str(atom_no)+' '
        out_file.write(group2_atoms)
        
        out_file.close()


