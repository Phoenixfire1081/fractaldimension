import numpy as np
from numba import jit

#---------------------------------------------------------------------#

# Author: Abhishek Harikrishnan
# Email: abhishek.harikrishnan@fu-berlin.de
# Last updated: 26-11-2023
# Port of the MATLAB box-counting code by F. Moisy
# https://de.mathworks.com/matlabcentral/fileexchange/13063-boxcount

#---------------------------------------------------------------------#

class boxCount:
	
	'''
	
	This calculates the box-counting dimension of a given d-dimensional
	array. d = 1, 2, 3 are supported. The box sizes are in powers of 2.
	If the largest dimension of a given array i.e., max(np.shape(c)) <= 2**p,
	then the array is padded with zeros in all dimensions. For instance, an 
	image having size 450 x 300 will be padded to 512 x 512.
	
	With a non-overlapping fixed grid scan (see https://en.wikipedia.org/wiki/Box_counting),
	boxes of various size are used to count the number of non-empty boxes.
	The box sizes range from the smallest grid size to 2**p
	
	NOTE: In this class, computeFast, computeFast2, computeFast3 are 
	utility functions which operate on only the given parameters.
	The @staticmethod decorator is necessary to make numba work inside 
	a class. To use the class without numba simply uncomment @staticmethod 
	and @jit(nopython=True)
	
	'''
	
	def __init__(self, c):
		
		# Determine the smallest value of p such that the largest dimension
		# is less than or equal to 2**p. This gives the width of the padded
		# box.
		
		self.p = np.ceil(np.log(max(np.shape(c)))/np.log(2))
		self.width = 2**self.p
		
		# Determine number of dimensions
		
		self.dim = len(np.shape(c))
		
		# Pad the data with the determined width
		
		if self.dim == 1:
			
			mz = np.zeros((int(self.width)), dtype = bool)
			mz[:np.shape(c)[0]] = c
			self.paddedData = mz
		
		elif self.dim == 2:
			
			mz = np.zeros((int(self.width), int(self.width)), dtype = bool)
			mz[:np.shape(c)[0], :np.shape(c)[1]] = c
			self.paddedData = mz
		
		elif self.dim == 3:
			
			mz = np.zeros((int(self.width), int(self.width), int(self.width)), dtype = bool)
			mz[:np.shape(c)[0], :np.shape(c)[1], :np.shape(c)[2]] = c
			self.paddedData = mz
		
		else:
			
			print('Check the dimensions of the input data. d = 1, 2, 3 are supported.')

	@staticmethod
	@jit(nopython=True)
	def computeFast(xlen, c, p, width, reverse_range, n, r):
		
		# Box count for 1d array
		
		def getSum(xlen, _array):
			_sum = 0
			for i in range(xlen):
				if _array[i]:
					_sum = _sum + 1

			return _sum

		n[0] = getSum(xlen, c)

		for g in reverse_range:
			c_sum = 0
			siz = 2**(p-g)
			siz2 = int(round(siz/2))
			
			for i in range(0, int(width-siz)+1, int(siz)):
				c[i] = int(c[i]) or int(c[i+siz2])
				c_sum = c_sum + c[i]
			n[-g-1] = c_sum

		return n

	@staticmethod
	@jit(nopython=True)
	def computeFast2(xlen, ylen, c, p, width, reverse_range, n, r):
		
		# Box count for 2d array
		
		def getSum(xlen, ylen, _array):
			_sum = 0
			for i in range(xlen):
				for j in range(ylen):
					if _array[i, j]:
						_sum = _sum + 1

			return _sum

		n[0] = getSum(xlen, ylen, c)

		for g in reverse_range:
			c_sum = 0
			siz = 2**(p-g)
			siz2 = int(round(siz/2))
			
			for i in range(0, int(width-siz)+1, int(siz)):
				for j in range(0, int(width-siz)+1, int(siz)):
					c[i,j] = int(c[i,j]) or int(c[i+siz2, j]) or \
					int(c[i, j+siz2]) or int(c[i+siz2, j+siz2])
					c_sum = c_sum + c[i,j]
			n[-g-1] = c_sum

		return n

	@staticmethod
	@jit(nopython=True)
	def computeFast3(xlen, ylen, zlen, c, p, width, reverse_range, n, r):
		
		# Box count for 3d array
		
		def getSum(xlen, ylen, zlen, _array):
			_sum = 0
			for i in range(xlen):
				for j in range(ylen):
					for k in range(zlen):
						if _array[i, j, k]:
							_sum = _sum + 1

			return _sum

		n[0] = getSum(xlen, ylen, zlen, c)

		for g in reverse_range:
			c_sum = 0
			siz = 2**(p-g)
			siz2 = int(round(siz/2))
			
			for i in range(0, int(width-siz)+1, int(siz)):
				for j in range(0, int(width-siz)+1, int(siz)):
					for k in range(0, int(width-siz)+1, int(siz)):
						c[i,j,k] = int(c[i,j,k]) or int(c[i+siz2, j, k]) or \
						int(c[i, j+siz2, k]) or int(c[i+siz2, j+siz2, k]) or \
						int(c[i,j,k+siz2]) or int(c[i+siz2,j,k+siz2]) or \
						int(c[i,j+siz2,k+siz2]) or int(c[i+siz2,j+siz2,k+siz2])
						c_sum = c_sum + c[i,j,k]
			n[-g-1] = c_sum

		return n

	def calculateBoxCount(self):
		
		reverse_range = np.array([i for i in range(int(self.p))[::-1]])
		n = np.zeros((len(reverse_range) + 1), dtype = np.float32)
		r = 2**np.array(range(int(self.p)+1))
		
		if len(np.shape(self.paddedData)) == 1:

			xlen, = np.shape(self.paddedData)
			n = self.computeFast(xlen, self.paddedData, self.p, self.width, reverse_range, n, r)

		elif len(np.shape(self.paddedData)) == 2:
			xlen, ylen = np.shape(self.paddedData)
			n = self.computeFast2(xlen, ylen, self.paddedData, self.p, self.width, reverse_range, n, r)
			
		elif len(np.shape(self.paddedData)) == 3:
			xlen, ylen, zlen = np.shape(self.paddedData)
			n = self.computeFast3(xlen, ylen, zlen, self.paddedData, self.p, self.width, reverse_range, n, r)
			
		else:
			print('Exceeded 3 dimensions. Not implemented.')
			raise NotImplementedError
		
		df = - np.diff(np.log(n)) / np.diff(np.log(r))
		
		return n, r, df
