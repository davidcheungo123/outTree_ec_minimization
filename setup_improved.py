from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

setup(ext_modules=cythonize('algo_improved.pyx', language_level = "3"),include_dirs=[numpy.get_include()])

# ext_modules=[
#     Extension("algo_improved",
#               ["algo_improved.pyx"],
#               extra_compile_args = ["/openmp" ],
#               extra_link_args=['/openmp']
#               ) 
# ]

# setup(name="algo_improved", ext_modules=cythonize(ext_modules) ,include_dirs=[numpy.get_include()], cmdclass = {'build_ext': build_ext})

