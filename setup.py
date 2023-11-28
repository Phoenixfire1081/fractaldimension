import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="boxcounting", 
    version="1.0.0.0", 
    author="Abhishek Harikrishnan", 
    author_email="abhishek.harikrishnan@fu-berlin.de", 
    packages=["boxcounting"], 
    description="A python port of the MATLAB boxcount to calculate the \
    fractal (box-counting) dimension of 1D, 2D or 3D data", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/Phoenixfire1081/fractaldimension", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=[] 
) 
