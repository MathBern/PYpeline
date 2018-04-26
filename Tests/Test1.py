import sys

# sys.path.append("/home2/matheus15/Tratamento_de_Dados/PYpeline/PYpeline")
sys.path.append("/home/math/Graduacao/TratamentoDeDados/PYpeline/PYpeline")

import __init__ as PYl

obs = '../Data/xo2b'

PYl.MasterBias(obs)
PYl.MasterFlat(obs)
