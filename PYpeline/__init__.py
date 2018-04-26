#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
PYpeline é um pacote que contém funções para fazer a redução de dados astronômicos em formato FITS.
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

master_bias_path = 0
master_flat_path = 0

@jit
def open_and_convert_to_f64(image_FITS):
    '''
    Abre um arquivo .fits e o converte para float64.
    '''

    image_data = aif.getdata(image_FITS, header=False)
    image_data = image_data.astype(np.float64)
    return image_data

# @jit
# def create_log_file():



def SaveFits(array_img, outfile):
    '''
    Salva um arquivo .fits
    '''
    hdu = aif.PrimaryHDU() #criando o HDU
    hdu.data = array_img
    hdu.writeto(outfile)

def MasterBias(obs_dir):
    '''
       Cria um bias combinado a partir das imagens de bias .
    '''

    bias_dir = obs_dir + '/bias'
    bias_list_array = glob.glob(bias_dir + '/*.fits')
    matrixes_array = []

    for bias_image_i in bias_list_array:
        matrixes_array.append(open_and_convert_to_f64(bias_image_i))


    matrixes_array_np = np.array(matrixes_array)
    master_bias = np.median(matrixes_array_np, axis = 0) #axis = 0 faz com que a combinação seja pixel a pixel de cada imagem

    SaveFits(master_bias, bias_dir + '/MasterBias.fits')
    global master_bias_path
    master_bias_path = bias_dir + '/MasterBias.fits'



def normalize_flat(flat_image):
    return flat_image/np.mean(flat_image)


# def MasterFlat(obs_dir, masterbias_name = obs_dir + '/bias' + 'MasterBias.fits'):
def MasterFlat(obs_dir):
    '''
    Cria um flat combinado a partir das imagens de bias .
    '''

    flat_dir = obs_dir + '/flat'
    flat_list_array = glob.glob(flat_dir + '/*.fits')
    matrixes_array = []
    print(flat_list_array)
    print(master_bias_path)
    for flat_image_i in flat_list_array:
        matrixes_array.append(normalize_flat(open_and_convert_to_f64(flat_image_i) - open_and_convert_to_f64(master_bias_path)))

    matrixes_array_np = np.array(matrixes_array)
    master_flat = np.median(matrixes_array_np, axis = 0) #axis = 0 faz com que a combinação seja pixel a pixel de cada imagem

    global master_flat_path
    master_flat_path = flat_dir + '/MasterFlat.fits'

    SaveFits(master_flat, flat_dir + '/MasterFlat.fits')
