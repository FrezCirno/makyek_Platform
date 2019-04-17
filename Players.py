#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''players支持'''
__author__ = 'tzx'

import random
from pair import *


def inputbuf():
    def __g():
        while True:
            buffer = input().split()
            for i in buffer:
                if i.isdigit():
                    yield int(i)
                else:
                    yield i
    __iter = __g()

    def __f(n=1):
        if n == 1:
            return next(__iter)
        else:
            return [next(__iter) for i in range(n) if True]
    return __f


class player(object):
    '''
    DESP    玩家类
    '''
    __pattern = {0: ' ', 1: 'o', 2: 'x'}
    __name2step = {'nw': (-1, -1), 'n': (-1, 0), 'ne': (-1, 1), 'w': (0, -1),
                   'e': (0, 1), 'sw': (1, -1), 's': (1, 0), 'se': (1, 1)}
    __nochess = 0

    def __init__(self, mychess, size):
        self.__author__ = input('Please input your name: ')
        self.__mychess = mychess
        self.__otherchess = 3-mychess
        self.__pattern[mychess] = input('Please input your chess pattern: ')
        if self.__pattern[mychess] == '':
            self.__pattern[mychess] = 'o'
        self.__pattern[self.__otherchess] = input(
            'Please input your opponent\'s chess pattern: ')
        if self.__pattern[self.__otherchess] == '':
            self.__pattern[self.__otherchess] = 'x'
        self.__pattern[self.__nochess] = input('Please input board pattern: ')
        if self.__pattern[self.__nochess] == '':
            self.__pattern[self.__nochess] = ' '
        self.__size = size

    def printBoard(self):
        print('  ', end='')
        for n in range(12):
            print("%2d" % n, end='')
        print()
        for i, row in enumerate(self.__board):
            print("%2d" % i, *[self.__pattern[i] for i in row])

    def turn(self, board):
        Input = inputbuf()
        self.__board = board
        self.printBoard()
        x, y, d = Input(3)
        return (x, y), self.__name2step[d]


