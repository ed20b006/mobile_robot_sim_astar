# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 11:39:12 2022

@author: its_a

"""
from optimizer import Optimizer


test = Optimizer([0, 0, 0.75])
test.get_gtg_data(0.1, 0.0)
test.get_obs_data(1.5, 1, 0, 0)
print(test.optimize())


