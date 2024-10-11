#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2016-2021 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2016-2021 Joshua Przyborowski - https://github.com/JoshuaPrzyborowski

    $FileInfo: setup.py - Last Update: 1/4/2021 Ver. 0.3.0 RC 1 - Author: cooldude2k $
'''

import re
import os
import sys
import time
import datetime
import platform
import pkg_resources
from setuptools import setup, find_packages

install_requires = []

pygenbuildinfo = True
verinfofilename = os.path.realpath("."+os.path.sep+"pydice.py")
verinfofile = open(verinfofilename, "r")
verinfodata = verinfofile.read()
verinfofile.close()
setuppy_verinfo_esc = re.escape("__version_info__ = (")+"(.*)"+re.escape(");")
setuppy_verinfo = re.findall(setuppy_verinfo_esc, verinfodata)[0]
setuppy_verinfo_exp = [vergetspt.strip().replace("\"", "")
                       for vergetspt in setuppy_verinfo.split(',')]
setuppy_dateinfo_esc = re.escape(
    "__version_date_info__ = (")+"(.*)"+re.escape(");")
setuppy_dateinfo = re.findall(setuppy_dateinfo_esc, verinfodata)[0]
setuppy_dateinfo_exp = [vergetspt.strip().replace("\"", "")
                        for vergetspt in setuppy_dateinfo.split(',')]
pymodule = {}
pymodule['version'] = str(setuppy_verinfo_exp[0])+"." + \
    str(setuppy_verinfo_exp[1])+"."+str(setuppy_verinfo_exp[2])
pymodule['versionrc'] = int(setuppy_verinfo_exp[4])
pymodule['versionlist'] = (int(setuppy_verinfo_exp[0]), int(setuppy_verinfo_exp[1]), int(
    setuppy_verinfo_exp[2]), str(setuppy_verinfo_exp[3]), int(setuppy_verinfo_exp[4]))
pymodule['verdate'] = str(setuppy_dateinfo_exp[0])+"." + \
    str(setuppy_dateinfo_exp[1])+"."+str(setuppy_dateinfo_exp[2])
pymodule['verdaterc'] = int(setuppy_dateinfo_exp[4])
pymodule['verdatelist'] = (int(setuppy_dateinfo_exp[0]), int(setuppy_dateinfo_exp[1]), int(
    setuppy_dateinfo_exp[2]), str(setuppy_dateinfo_exp[3]), int(setuppy_dateinfo_exp[4]))
pymodule['name'] = 'PyDice'
pymodule['author'] = 'Joshua Przyborowski'
pymodule['authoremail'] = 'joshua.przyborowski@gmail.com'
pymodule['maintainer'] = 'Joshua Przyborowski'
pymodule['maintaineremail'] = 'joshua.przyborowski@gmail.com'
pymodule['description'] = 'A barcode library/module for python.'
pymodule['license'] = 'Revised BSD License'
pymodule['keywords'] = 'barcode barcodegenerator barcodes codabar msi code11 code-11 code39 code-39 code93 code-93 ean ean13 ean-13 ean2 ean-2 ean5 ean-5 ean8 ean-8 itf itf14 itf-14 stf upc upca upc-a upce upc-e'
pymodule['url'] = 'https://github.com/GameMaker2k/PyDice'
pymodule['downloadurl'] = 'https://github.com/JoshuaPrzyborowski/PyDice/archive/master.tar.gz'
pymodule['packages'] = find_packages()
pymodule['packagedata'] = {'upcean': ['*.otf', '*.ttf', '*.dtd', '*.xsl', '*.xsd', '*.rng', '*.rnc'],
                           'upcean/fonts': ['*.otf', '*.ttf'], 'upcean/xml': ['*.dtd', '*.xsl', '*.xsd', '*.rng', '*.rnc']}
pymodule['includepackagedata'] = True
pymodule['installrequires'] = [install_requires]
pymodule['longdescription'] = 'PyDice is a barcode library/module for Python. It supports the barcode formats upc-e, upc-a, ean-13, ean-8, ean-2, ean-5, itf14, codabar, code11, code39, code93, and msi.'
pymodule['platforms'] = 'OS Independent'
pymodule['zipsafe'] = False
pymodule['pymodules'] = ['upcean']
pymodule['classifiers'] = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Customer Service',
    'Intended Audience :: Developers',
    'Intended Audience :: Other Audience',
    'License :: OSI Approved',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: OS/2',
    'Operating System :: OS Independent',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Office/Business',
    'Topic :: Office/Business :: Financial',
    'Topic :: Office/Business :: Financial :: Point-Of-Sale',
    'Topic :: Utilities',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules'
]
if(len(sys.argv) > 1 and (sys.argv[1] == "versioninfo" or sys.argv[1] == "getversioninfo")):
    import json
    pymodule_data = json.dumps(pymodule)
    print(pymodule_data)
    sys.exit()
if(len(sys.argv) > 1 and (sys.argv[1] == "sourceinfo" or sys.argv[1] == "getsourceinfo")):
    srcinfofilename = os.path.realpath("."+os.path.sep+pkg_resources.to_filename(
        pymodule['name'])+".egg-info"+os.path.sep+"SOURCES.txt")
    srcinfofile = open(srcinfofilename, "r")
    srcinfodata = srcinfofile.read()
    srcinfofile.close()
    srcinfolist = srcinfodata.split('\n')
    srcfilelist = ""
    srcpdir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    for ifile in srcinfolist:
        srcfilelist = "."+os.path.sep+srcpdir+os.path.sep+ifile+" "+srcfilelist
    print(srcfilelist)
    sys.exit()
if(len(sys.argv) > 1 and sys.argv[1] == "cleansourceinfo"):
    os.system("rm -rfv \""+os.path.realpath("."+os.path.sep+"dist\""))
    os.system("rm -rfv \""+os.path.realpath("."+os.path.sep +
              pkg_resources.to_filename(pymodule['name'])+".egg-info\""))
    sys.exit()

setup(
    name=pymodule['name'],
    version=pymodule['version'],
    author=pymodule['author'],
    author_email=pymodule['authoremail'],
    maintainer=pymodule['maintainer'],
    maintainer_email=pymodule['maintaineremail'],
    description=pymodule['description'],
    license=pymodule['license'],
    keywords=pymodule['keywords'],
    url=pymodule['url'],
    download_url=pymodule['downloadurl'],
    packages=pymodule['packages'],
    package_data=pymodule['packagedata'],
    include_package_data=pymodule['includepackagedata'],
    install_requires=pymodule['installrequires'],
    long_description=pymodule['longdescription'],
    platforms=pymodule['platforms'],
    zip_safe=pymodule['zipsafe'],
    py_modules=pymodule['pymodules'],
    classifiers=pymodule['classifiers']
)
