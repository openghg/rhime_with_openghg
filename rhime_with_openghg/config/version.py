#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:21:27 2020

@author: al18242

This file contains a method of obtaining the version 
of the code used to generate output.
---------------------------------------
Updated by Eric Saboya (Dec. 2022)

"""

import subprocess
from rhime_with_openghg.config.paths import Paths

rhime_path = Paths.rhime

def code_version():
    '''   
    Use git describe to return the latest tag 
    (and git hash if applicable).
    -----------------------------------
    Returns
      version : String defining the version of the code used, 
                or "Unknown" if git is unavailable
    -----------------------------------
    '''
    try:
        output = subprocess.run(['git', 'describe'], 
                                capture_output = True,
                                cwd = rhime_path,
                                universal_newlines = True)
        #remove newlines and cast as string
        version = str(output.stdout.strip('\n'))
    except:
        print("WARNING: Unable to identify version using git."
              " Check that git is available to the python process.")
        version = "Unknown"
        
    return version