class ai(object):
    '''AI in Program'''
    __author__ = 'tzx'
    __author__ = 'AI酱'

    __name2step = {'nw': (-1, -1), 'n': (-1, 0), 'ne': (-1, 1), 'w': (0, -1),
                   'e': (0, 1), 'sw': (1, -1), 's': (1, 0), 'se': (1, 1)}
    __level = 1
    __nochess = 0
    # 0--easy 1--normal 2--hard

    def onboard(self, pos):
        '''
        DESP    返回x,y是否在棋盘上
        '''
        return 0 <= pos[0] < self.__size and 0 <= pos[1] < self.__size

    def tryget(self, pos, turn=None):
        '''
        DESP    试图读取x,y处的棋子
        RET     指定turn时返回bool
                未指定时返回[0|False|1|2]
        '''
        if turn != None:
            return 0 <= pos[0] < self.__size and 0 <= pos[1] < self.__size and self.__nowboard[pos[0]][pos[1]] == turn
        else:
            return 0 <= pos[0] < self.__size and 0 <= pos[1] < self.__size and self.__nowboard[pos[0]][pos[1]]

    def __set(self, pos, turn):
        '''
        DESP    简单设置，无检查
        '''
        self.__nowboard[pos[0]][pos[1]] = turn
        # 更新chesslists
        if turn == 0:
            self.__chesslists.remove(pos)
        else:
            self.__chesslists.append(pos)

    def __init__(self,  mychess, size):
        '''
        DESP    初始化
        mychess AI的棋子
        size    棋盘尺寸
        '''
        self.__mychess = mychess
        self.__otherchess = 3-mychess
        self.__size = size

    def turn(self, board):
        '''
        DESP    AI思考函数，根据难度设置选择不同函数
                并保存棋盘，生成棋子列表
        board   int[][]     现在棋盘
        RET     ((int, int), (int, int))
        '''
        # 复制board
        self.__nowboard = board
        self.__chesslists = []
        for x in range(self.__size):
            for y in range(self.__size):
                if self.__nowboard[x][y] != self.__nochess:
                    self.__chesslists.append(pair(x, y))

        if self.__level == 0:
            return self.__AI_easy()
        elif self.__level == 1:
            return self.__AI_normal()
        elif self.__level == 2:
            return self.__AI_hard()
        else:
            return False

    def __AI_easy(self):
        '''
        DESP    easy模式AI，随机下点
        '''
        while True:
            pos = self.__chesslists[random.randint(0, 12)]
            d = (random.randint(-1, 1), random.randint(-1, 1))
            if d in self.__name2step.values() and self.tryget(pos, self.__mychess) and self.tryget(pos+d, self.__nochess):
                break
        return pos, d

    def __AI_normal(self):
        '''
        DESP    normal模式AI,使用AB剪枝算法优化
                只用一个board完成全部过程
                place函数执行判断及移动过程
                递归
                undo函数执行撤销过程
        '''
        alpha = -30000
        beta = 30000
        global depths
        depths = 4  # 深度为3层
        return self.ABsearch(depths, alpha, beta, self.__mychess)

    def eval(self, pos, d):
        '''
        DESP    评估函数，返回某一步移动对于我(算法执行者)的分数
        pos     pair        移动位置
        d       pair        移动方向
        RET     int         分数
        '''
        value = 0
        # new_x, new_y = x+d[0], y+d[1]
        # 统计自身棋子数，一枚1500分
        for pos in self.__chesslists:
            if self.tryget(pos, self.__mychess):
                value += 150
        # 统计落点周围双方棋子数量
        my_chess_around = 0
        other_chess_around = 0
        for d in self.__name2step.values():
            new_pos = pos+d
            if self.tryget(new_pos, self.__mychess):
                my_chess_around += 1
            elif self.tryget(new_pos, self.__otherchess):
                other_chess_around += 1
        # 核算分数
        value = value+30*my_chess_around-10*other_chess_around
        # 向中间移动
        if pos[0] in range(5):
            if d in ((1, 0), (1, -1), (1, 1)):
                value += 5*new_pos[0]
            elif d in ((-1, 0), (-1, -1), (-1, 1)):
                value -= 20*pos[0]
        elif pos[0] in range(7, 12):
            if d in ((-1, 0), (-1, -1), (-1, 1)):
                value += 5*(11-new_pos[0])
            elif d in ((1, 0), (1, -1), (1, 1)):
                value -= 20*(11-pos[0])
        if pos[1] in range(5):
            if d in ((0, 1), (1, 1), (-1, 1)):
                value += 5*new_pos[1]
            elif d in ((0, -1), (-1, -1), (1, -1)):
                value -= 20*pos[1]
        elif pos[1] in range(7, 12):
            if d in ((0, -1), (-1, -1), (1, -1)):
                value += 5*(11-new_pos[1])
            elif d in ((0, 1), (1, 1), (-1, 1)):
                value -= 20*(11-pos[1])
        return value

    def place(self, pos, d, nowturn):
        '''
        DESP    执行移动，返回执行结果
        pos     pair        坐标
        d     (int, int)  方向
        nowturn [1|2]       深度为depth时的棋手
        RET     False|thismove  移动成功与否
        thismove
                结构：[pair ori_pos, pair d, pos, pos,...]
                用push_back()表示新变更
                用pop()表示复原
        '''
        new_pos = pos+d
        self.__set(pos, self.__nochess)
        self.__set(new_pos, nowturn)
        otherturn = 3-nowturn
        thismove = [pos, d]
        # 挑
        intervention_dir = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for ind in intervention_dir:
            pos1 = new_pos+ind
            pos2 = new_pos-ind
            if self.tryget(pos1, otherturn) and self.tryget(pos2, otherturn):
                self.__flip(pos1)
                self.__flip(pos2)
                thismove.append(pos1)
                thismove.append(pos2)
        # 夹
        custodian_dir = [(1, 0), (-1, 0), (0, 1), (0, -1),
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for cud in custodian_dir:
            pos1 = new_pos + cud
            pos2 = new_pos + cud + cud
            if self.tryget(pos2, nowturn) and self.tryget(pos1, otherturn):
                self.__flip(pos1)
                thismove.append(pos1)
        return thismove

    def __flip(self, pos):
        '''
        DESP    翻转棋子函数，吃子用
        '''
        self.__nowboard[pos[0]][pos[1]] = 3-self.__nowboard[pos[0]][pos[1]]

    def undo(self, thismove):
        '''
        DESP    撤销一步
        '''
        pos = thismove[0]
        new_pos = pos+thismove[1]
        self.__set(pos, self.tryget(new_pos))
        self.__set(new_pos, self.__nochess)
        for pos in thismove[2:]:
            self.__flip(pos)

    def ABsearch(self, depth, alpha, beta, nowturn):
        '''
        DESP    alpha-beta搜索
                若新搜索节点的估值比alpha大，就不再搜索
                若新搜索节点的估值比beta小，就不再继续搜索
        depth   搜索深度
        alpha   已搜索过的子节点中最大值
        beta    已搜索过的子节点中最小值
        nowturn [0|1]       此次搜索是哪一方
        RET     int|final   alpha或beta或((int, int),(int, int))
        '''
        # 我的回合，返回最好结果alpha
        if nowturn == self.__mychess:
            for pos in self.__chesslists:
                if self.tryget(pos, nowturn):
                    for d in self.__name2step.values():
                        if self.tryget(pos+d, self.__nochess):
                            thismove = self.place(pos, d, nowturn)
                            # 非叶子节点，递归
                            if depth:
                                val = self.ABsearch(
                                    depth-1, alpha, beta,  3-nowturn)
                                # 和现在的alpha比较，更新最大值
                                # print('  '*depth, 'Max ', pos,d,  val, sep='')
                                if val > alpha:
                                    alpha = val
                                    # 暂存最佳走法
                                    if depth == depths:
                                        final = (pos, d)
                            # 叶子节点，估值，用alpha保存最大值
                            else:
                                alpha = max(alpha, self.eval(pos, d))
                            # 恢复原棋盘
                            self.undo(thismove)
                            # 某一子节点的评价值高于上一层已找到的beta，默认对方不会选择这步，故不再判断此层其他子节点
                            if beta <= alpha:
                                return alpha
            # 返回最佳走法
            if depth == depths:
                return final
            return alpha
        # 对手回合，找最小值beta
        else:
            for pos in self.__chesslists:
                if self.tryget(pos, nowturn):
                    for d in self.__name2step.values():
                        if self.tryget(pos+d, self.__nochess):
                            thismove = self.place(pos, d, nowturn)
                            # 非叶子结点，递归
                            if depth:
                                val = self.ABsearch(
                                    depth-1, alpha, beta, 3-nowturn)
                                # print('  '*depth, 'Min ', pos,d, val, sep='')
                                # 和现在的beta比较，更新最小值
                                beta = min(beta, val)
                            # 叶子节点，估值，beta存储最小值
                            else:
                                beta = min(beta, self.eval(pos, d))
                            # 恢复原棋盘
                            self.undo(thismove)
                            # 某一子节点的评价值低于上一层已找到的alpha，自己不会这样下，不再判断此层其他子节点
                            if beta <= alpha:
                                return beta
            return beta

    def __AI_hard(self):
        pass
