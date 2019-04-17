#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''pair class , represent a position'''

__author__ = 'tzx'

class pair(tuple):
    def __new__(self, x, y):
        return tuple.__new__(self, (x, y))

    def __add__(self, other):
        return pair(self[0]+other[0], self[1]+other[1])

    def __sub__(self, other):
        return pair(self[0]-other[0], self[1]-other[1])