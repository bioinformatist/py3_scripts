#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yu Sun'

import glob
import os
import re


def get_all_code(suffix):
    for filename in glob.iglob("." + os.sep + '**' + os.sep + '*.' + suffix, recursive=True):
        with open("all_code.txt", 'a', encoding='utf-8') as f1:
            f1.writelines("File name:" + filename + "\n")
            # For some comments are in Chinese, using ISO-8859-1
            with open(filename, encoding='ISO-8859-1') as f:
                for line in f.readlines():
                    if re.match(r'^\s*$', line):
                        pass
                    else:
                        # To remove comments
                        line_no_comments = str(line).split("#")[0]
                        f1.writelines(line_no_comments)


if __name__ == '__main__':
    get_all_code("pl")
