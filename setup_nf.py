from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy
import argparse

parser = argparse.ArgumentParser(description='Cython setup tool')
parser.add_argument('-r', '--rootDir', metavar="ROOT DIRECTORY", action='store', type=str, help="root directory for the project")
args = parser.parse_args()

argsDict = vars(args)
rootDirectory = argsDict['rootDir'][:-1] if argsDict['rootDir'].endswith("/") else argsDict['rootDir']

setup(ext_modules=cythonize(f'{rootDirectory}/outTree_ec_minimization/algo.pyx', language_level = "3"),include_dirs=[numpy.get_include()])