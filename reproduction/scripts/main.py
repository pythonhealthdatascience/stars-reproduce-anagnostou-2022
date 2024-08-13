# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 08:53:41 2021

@author: anastasia anagnostou
"""

import sys

sys.dont_write_bytecode = True

import utils as u
import model as m

u.args()

m.runSim(u.RANDOM_SEED, u.replications)

