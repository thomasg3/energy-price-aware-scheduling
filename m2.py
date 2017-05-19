#!/usr/bin/env python

import time as ttime
from datetime import datetime

import learners.list as learners
from predict_and_schedule import generic_run

dates = ["2013-01-01"]


def main():
    total_start_time = ttime.time()
    for ml_name, learner in learners.method2():
        print ">>> " + ml_name
        start_time = ttime.time()
        loads = ["load1", "load2"]+["load" + repr(i) for i in range(4, 9)]
        for load in loads:
            load_start = ttime.time()
            print ">>> " + load
            for date in dates:
                for result in generic_run(load, datetime.strptime(date,
                                                                  '%Y-%m-%d').date(),
                                          learner, ml_name):
                    print result.file_name()
            print ">>> {0} took {1} seconds".format(load,
                                                    ttime.time() - load_start)
        print ">>> Time: {0} seconds".format(ttime.time() - start_time)
    print ">>> Total Run Time: {0} seconds".format(
        ttime.time() - total_start_time)


if __name__ == '__main__':
    main()
