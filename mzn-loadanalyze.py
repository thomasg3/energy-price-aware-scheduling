#!/usr/bin/env python


import sys
import os
import shutil
import argparse
import random
import subprocess
import tempfile
import time
import glob
import datetime

from scripts.checker import *
import scripts.instance2dzn as i2dzn
import scripts.forecast2dzn as f2dzn
import scripts.checker_mzn as chkmzn
from scripts.prices_data import *
from scripts.prices_regress import *
import numpy as np
from sklearn import linear_model


# from http://code.activestate.com/recipes/577932-flatten-arraytuple/
def _qflatten(L, a, I):
    for x in L:
        if isinstance(x, I):
            _qflatten(x, a, I)
        else:
            a(x)


def qflatten(L):
    R = []
    _qflatten(L, R.append, (list, tuple, np.ndarray))
    return np.array(R)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run and check a MZN model in ICON challenge data")
    parser.add_argument("file_instance",
                        help="(can also be a directory to run everything matching 'day*.txt' in the directory)")
    # debugging options:
    parser.add_argument("-p", "--print-pretty", help="pretty print the machines and tasks", action="store_true")
    parser.add_argument("-v", help="verbosity (0,1,2 or 3)", type=int, default=1)
    parser.add_argument("--print-output", help="print the output of minizinc", action="store_true")
    args = parser.parse_args()

    # single or multiple instances
    f_instances = [args.file_instance]
    if os.path.isdir(args.file_instance):
        globpatt = os.path.join(args.file_instance, 'day*.txt')
        f_instances = sorted(glob.glob(globpatt))

    for (i, f) in enumerate(f_instances):
        instance = Instance()
        # read standard instance and load forecast
        instance.read_instance(f)

        # per timeslot, min/max nr tasks running
        load_min = [0 for s in range(0, instance.day.nrperiods)]
        load_max = [0 for s in range(0, instance.day.nrperiods)]

        # print
        print "Load:", f
        for t in instance.day.tasks:
            lateststart = t.let - t.duration
            earliestend = t.est + t.duration
            out = "-" * (t.est)
            if lateststart < earliestend:
                dur = earliestend - lateststart
                out += " " * (lateststart - t.est)
                out += "X" * (dur)
                out += " " * (t.let - (earliestend))
            else:
                out += " " * (t.let - t.est)
            out += "-" * (t.nrperiods - t.let)
            out += " :: Task %i" % t.taskid
            print out
            # catch loads
            for s in range(0, t.nrperiods):
                if t.est <= s and s < t.let:
                    load_max[s] += 1
                    if lateststart <= s and s < earliestend:
                        load_min[s] += 1
        print load_max, " -- load_max"
        print load_min, " -- load_min"
