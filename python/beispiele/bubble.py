# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 14:37:34 2017

@author: gunny
"""

def bubble(lst):
    for i in range( len( lst ) ):
        for k in range( len( lst ) - 1, i, -1 ):
          if ( lst[k] < lst[k - 1] ):
            lst[k - 1], lst[k] = lst[k], lst[k - 1]



unsortet = [9,2,6,1,7,3,4,8,5,0]
print(unsortet)
bubble(unsortet)
print(unsortet)
