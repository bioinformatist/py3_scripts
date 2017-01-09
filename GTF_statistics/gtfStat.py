#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
To generate plain-text file containing statistic results of GTF file, which can be used as data for graphics in R, etc.

Usage: Python gtfStat.py GTFfile
"""

import sys

import GTF


def count_lowlevel_in_hightlevel(filename, low_level_name, high_level_name):
    """
    To count how many sub-features in a highlevel feature.
    :param filename: File used to be processed.
    :param low_level_name: Feature names in GTF file. Such as "exon", "transcript".
    :param high_level_name: Feature names in GTF file. Such as "exon", "transcript", "gene".
    :return: No return, but output to file directly.
    """
    occurrence = 0
    with open('{} number in each {}'.format(low_level_name, high_level_name), 'w') as f:
        for idx, item_with_bool in enumerate(lookahead(GTF.lines(filename))):
            if item_with_bool[0]['feature'] == high_level_name:
                if idx != 0 and idx != 1:
                    f.write(str(occurrence) + '\n')
                occurrence = 0
            elif item_with_bool[0]['feature'] == low_level_name:
                occurrence += 1
            elif item_with_bool[1] == False:
                f.write(str(occurrence) + '\n')
            else:
                continue


def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    Thanks to Ferdinand Beyer and others' answer on http://stackoverflow.com/questions/1630320/what-is-the-
    pythonic-way-to-detect-the-last-element-in-a-python-for-loop
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val
    # Report the last value.
    yield last, False


def processing_count(filenames):
    count_lowlevel_in_hightlevel(filenames, 'transcript', 'gene')
    count_lowlevel_in_hightlevel(filenames, 'exon', 'transcript')


if __name__ == '__main__':
    # Below is a demo for using function lookahead():
    # for i, has_more in lookahead(range(3)):
    #     print(i, has_more)
    whole_gtf = GTF.dataframe(sys.argv[1])
    processing_count(sys.argv[1])
    whole_gtf['length'] = whole_gtf['end'].astype('int') - whole_gtf['start'].astype('int') + 1
    whole_gtf = whole_gtf.loc[:, ['gene_biotype', 'feature', 'length']]
    whole_gtf.to_csv("whole_gtf", sep='\t', index=False)
    # Below is a example for using ggplot package in Python:
    # p = ggplot(aes(x='length'), data=a) + geom_histogram() + facet_grid(x='gene_biotype', y='feature') \
    # + xlim(0,50000) + scale_y_log(10) + ylim(1, 1e3)
    # ggplot.save(p, "fuck.tiff", width=55, height=50, dpi=300)
    biotype_count_as_features = whole_gtf.groupby(['gene_biotype', 'feature']).size()
    biotype_count_as_features.to_csv("biotype_count_as_features", sep='\t')
