#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yu Sun'

import os
import re
import shutil


def xml_copy(path):
    '''
    To get xml file names and copy them into proper directories separately.
    '''
    cell_name_pattern = re.compile("cell\d+")
    cell_dir_list = os.listdir(path)
    for dir in cell_dir_list:
        if cell_name_pattern.match(dir):
            try:
                os.chdir(dir + os.sep + "Analysis_Results")
            except:
                os.chdir(dir)
                os.mkdir("Analysis_Results")
                h5_file_list = os.listdir(".")
                for h5_file in h5_file_list:
                    if h5_file.endswith(".bax.h5"):
                        print("Performing on file:", h5_file, "...")
                        shutil.move(h5_file, "Analysis_Results")
                os.chdir("Analysis_Results")
            shutil.copy("../../meta/" + os.listdir(".")[0].split(".")[0] + ".metadata.xml", "..")
            os.chdir("../..")


if __name__ == '__main__':
    xml_copy(".")
