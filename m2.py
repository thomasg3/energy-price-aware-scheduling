#!/usr/bin/env python

from datetime import datetime
import os
import glob
import time as ttime
from scripts.prices_data import *
from scripts.prices_regress import *
import scheduler

import learners.list as learners

dates = ["2013-01-01"]


def main():
    total_start_time = ttime.time()
    for ml_name, learner in learners.method2():
        print ">>> " + ml_name
        start_time = ttime.time()
        loads = ["load1", "load2"] + ["load" + repr(i) for i in range(4, 9)]
        for load in loads:
            load_start = ttime.time()
            print ">>> " + load
            for date in dates:
                generic_run(load, datetime.strptime(date, '%Y-%m-%d').date(),
                            learner, ml_name)
            print ">>> {0} took {1} seconds".format(load,
                                                    ttime.time() - load_start)
        print ">>> Time: {0} seconds".format(ttime.time() - start_time)
    print ">>> Total Run Time: {0} seconds".format(
        ttime.time() - total_start_time)


instances_location = 'instances'


def generic_run(dir_instances, start_date, learner, learner_name,
                export_location="results"):
    dir_instances = os.path.join(instances_location, dir_instances)
    if os.path.isdir(dir_instances):
        globpatt = os.path.join(dir_instances, 'day*.txt')
        instances_file_names = sorted(glob.glob(globpatt))
        instances = [scheduler.read_instance(instance) for instance in
                     instances_file_names]
    else:
        raise RuntimeError("Instances should be a directory of instances")

    datafile = 'data/prices2013.dat'
    prediction_data = load_prices(datafile)

    for i, instance in enumerate(instances):
        today = start_date + timedelta(i)
        learner(today, prediction_data, instance)


if __name__ == '__main__':
    main()
