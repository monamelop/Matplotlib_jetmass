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
    jet.rebin(2)


    x = np.asarray(jet.xVals())+0.5
    y = np.asarray(jet.yVals())
    yerr = np.asarray((jet.yMaxs() - jet.yMins()) / 2)
    xerr = np.asarray((jet.xMaxs() - jet.xMins()) / 2)

    return [x, y, yerr, xerr]


def COMP(mc, data):
    
    # Encontre os valores de x que estão presentes em ambas as listas
    common_x = np.intersect1d(mc[0], data[0])

    # Encontre os índices correspondentes aos valores de x comuns
    arr_indices = np.where(np.isin(mc[0], common_x))[0]
    alice1_indices = np.where(np.isin(data[0], common_x))[0]
    
    # Use os índices para recuperar os valores dos erros de x correspondentes
    
    x_err_data = data[3][alice1_indices]

    # Use os índices para recuperar os valores de y correspondentes
    common_y_arr = mc[1][arr_indices]
    common_y_alice1 = data[1][alice1_indices]
    
    

    # Use os índices para recuperar as incertezas em y correspondentes
    common_y_errors_arr = mc[2][arr_indices]
    common_y_errors_alice1 = data[2][alice1_indices]

    
    new_y = common_y_arr/common_y_alice1
    
    # Calcular as incertezas relativas (delta x / x e delta y / y)
    relative_errors_arr = common_y_errors_arr / common_y_arr
    relative_errors_alice1 = common_y_errors_alice1 / common_y_alice1

    # Calcular a incerteza propagada para new_y usando a fórmula de propagação de incertezas
    new_y_err = new_y*np.sqrt(relative_errors_arr**2 + relative_errors_alice1**2) 
    
    
    
    
    
    return [common_x, new_y, new_y_err, x_err_data]
    