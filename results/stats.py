#!/usr/bin/python

# For running stats on the example result data
# usage: cat endroll.txt | python stats.py


import fileinput
from sets import Set

values = []

def loadData():
    """
    This loads data from stdin or from a file if one is specified into an array to be handled in memory
    """
    for line in fileinput.input():
        values.append(int(line))

    fileinput.close()


def uniqCount():
    uniq = Set(values)
    result = {}
    for item in uniq:
        result[item] = values.count(item) / float(len(values))

    print result
    return result

loadData()
uniqCount()

