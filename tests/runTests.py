import array
import numpy as np
import sys
sys.path.append('../src/boxcounting/')
from box_count import boxCount
import unittest

#---------------------------------------------------------------------#

# Author: Abhishek Harikrishnan
# Email: abhishek.harikrishnan@fu-berlin.de
# Last updated: 28-11-2023
# Tests to ensure correct working of boxCount python module

#---------------------------------------------------------------------#

class TestBoxCount(unittest.TestCase):
	
	'''
	
	This script tests the 1D, 2D and 3D boxcounts of the boxCount code.
	In each case, the number of boxes for each box size was caclulated 
	with the boxcount MATLAB code. See here: https://de.mathworks.com/matlabcentral/fileexchange/13063-boxcount.
	
	For the 1D case, the randcantor function was used as follows:
	
	c = randcantor(0.9, 1024, 1);
	[n, r] = boxcount(c)
	
	For the 2D case, the Apollonian gasket image was used as follows:
	
	c = imread('Apollonian_gasket.gif');
	c = (c<198);
	[n, r] = boxcount(c)
	
	For the 3D case, the randcantor function was again used as follows:
	
	c = randcantor(0.9, 32, 3);
	[n, r] = boxcount(c)
	
	NOTE: The randcantor function was used without a seed and is hence
	not reproducible. However, the Apollonian gasket image can be obtained
	from https://en.wikipedia.org/wiki/File:Apollonian_gasket.gif.
	
	'''
	
	def test_1d_boxCount(self):
		
		print('Running 1D test case...')
		
		_array = array.array('B')
		
		fid = open('1D_random_cantor.bin', 'rb')
		_array.fromfile(fid, (1024))
		fid.close()
		
		_array = np.reshape(_array, [1024])

		boxCountObj = boxCount(_array)
		n, r, df = boxCountObj.calculateBoxCount()
		
		n_calculated = [491, 273, 148, 81, 43, 25, 14, 8, 4, 2, 1]
		
		self.assertEqual(n.tolist(), n_calculated)
	
	def test_2d_boxCount(self):
		
		print('Running 2D test case...')
		
		_array = array.array('B')
		
		fid = open('2D_apollonian_gasket.bin', 'rb')
		_array.fromfile(fid, (600 * 600))
		fid.close()
		
		_array = np.reshape(_array, [600, 600])

		boxCountObj = boxCount(_array)
		n, r, df = boxCountObj.calculateBoxCount()
		
		n_calculated = [21831, 7473, 2732, 1045, 414, 163, 64, 22, 9, 4, 1]
		
		self.assertEqual(n.tolist(), n_calculated)
		
	def test_3d_boxCount(self):
		
		print('Running 3D test case...')
		
		_array = array.array('B')
		
		fid = open('3D_random_cantor.bin', 'rb')
		_array.fromfile(fid, (32 * 32 * 32))
		fid.close()
		
		_array = np.reshape(_array, [32, 32, 32])

		boxCountObj = boxCount(_array)
		n, r, df = boxCountObj.calculateBoxCount()
		
		n_calculated = [19401, 2695, 375, 51, 7, 1]
		
		self.assertEqual(n.tolist(), n_calculated)

if __name__ == '__main__':
	
	# Run unit tests.
	# If everything checks out, it'll print OK.
	
    unittest.main()
