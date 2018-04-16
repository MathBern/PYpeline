'''
PYpeline is a package that contains funtcions for data reducing and analisys.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy.io.fits as aif
import os
import glob

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







class reduc(object):
	'''
	Contains all functions of reduction
	'''
	
	def __init__(self, obs_dir):
		self.obs_dir = obs_dir
	
	def SaveFits(array_img,outfile):
		'''
		Save a .fits image, given the array to be writen as image and the output file name.
		'''
		
		hdu = fits.PrimaryHDU() #criando o HDU 
		hdu.data = array_img
		hdu.writeto(outfile)
	
	def MasterBias(obs_dir):
		'''
		Creates a masterbias image (median combinatation of bias files)
		'''
		bias_dir = obs_dir + '/bias'
		bias_fits_array = np.array(glob.glob(bias_dir + '/*.fits'))		
		master_bias = np.median(bias_fits_array)
		SaveFits(master_bias,bias_dir + 'masterbias.fits')
		
		bias_fits_array = 0 #apenas para zerar a memoria
		bias_dir = 0 
		

