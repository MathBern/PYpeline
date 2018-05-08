#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import astropy.io.fits as aif
import matplotlib.pyplot as plt
import PYpeline as PYl

#*************
#Edite PATH colocando o caminho do local em que baixou os dados de exemplo! Recomenda-se colocar na padta Data.
obs = 'PATH/xo2b'

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
