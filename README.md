# Calculate fractal (box-counting) dimension

This page has been setup to support the preprint titled **_Geometry and organization of coherent structures in stably stratified atmospheric boundary layers_** which can be found in arXiv: https://arxiv.org/abs/2110.02253

This is a direct port of the MATLAB boxcount code developed by F. Moisy. It calculates the box-counting dimension of a given d-dimensional array.

See the MATLAB code here: https://de.mathworks.com/matlabcentral/fileexchange/13063-boxcount.

## Installation

The code is available as a package from PyPI: https://pypi.org/project/boxcounting/

```
pip install boxcounting
```

## Example - box counting of a 2D image

Consider a fractal called the Apollonian gasket: see https://en.wikipedia.org/wiki/Apollonian_gasket.

```
from PIL import Image
from boxcounting import boxCount
import numpy as np

# Open image
imagedata = Image.open("Apollonian_gasket.gif")

# Convert to numpy array
imagedata = np.asarray(imagedata)

# Threshold the image
imagedata = imagedata < 198

# Calculate box counting dimension
boxCountObj = boxCount(imagedata)
n, r, df = boxCountObj.calculateBoxCount()

print('Box sizes (r):', r)
print('Box count n(r):', n)

# Calculate local slope for box size (r) < 100
print('Fractal (box-counting) dimension is ' + str(np.mean(df[:6])) + ' +/- ' + str(np.std(df[:6])))
```
