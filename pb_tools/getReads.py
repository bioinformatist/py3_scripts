#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def get_reads(path):
    """
    To get reads from bax files, then merge all fasta file which were from one cell to a fa file in working directory.
	To use this script, please activate virtuenv with PacBio's bash5tools.
    """
    cwd = os.getcwd()
    cell_dir_list = os.listdir(path)

    for dir in cell_dir_list:
        if os.path.isdir(os.path.join(cwd, dir)) and dir.startswith("cell"):
            os.chdir(os.path.join(cwd, dir) + os.sep + "Analysis_Results")
            bax_list = os.listdir(path)
            for bax in bax_list:
                os.system('bash5tools.py --outFilePrefix {} --readType unrolled --outType fasta {}'.format(bax, bax))
            os.system('cat *.fasta > ../../{}.fa'.format(dir))
        os.chdir("../..")
        os.system('rm -rf {}'.format(dir))


if __name__ == '__main__':
    get_reads(".")
