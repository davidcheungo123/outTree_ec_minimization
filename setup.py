from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

setup(ext_modules=cythonize('algo.pyx', language_level = "3"),include_dirs=[numpy.get_include()])