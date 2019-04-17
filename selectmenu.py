#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''通用选择列表模块'''
__author__ = 'tzx'


def menu(slist, start=0, default=None, sep='/', title=None):
    '''打印一个选择列表并返回一个int序号'''
    if default == None:
        default = start
    if title != None:
        print(title)
    first = True
    for i, s in enumerate(slist, start):
        print('>>>%d.%s' % (i, s))
        if i == default:
            si = '['+str(i)+']'
        else:
            si = str(i)
        if first:
            ss = si
            first = False
        else:
            ss += sep+si
    while True:
        key = input('请输入%s: ' % ss)
        if key == '':
            return default
        if key.isdigit() and start <= int(key) < start+len(slist):
            break
        else:
            print("输入有误，请重新输入")
    return int(key)


def menu2(sdict, start=0, default=None, sep='/', title=None):
    '''打印一个选择列表
    sdict={'提示信息1':执行函数1,'提示信息2':执行函数2,...}
    start=选择列表首项序号
    default=默认选择项key,默认为第一项
    '''
    if title != None:
        print(title)
    str_dict = dict(enumerate(sdict.keys(), start))
    if default == None or not default in sdict.keys():
        default = str_dict[start]
    first = True
    for index, string in str_dict.items():
        print('>>>%d.%s' % (index, string))
        if string == default:
            si = '['+str(index)+']'
        else:
            si = str(index)
        if first:
            ss = si
            first = False
        else:
            ss += sep+si

    while True:
        key = input('请输入%s: ' % (ss))
        if key == '' and callable(sdict[default]):
            return sdict[default]
        elif key.isdigit() and start <= int(key) < start+len(sdict) and callable(sdict[str_dict[int(key)]]):
            return sdict[str_dict[int(key)]]
        else:
            print("输入有误，请重新输入")
