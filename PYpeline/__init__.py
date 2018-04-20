'''
PYpeline is a package that contains funtcions for data reducing and analisys.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy.io.fits as aif
import os
import glob

from numba import jit

def init_plotting(x=9,y=7):
    plt.rcParams['figure.figsize'] = (x,y)
    plt.rcParams['font.size'] = 20
    #plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 0.75*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = 0.65*plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.loc'] = 'best'
    plt.rcParams['axes.linewidth'] = 1

init_plotting()

#======================================================================#

@jit
def convert_to_f64(image_FITS):
	image_data = aif.getdata(image_FITS, header=False)
	image_data =  image_data.astype(np.float64)
	return image_data

@jit
def SaveFits(array_img, outfile):
	'''
	Save a .fits image, given the array to be writen as image and the output file name.
	'''
	hdu = aif.PrimaryHDU() #criando o HDU 
	hdu.data = array_img
	hdu.writeto(outfile)
	
@jit
def MasterBias(obs_dir):
	'''
	Creates a masterbias image (median combinatation of bias files)
	'''
	bias_dir = obs_dir + '/bias'
	bias_list_array = glob.glob(bias_dir + '/*.fits')		
	print (bias_list_array)
	matrixes_array = []
	for bias_image_i in bias_list_array:
		matrixes_array.append(convert_to_f64(bias_image_i))
	#~ print (matrixes_array)
	matrixes_array_np = np.array(matrixes_array)
	master_bias = np.median(matrixes_array_np, axis = 0)
	
	#~ SaveFits(master_bias, bias_dir + '/masterbias.fits')

		

