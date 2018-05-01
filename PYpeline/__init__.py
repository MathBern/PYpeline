#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
PYpeline é um pacote que contém funções para fazer a redução de dados astronômicos em formato FITS.
'''

#Importando bibliotecas necessárias
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

master_bias_image = None
master_flat_image = None

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

def CreateMasterBias(obs_dir):
    '''
    Cria um bias combinado, pela mediana, a partir das imagens de bias .
    '''

    bias_dir = obs_dir + '/bias'
    bias_list = glob.glob(bias_dir + '/*.fits')
    images_array = []

    for bias_image_i in bias_list:
        images_array.append(open_and_convert_to_f64(bias_image_i))


    images_array_np = np.array(images_array)
    master_bias = np.median(images_array_np, axis = 0) #axis = 0 faz com que a combinação seja pixel a pixel de cada imagem

    global master_bias_image
    master_bias_image = obs_dir + '/MasterBias.fits'

    SaveFits(master_bias, master_bias_image)

    return None



def normalize_by_mean(array):
    '''
    Normaliza um array pela média.
    '''
    return array/np.mean(array)


# def MasterFlat(obs_dir, masterbias_name = obs_dir + '/bias' + 'MasterBias.fits'):
def CreateMasterFlat(obs_dir):
    '''
    Cria um flat combinado a partir das imagens de bias .
    '''

    flat_dir = obs_dir + '/flat'
    flat_list = glob.glob(flat_dir + '/*.fits')
    images_array = []
    for flat_image_i in flat_list:
        images_array.append(normalize_by_mean(open_and_convert_to_f64(flat_image_i) - open_and_convert_to_f64(master_bias_image)))

    images_array_np = np.array(images_array)
    master_flat = np.median(images_array_np, axis = 0) #axis = 0 faz com que a combinação seja pixel a pixel de cada imagem

    global master_flat_image
    master_flat_image = obs_dir + '/MasterFlat.fits'

    SaveFits(master_flat, master_flat_image)
    return None

def ReduceCompletely(obs_dir, combine_images = 0):
    '''
    Efetua a redução completa de uma imagem FITS de ciência, subtraindo bias e nivelando pelo flat.
    '''

    sci_raw_dir = obs_dir + '/science_raw'
    sci_red_dir = obs_dir + '/science_reduced'
    sci_raw_list = glob.glob(sci_raw_dir + '/*.fits')

    images_array = []
    bias = open_and_convert_to_f64(master_bias_image)
    flat = open_and_convert_to_f64(master_flat_image)
    for sci_raw_image_i in sci_raw_list:
        images_array.append((open_and_convert_to_f64(sci_raw_image_i) - bias)/flat)

    images_array_np = np.array(images_array)

    if combine_images == 1:
        SaveFits(np.median(images_array_np, axis = 0), sci_red_dir + '/reduced_comb_median.fits')
    elif combine_images == 2:
        SaveFits(np.mean(images_array_np, axis = 0), sci_red_dir + '/reduced_comb_mean.fits')
    else:
        for i in range(len(images_array_np)):
            SaveFits(images_array_np[i], sci_red_dir + '/reduced' + str(i) + '.fits')

    return None
