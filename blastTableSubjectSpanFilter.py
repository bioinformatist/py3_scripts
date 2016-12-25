#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: Python blastTableSubjectSpanFilter.py inputFileName outputFileName threshhold
"""

import sys
from itertools import chain

query_pool = {}


def get_intervals(file):
    """
    Initialize a dictionary of list, with the key contain the ID of queries and the value whose first element is the
    whole line of the file, as the second element are subject locations (tuple type)..
    """
    global query_pool
    with open(file) as f:
        for line in f.readlines():
            line_content = line.split('\t')
            # To make a empty dictionary.
            query_pool.setdefault(line_content[0], [[], []])
            # Push the whole line into list (with "\n").
            query_pool[line_content[0]][0].append(line)
            # Push the location (forced from smaller to larger).
            query_pool[line_content[0]][1].append(
                (int(min(line_content[8], line_content[9])), int(max(line_content[8], line_content[9]))))


def merge_intervals(intervals):
    """
    This function was copied from http://codereview.stackexchange.com/questions/69242/merging-overlapping-intervals
    Thanks to Nic Young, ferada and amon.
    A simple algorithm can be used:
    1. Sort the intervals in increasing order
    2. Push the first interval on the stack
    3. Iterate through intervals and for each one compare current interval
       with the top of the stack and:
       A. If current interval does not overlap, push on to stack
       B. If current interval does overlap, merge both intervals in to one
          and push on to stack
    4. At the end return stack
    """
    sorted_by_left_bound = sorted(intervals, key=lambda tup: tup[0])
    merged = []

    for higher in sorted_by_left_bound:
        if not merged:
            merged.append(higher)
        else:
            lower = merged[-1]
            # To test for intersection between lower and higher:
            # We know via sorting that lower[0] <= higher[0]
            if higher[0] <= lower[1]:
                upper_bound = max(lower[1], higher[1])
                merged[-1] = (lower[0], upper_bound)  # Replaced by merged interval
            else:
                merged.append(higher)
    return merged


def interval_filtering(output_filename, min_distance):
    with open(output_filename, 'w') as f:
        for query_id, v in query_pool.items():
            intervals = merge_intervals(v[1])
            # There may be only one interval for per query after merging, which mean actually one hit in genome.
            # Just abandon them.
            if len(intervals) == 1:
                continue
            # To convert list of tuple into a list.
            interval_pool = list(chain.from_iterable(intervals))
            # To remove the fist and the last elements.
            interval_pool = interval_pool[1:-1]
            interval_differences = []
            # Calculate distance between adjacent interval.
            for former_right_bound, later_left_bound in grouped(interval_pool, 2):
                interval_differences.append(later_left_bound - former_right_bound)
            # if all distance lower than threshold, abandon this query.
            if all(difference < min_distance for difference in interval_differences):
                continue
            f.writelines(merge_intervals(v[0]))


def grouped(iterable, n):
    """
    To recombine an iterable object with certain elements as a group.
    :param iterable: An iterable object
    :param n: Number of elements per group
    :return: A new iterable object, can be used in for loop structure, etc.
    """
    return zip(*[iter(iterable)] * n)


if __name__ == '__main__':
    min_distance = int(sys.argv[3])
    output_filename = sys.argv[2]
    get_intervals(sys.argv[1])
    interval_filtering(output_filename, min_distance)
