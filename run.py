#!/usr/bin/env python

import argparse
import time as ttime
from datetime import datetime

import learners.list as learners
from predict_and_schedule import generic_run

import summarize as summarizer
import combine as combiner
from os import listdir

dates = ["2012-12-01", "2013-03-01", "2013-06-01", "2013-09-01"]

def main(arguments):
    total_start_time = ttime.time()
    for ml_name, learner in learners.iterator():
        if not arguments.learner or arguments.learner in ml_name:
            print ">>> " + ml_name
            start_time = ttime.time()
            loads = ["load" + repr(i) for i in range(1, 9)]
            for load in loads:
                load_start = ttime.time()
                print ">>> " + load
                for date in dates:
                    for result in generic_run(load, datetime.strptime(date, '%Y-%m-%d').date(), learner, ml_name):
                        print result.file_name()
                print ">>> {0} took {1} seconds".format(load, ttime.time() - load_start)
            print ">>> Time: {0} seconds".format(ttime.time() - start_time)
    print ">>> Total Run Time: {0} seconds".format(ttime.time() - total_start_time)


def summarize(applied_filter=''):
    summarizer.summarize('results', applied_filter=applied_filter)
    for load in [l for l in listdir('.') if 'load' in l]:
        summarizer.summarize('results', load=load)
    combiner.additional_analysis()
    combiner.main()


def listing():
    for ml_name, _ in learners.iterator():
        print ml_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Run experiments")

    parser.add_argument("-l", "--learner", help="only use one specific learner", default="")
    parser.add_argument("-s", "--summarize", help="summarize in general, per load and combine this summaries", action="store_true")
    parser.add_argument("-f", "--filter", help="filter to apply to summary", default='')
    parser.add_argument("--list", help="list all possible learners", action="store_true")

    args = parser.parse_args()
    if args.summarize:
        summarize(args.filter)
    elif args.list:
        listing()
    else:
        main(args)
