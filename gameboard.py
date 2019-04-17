#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''挑夹棋游戏引擎类'''

__author__ = 'tzx'


class board(object):
    '''
    DESP    一个简单的挑夹棋游戏引擎
            内部用int[][]表示棋盘
            值0/1/2分别表示空/玩家1棋子/玩家2棋子
    '''
    __dirdic = {'n': (-1, 0), 's': (1, 0), 'w': (0, -1), 'e': (0, 1),
                'nw': (-1, -1), 'ne': (-1, 1), 'sw': (1, -1), 'se': (1, 1)}
    __none = 0
    __nowturn = 1
    __otherturn = 2
    __times = 0

    def __init__(self, size=12):
        '''
        size    int     棋盘尺寸，默认是正方形
                        暂时不需要更改
        '''
        self.__size = size
        self.__board = [
            [0 for j in range(size)] for i in range(size)]
        self.__board[2][2] = self.__board[2][3] = self.__board[2][4] = self.__board[6][6] = self.__board[
            6][7] = self.__board[6][8] = self.__board[9][2] = self.__board[10][2] = 1
        self.__board[2][9] = self.__board[3][9] = self.__board[10][7] = self.__board[5][3] = self.__board[
            5][4] = self.__board[5][5] = self.__board[10][8] = self.__board[10][9] = 2

    def onboard(self, pos):
        '''
        DESP    判断pos是否在棋盘上
        pos     (int, int)
        RET     bool
        '''
        return 0 <= pos[0] < self.__size and 0 <= pos[1] < self.__size

    def tryget(self, pos, turn=None):
        '''
        DESP    未指定turn时，返回pos处的状态
                指定turn时，返回pos处为turn的棋子的真假
        pos     (int, int)
        turn    int
        RET     未指定turn  [0|1|2|False]
                指定turn    [True|False]
        '''
        if turn != None:
            return 0 <= pos[0] < self.__size and 0 <= pos[1] < self.__size and self.__board[pos[0]][pos[1]] == turn
        else:
            return 0 <= pos[0] < self.__size and 0 <= pos[1] < self.__size and self.__board[pos[0]][pos[1]]

    def __set(self, pos, turn):
        '''
        DESP    将pos处设置为turn
        pos     (int, int)
        turn    [1|2]
        '''
        self.__board[pos[0]][pos[1]] = turn

    def whoseTurn(self):
        '''
        DESP    返回当前到谁的回合
        RET     [1|2]
        '''
        return self.__nowturn

    def gettimes(self):
        '''
        DESP    返回当前总步数
        '''
        return self.__times

    def getsize(self):
        '''
        DESP    返回棋盘尺寸，暂时无意义
        '''
        return self.__size

    def check(self):
        '''
        DESP    检查游戏是否结束，未结束返回0，结束返回1/2
        '''
        chess1 = 0
        for row in self.__board:
            for i in row:
                if i == 1:
                    chess1 += 1
        if chess1 == 0:
            return 2
        elif chess1 == 12:
            return 1
        else:
            return 0

    def place(self, pos, d):
        '''
        DESP    落子指令
        pos     (int, int)
        d       (int, int)  ['n'|'s'|'w'|'e'|'nw'|'ne'|'sw'|'se']
        RET     bool    表示是否成功
        '''
        if not isinstance(pos, tuple) or len(pos) != 2 or not isinstance(pos[0], int) or not isinstance(pos[1], int):
            return False

        newPos = (pos[0]+d[0], pos[1]+d[1])
        if not self.tryget(pos, self.__nowturn) or not self.tryget(newPos, self.__none):
            return False

        self.__set(pos, self.__none)
        self.__set(newPos, self.__nowturn)
        del pos
        pos = newPos
        for dirStep in self.__dirdic.values():
            # 夹
            around = (pos[0]+dirStep[0], pos[1]+dirStep[1])
            around2 = (pos[0]+2*dirStep[0], pos[1]+2*dirStep[1])

            if self.tryget(around, self.__otherturn) and self.tryget(around2, self.__nowturn):
                self.__set(around, self.__nowturn)
            # 挑
            raround = (pos[0]-dirStep[0], pos[1]-dirStep[1])
            if self.tryget(around, self.__otherturn) and self.tryget(raround, self.__otherturn):
                self.__set(around, self.__nowturn)
                self.__set(raround, self.__nowturn)
        self.__otherturn = self.__nowturn
        self.__nowturn = 3-self.__nowturn
        self.__times += 1
        return True

    def printBoard(self, pat='012'):
        '''
        DESP    以符号pat打印棋盘
        '''
        print('  ', end='')
        for n in range(12):
            print("%2d" % n, end='')
        print()
        for i, row in enumerate(self.__board):
            print("%2d" % i, *[pat[i] for i in row])

    def outputBoard(self):
        '''
        DESP    输出棋盘的备份
        RET     int[][]
        '''
        return [row[:]for row in self.__board]


if __name__ == "__main__":
    gb = board()
    gb.printBoard()
    gb.place((9, 2), (1, 1))
    gb.printBoard()
    gb.place((9, 2), (1, 1))
    gb.printBoard()
    gb.place((9, 2), (1, 1))
