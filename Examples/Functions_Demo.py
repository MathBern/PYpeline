#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import astropy.io.fits as aif
import matplotlib.pyplot as plt

# sys.path.append("/home2/matheus15/Tratamento_de_Dados/PYpeline/PYpeline")
sys.path.append("/home/math/Graduacao/TratamentoDeDados/PYpeline/PYpeline")

import __init__ as PYl

# obs = '/home2/matheus15/Música/xo2b'
obs = '../../xo2b'

# criar apenas um masterbias
PYl.CreateMasterBias(obs)

#criar apenas um masterflat
PYl.CreateMasterFlat(obs)

#-------diferentes opções da função que faz a redução completa.
#faz a redução e combina as imagems pela mediana
PYl.ReduceCompletely(obs,name = 'CUSTOM_NAME', combine_images = 1)

#faz a redução e combina as imagems pela média
PYl.ReduceCompletely(obs,name = 'CUSTOM_NAME', combine_images = 2)

#mesma coisa, porém sem um nome de entrada (que por default será reduced)
PYl.ReduceCompletely(obs, combine_images = 2)

# faz a redução das imagens sem combina-las.
PYl.ReduceCompletely(obs,name = 'CUSTOM_NAME', combine_images = 0)

#mesmo processo, porém mudando o nome e demonstrando que qualquer valor além de
# combine_images =  1 e combine_images = 2 resulta na não combinação das imagens.
PYl.ReduceCompletely(obs,name = 'OTHER_CUSTOM_NAME', combine_images = 25678)
