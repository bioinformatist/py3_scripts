#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yu Sun'

import os
import re
import shutil


def xml_copy(path):
    pattern = re.compile("cell\d+")
    dir_list = os.listdir(path)
    for dir in dir_list:
        if pattern.match(dir):
            os.chdir(dir + "/Analysis_Results")
            print(os.listdir(".")[0].split(".")[0])
            print("../../meta/" + os.listdir(".")[0].split(".")[0] + ".metadata.xml")
            shutil.copy("../../meta/" + os.listdir(".")[0].split(".")[0] + ".metadata.xml", "..")
            os.chdir("../..")


if __name__ == '__main__':
    xml_copy(".")
