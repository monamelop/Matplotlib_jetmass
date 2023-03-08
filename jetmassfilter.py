# Script to filter events with absurd jetmass values

import numpy as np
import yoda
import glob
import os
import sys
import jetmass



code = str(sys.argv[1])

# The following should be changed for the correct energy
#folder = '/sampa/archive/monalisa/Mestrado/results/yoda/0-10/'
folder = '/home/monalisa/Desktop/Mestrado/JetMass/Testfilter'
#rejectedfolder = '/sampa/archive/monalisa/Mestrado/results/yoda/0-10/rejected/' 
rejectedfolder = '/home/monalisa/Desktop/Mestrado/JetMass/Testfilter/rejected'



jmmax = 0.7
 
files = glob.glob(folder + '/' + code + f'*_jetmass_R0.4.yoda')

print(f'Calculating JetMass of {len(files)} files...')


obslist = ['/JET_MASS/Jet_Mass_60_80','/JET_MASS/Jet_Mass_80_100','/JET_MASS/Jet_Mass_100_120']



for l in obslist:
    jetm = []
    for f in files:
        jetm.append(jetmass.JM(f, l))
       

    dists = []
    
    for i in range(len(jetm[0][1])):
        values = []
        for j in range(len(jetm)):
            v = jetm[j][1][i]
            values.append(v)
        dists.append(values)

    print(f'Comparing JetMass with threshold of {jmmax}...')
    rejected = [] 

    for p in dists:
        positions = np.where(np.asarray(p) > jmmax)[0]
        for pos in positions:
            rej = files[pos]
            print(f'\nReject file: {rej}, Jet_Mass = {p[pos]}')
            rejected.append(rej)
            os.system(f'cp {rej.replace("0.4", "*")} {rejectedfolder}/0-10/')
            #os.system(f'cp {rej.replace("jetmass").replace(0.4, "*")} rejected/0-10')
    print(f'''\n\nRemoved weird JetMass files.
    {code} 0-10 0.4: {100*len(set(rejected))/len(files)}%\n''')



