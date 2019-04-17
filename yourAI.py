#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''put your AI here'''


class ai(object):
    __author__ = 'Put your name here'
    __dirname = [['nw', 'n', 'ne'],
                 ['w', '', 'e'],
                 ['sw', 's', 'se']]

    def __init__(self, mychess, size):
        self.__mychess = mychess
        self.__otherchess = 3-mychess
        self.__nochess = 0
        self.__size = size

    def turn(self, board):
        '''AI思考函数'''
        pass
