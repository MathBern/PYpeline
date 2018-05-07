#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
PYpeline é um pacote que contém funções para fazer a redução de dados astronômicos em formato FITS.
'''

#Importando bibliotecas necessárias
import numpy as np
import astropy.io.fits as aif
import os
import glob
from numba import jit

#======================================================================#

master_bias_image = None
master_flat_image = None

@jit #utilizado para 'compilar' a função e tornar o código mais rápido.
def open_and_convert_to_f64(image_FITS):
    '''
    Abre um arquivo .fits e converte seus dados numéricos para float64.
    INPUT [fits]: imagem FITS que terá seus dados numéricos convertidos para float64.
    OUTPUT [numpy.array]: dados da imagem convertidos para array do Numpy, porém float64.
    return image_data
    '''

    image_data, image_header = aif.getdata(image_FITS, header=True)
    image_data = image_data.astype(np.float64)

    return image_data

def save_fits(array_img, outfile, image_header = None):
    '''
    Salva um arquivo .fits
    INPUT 1 [np.array]: dados da imagem, já convertido em array do numpy.
    INPUT 2 [str]: nome do arquivo de saída
    INPUT 3 [astropy.Header.header]: dados do header da imagem. Se nada inserido, cria um header básico.
    OUTPUT [fits]: arquivo fits com o nome dado pelo INPUT 2.
    return None
    '''
    hdu = aif.PrimaryHDU() #criando o HDU
    hdu.data = array_img
    if image_header != None:
        hdu.header = image_header

    hdu.writeto(outfile)

def CreateMasterBias(obs_dir):
    '''
    Cria um bias combinado, pela mediana, a partir das imagens de bias, contidos na pasta bias.
    INPUT [str]: caminho da pasta dos dados de observação.
    OUTPUT [fits]: arquivo de bias combinado pela mediana (MasterBias.fits)
    return None
    '''
    #checa se existe um arquivo homônimo e o deleta, caso exista.
    if os.path.isfile(obs_dir + '/auxiliary_images/MasterBias.fits'):
        os.system('rm '+ obs_dir + '/auxiliary_images/MasterBias.fits')
        print('There was a MasterBias.fits. It was replaced!')

    bias_dir = obs_dir + '/bias' #caminho das imagens bias
    bias_list = glob.glob(bias_dir + '/*.fits') #lista com os nomes de cada imagem contido na pasta bias.
    bias_header  = aif.PrimaryHDU().header #inicializa um header básico para o MasterBias
    bias_header['FILENAME'] = 'MasterBias.fits'
    bias_header.comments['FILENAME'] = 'MasterBias created with several combined bias by median.'
    #loop para criar uma lista com os dados de cada imagem.
    images_array = []
    for bias_image_i in bias_list:
        images_array.append(open_and_convert_to_f64(bias_image_i))

    #converte a lista em uma array do Numpy e
    images_array_np = np.array(images_array)
    #combinando pela média os dados
    master_bias = np.median(images_array_np, axis = 0) #axis = 0 faz com que a combinação seja pixel a pixel de cada imagem

    #salvando o caminho do masterbias para a imagem poder ser utilizada por outras funções
    global master_bias_image
    master_bias_image = obs_dir + '/auxiliary_images/MasterBias.fits'
    #salva a imagem
    save_fits(master_bias, master_bias_image, bias_header)

    print('Master bias saved on: ' + master_bias_image)
    print('Statistical test (smaller than 30.0 is good!): ' + str(np.mean(master_bias)))
    #zera as variáveis para não consumir memória
    master_bias = None
    images_array_np = None

    return None



def normalize_by_mean(array):
    '''
    Normaliza um array pela média.
    INPUT [numpy.array]: O array que será normalizado
    OUTPUT [array]: Array normalizado pela média aritimética.
    return None
    '''
    return array/np.mean(array)


def CreateMasterFlat(obs_dir):
    '''
    Cria um flat combinado a partir das imagens de flat, contidos na pasta flat.
    INPUT [str]: caminho da pasta dos dados de observação.
    OUTPUT [fits]: arquivo de flat normalizado (auxiliary_images/MasterFlat.fits)
    return None
    '''

    # define o caminho do masterbias
    global master_bias_image
    master_bias_image = obs_dir + '/auxiliary_images/MasterBias.fits'

    #checa se existe um masterbias. Caso não haja, cria
    if (not os.path.isfile(master_bias_image)):
        CreateMasterBias(obs_dir)

    #o que for similar a função CreateMasterBias não será comentado!

    if os.path.isfile(obs_dir + '/auxiliary_images/MasterFlat.fits'):
        os.system('rm '+ obs_dir + '/auxiliary_images/MasterFlat.fits')
        print('There was a MasterFlat.fits. It was replaced!')

    flat_dir = obs_dir + '/flat'
    flat_list = glob.glob(flat_dir + '/*.fits')

    flat_header  = aif.PrimaryHDU().header
    flat_header['FILENAME'] = 'MasterFlat.fits'
    flat_header.comments['FILENAME'] = 'MasterFlat created with a combination by median of normalized by mean flats.'

    images_array = []
    for flat_image_i in flat_list:
        images_array.append(normalize_by_mean(open_and_convert_to_f64(flat_image_i) - open_and_convert_to_f64(master_bias_image)))

    images_array_np = np.array(images_array)
    master_flat = np.median(images_array_np, axis = 0) #axis = 0 faz com que a combinação seja pixel a pixel de cada imagem

    global master_flat_image
    master_flat_image = obs_dir + '/auxiliary_images/MasterFlat.fits'

    save_fits(master_flat, master_flat_image, flat_header)

    print('Master flat saved on: ' + master_flat_image)
    #Realiza um teste para mostrar se o flat foi bem sucedido.
    print('Statistical test (close to 1.0 is good!): ' + str(np.mean(master_flat)))

    master_flat = None
    images_array_np = None

    return None

def ReduceCompletely(obs_dir, name = 'reduced', combine_images = 0):
    '''
    Efetua a redução completa de uma imagem FITS de ciência, subtraindo bias e nivelando pelo flat.
    INPUT 1 [str] : caminho da pasta dos dados de observação.
    INPUT 2 [str] : nome da imagem reduzida (não é necessário colocar o caminho todo).
    INPUT 3 [int]: parâmetro de escolha de combinação, ou não das imagens:
             1 combina pela mediana.
             2 combina pela média.
             outro: não combina as imagens.
    OUTPUT [fits] : imagem, ou imagens, de ciência reduzidas de bias e flat.
    return None
    '''

    #inicializa as variáveis contendo os locais do MasterBias e MasterFlat.
    global master_bias_image
    master_bias_image = obs_dir + '/auxiliary_images/MasterBias.fits'
    global master_flat_image
    master_flat_image = obs_dir + '/auxiliary_images/MasterFlat.fits'

    #se não existem, eles são criados.
    if (not os.path.isfile(master_bias_image)):
        CreateMasterBias(obs_dir)

    if (not os.path.isfile(master_flat_image)):
        CreateMasterFlat(obs_dir)

    sci_raw_dir = obs_dir + '/science_raw'
    sci_red_dir = obs_dir + '/science_reduced'
    sci_raw_list = glob.glob(sci_raw_dir + '/*.fits')

    #cria um header padrão do Astropy para o
    sci_red_header_1 = aif.PrimaryHDU().header
    sci_red_header_2 = aif.PrimaryHDU().header

    #salva os dados do masterbias e do masterflat
    bias = open_and_convert_to_f64(master_bias_image)
    flat = open_and_convert_to_f64(master_flat_image)
    images_array = []
    for sci_raw_image_i in sci_raw_list:
        images_array.append((open_and_convert_to_f64(sci_raw_image_i) - bias)/flat)

    images_array_np = np.array(images_array)

    if combine_images == 1:
        if not os.path.isfile(sci_red_dir + '/' + name + '_comb_median.fits'):
            sci_red_header_1['FILENAME'] = name + '_comb_median.fits'
            save_fits(np.median(images_array_np, axis = 0), sci_red_dir + '/' + name + '_comb_median.fits', sci_red_header_1)
            print('Reduced image saved on: ' + sci_red_dir + '/' + name + '_comb_median.fits.')
        else:
            print(sci_red_dir + '/' + name + '_comb_median.fits' + ' already exists! So did not performed image reduction.')
    elif combine_images == 2:
        if not os.path.isfile(sci_red_dir + '/' + name + '_comb_mean.fits'):
            sci_red_header_2['FILENAME'] = name + '_comb_mean.fits'
            save_fits(np.mean(images_array_np, axis = 0), sci_red_dir + '/' + name + '_comb_mean.fits', sci_red_header_2)
            print('Reduced image saved on: ' + sci_red_dir + '/' + name + '_comb_mean.fits.')
        else:
            print(sci_red_dir + '/' + name + '_comb_mean.fits' + ' already exists! So did not performed image reduction.')
    else:
        for i in range(len(images_array_np)):
            if(not os.path.isfile(sci_red_dir + '/'+ name + str(i) + '.fits')):
                sci_red_header = aif.getdata(sci_raw_list[i], header=True)[1]
                sci_red_header['BIASFLAT'] = True
                save_fits(images_array_np[i], sci_red_dir + '/' + name + str(i) + '.fits', sci_red_header)
                print('Reduced image saved on: ' + sci_red_dir + '/' + name + str(i))
            else:
                print(sci_red_dir + '/' + name + str(i) + '.fits' + ' already exists! So did not performed image reduction.')

    images_array_np = None

    return None
