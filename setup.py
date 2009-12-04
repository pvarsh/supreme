#!/usr/bin/env python

VERSION = '0.1'

import os
import sys
from glob import glob

import setuptools
import numpy as np
from numpy.distutils.core import setup, Extension

def packages_and_tests(packages):
    """For each package, add the corresponding tests directory.

    """
    out = []
    for p in packages:
        out.append(p)

        test_dir = p + '.tests'
        if os.path.isdir(test_dir.replace('.','/')):
            out.append(test_dir)

    return out

def CExtension(name,files,**kwargs):
    """Build an extension with a dummy Py_InitModule.

    """
    path = os.path.dirname(name)
    libname = os.path.basename(name)
    initfile = os.path.join(path, libname + 'init.c')
    if not os.path.exists(initfile):
        f = open(initfile,'w')
        f.write('''
#include <Python.h>

PyMethodDef methods[] = {
  {NULL, NULL},
};

void
init%(module)s()
{
    (void)Py_InitModule("%(module)s", methods);
}
''' % {'module':libname})

    if not initfile in files:
        files.append(initfile)
    return Extension(name,files,**kwargs)

dpt_extensions = [Extension('supreme/lib/dpt/' + dpt_mod,
                            ['supreme/lib/dpt/' + dpt_mod + '.c'],
                            include_dirs=[np.get_include()],) for dpt_mod in
                  ('int_array', 'connected_region',
                   'connected_region_handler', 'ccomp', 'base')]

setup(
  name = 'supreme',
  version = VERSION,
  packages = packages_and_tests(setuptools.find_packages()),

  ext_modules = [CExtension('supreme/ext/libsupreme_',
                            glob('supreme/ext/*.c')),

                 CExtension('supreme/lib/klt/libklt_',
                            ['supreme/lib/klt/' + f for f in
                                 ['convolve.c', 'error.c', 'pnmio.c', \
                                  'pyramid.c', 'selectGoodFeatures.c',\
                                  'storeFeatures.c', 'trackFeatures.c', \
                                  'klt.c', 'klt_util.c', 'writeFeatures.c']]),

                 CExtension('supreme/lib/fast/libfast_',
                            glob('supreme/lib/fast/*.c')),
                ] + dpt_extensions,

  package_data = {
      '': ['*.txt', '*.png', '*.jpg', '*.pgm'],
  },

  zip_safe = False,

  author = "Stefan van der Walt",
  author_email = "<stefan.no-spam(at)mentat.za.net>",
  description = "SUper REsolution MEthods",
  url = "http://mentat.za.net",
  license = "GPL",
)
