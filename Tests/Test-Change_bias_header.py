def f(x):
    return x**2, x+4

print(f(3))
print(f(3)[0])

import astropy.io.fits as aif

aa = bias_header = aif.getdata(image_file, header=True)[1]
