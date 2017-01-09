#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

name_dict = {}


def get_name_dict(name_list):
    '''
    To get name table from a csv file.
    '''
    global name_dict
    with open(name_list) as f:
        for line in f.readlines():
            record = line.split(sep=",")
            name_dict[record[1]] = record[0]


def change_names(path):
    '''
    To change file name.
    '''
    file_list = os.listdir(path)
    for file in file_list:
        cell_name = str(file.split(sep=".")[0])
        try:
            os.rename(cell_name + ".fasta", "ccs" + name_dict[cell_name] + ".fa")
        except:
            continue


if __name__ == '__main__':
    get_name_dict(sys.argv[1])
    change_names(".")
