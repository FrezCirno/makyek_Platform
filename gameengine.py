#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''挑夹棋游戏主体'''

__author__ = 'tzx'

import gameboard
import selectmenu
from Players import player, ai
import yourAI


def startengine():
    size = 12
    playerlist = {'程序AI': ai, '我的AI': yourAI.ai,
                  '自己': player}
    gb = gameboard.board()
    player1 = selectmenu.menu2(playerlist, title='选择Player1')(1, size)
    player2 = selectmenu.menu2(playerlist, title='选择Player2')(2, size)
    loop(gb, player1, player2)


def loop(gb, pl1, pl2):
    '''游戏主循环'''
    printboard = 1
    players = {1: pl1.__author__, 2: pl2.__author__}  # 记录双方id

    check = 0
    while not check:
        # 当前是谁的回合
        whoseTurn = gb.whoseTurn()
        print('Turn #%d: Player %d: %s' %
              (gb.gettimes(), whoseTurn, players[whoseTurn]))
        if printboard:
            gb.printBoard(' ox')

        if whoseTurn == 1:  # 玩家1
            pos, d = pl1.turn(gb.outputBoard())
        else:  # 玩家2
            pos, d = pl2.turn(gb.outputBoard())

        # 尝试落子
        res = gb.place(pos, d)

        # 输出回显
        if 1:
            print('%s want to move %s to %s' %
                  (players[whoseTurn], str(pos), str(pos+d)))
            if res:
                print('Success')
            else:
                print('Failed')

        # 检查游戏是否结束
        check = gb.check()

    print('#%s win!' % players[check])


if __name__ == "__main__":
    startengine()
