import sys
import astropy.io.fits as aif

# sys.path.append("/home2/matheus15/Tratamento_de_Dados/PYpeline/PYpeline")
sys.path.append("/home/math/Graduacao/TratamentoDeDados/PYpeline/PYpeline")

import __init__ as PYl

# obs = '/home2/matheus15/Tratamento_de_Dados/PYpeline/Data/xo2b'
obs = '../Data/xo2b'

PYl.CreateMasterBias(obs)
PYl.CreateMasterFlat(obs)
PYl.ReduceCompletely(obs,name = 'CUSTOM_NAME', combine_images = 1)
PYl.ReduceCompletely(obs,name = 'CUSTOM_NAME', combine_images = 2)
PYl.ReduceCompletely(obs,name = 'CUSTOM_NAME', combine_images = 0)
PYl.ReduceCompletely(obs,name = 'OTHER_CUSTOM_NAME', combine_images = 25678)
