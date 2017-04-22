#!/usr/bin/env python

import os
import glob
import time
import scheduler
import argparse


def main(dir_instances):
    prices = range(48)
    costs = []
    run_times = []
    if os.path.isdir(dir_instances):
        globpatt = os.path.join(dir_instances, 'day*.txt')
        instances_file_names = sorted(glob.glob(globpatt))
        instances = [scheduler.read_instance(instance) for instance in instances_file_names]
        for instance in instances:
            start_time = time.time()
            schedule = scheduler.schedule(instance, prices)
            run_times +=  [time.time() - start_time]
            cost = schedule.cost(prices)
            if cost in costs:
                print '>>> Error same cost detected, could be duplicate schedule'
            costs += [cost]
    print "Average run time per day is {0}".format(sum(run_times)/float(len(run_times)))




if __name__ == '__main__':
    parser = argparse.ArgumentParser("Test all instances")

    parser.add_argument('-d', help='Instances directory', default='instances')

    args = parser.parse_args()

    if os.path.isdir(args.d):
        globpatt = os.path.join(args.d, 'load*')
        load_dirs = sorted(glob.glob(globpatt))
        for load in load_dirs:
            print load
            main(load)
