#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 07:55:59 2019

@author: konstantinos.falangis
"""
import unittest
import numpy as np
from fabozzi_functions import loan_payment

class NamesTestCase(unittest.TestCase):
    """Tests for 'fabozzi_functions.py'."""
    def test_loan_payment(self):
        """Do loan_payment function work?"""
        loan_pmt = round(loan_payment(LB=200000, i=7.5, n=30),2)
        self.assertEqual(loan_pmt, (round(np.pmt(0.075/12, 12*30, 200000), 2)) * (-1))
        
unittest.main()

