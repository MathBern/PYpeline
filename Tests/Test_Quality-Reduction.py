import sys
import astropy.io.fits as aif
import matplotlib.pyplot as plt

sys.path.append("/home/math/Graduacao/TratamentoDeDados/PYpeline/PYpeline")

import __init__ as PYl

# obs = '/home2/matheus15/Música/xo2b'
obs = '../../xo2b'


raw_image = PYl.open_and_convert_to_f64(obs + '/science_raw/xo2b.0024.fits')
reduced_image = PYl.open_and_convert_to_f64(obs + '/science_reduced/CUSTOM_NAME12.fits')

plt.figure()
plt.title('Diference between Raw and Reduced')
plt.imshow(abs(reduced_image - raw_image), cmap='hot',origin='lower')
# plt.colorbar()
cbar = plt.colorbar()
cbar.set_clim(0, 20)
plt.clim(0,20)

plt.savefig('Test_Reduced-Raw.png')
