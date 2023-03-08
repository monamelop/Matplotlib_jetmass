#Jet Mass compute

import yoda
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from matplotlib.ticker import AutoMinorLocator
import os



def JM(yodafile, obs):
    
    histos = yoda.read(yodafile)
    
    jet = histos[obs]

    N_jets = jet.sumW()
    
    #normalization
    jet.scaleW(1/N_jets)


    x = np.asarray(jet.xVals())
    y = np.asarray(jet.yVals())
    yerr = np.asarray((jet.yMaxs() - jet.yMins()) / 2)
    xerr = np.asarray((jet.xMaxs() - jet.xMins()) / 2)

    return [x, y, xerr, yerr]


