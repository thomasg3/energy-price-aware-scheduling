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
from scripts.checker import *
import scripts.instance2dzn as i2dzn
import scripts.forecast2dzn as f2dzn
import scheduler as scheduler

def run(file_instance, data_forecasts, print_output=False, verbose=0, check_win_hack=True):
    data = i2dzn.read_instance(file_instance)
    if verbose >= 2:
        print "Loaded scheduling instances"

    if verbose >= 1:
        print "Starting scheduler"

    time_step = data['time_step']
    nbMachines = len(data['machines'])
    nbTasks = len(data['tasks'])
    nbRes = data['nr_res']
    m_res = [m['res'] for m in data['machines']]
    j_earl = [j['earl'] for j in data['tasks']]
    j_late = [j['late'] for j in data['tasks']]
    j_dur = [j['dur'] for j in data['tasks']]
    j_power = [j['power'] for j in data['tasks']]
    j_res = [j['usage'] for j in data['tasks']]


    time_start = time.time()
    out = scheduler.schedule(time_step, nbMachines, nbTasks,
        nbRes, m_res, j_earl, j_late, j_dur, j_power, j_res, data_forecasts)
    timing = (time.time() - time_start)

    if print_output or verbose >= 1:
        print "Output: \"\"\""

        print "\"\"\""

    return (timing, out)

def mzn_toInstance(file_instance, out, data_forecasts, data_actual=None, pretty_print=False, verbose=0):
        # ./checker_mzn.py ../smallinstances/demo_01
        instance = Instance()

        # read standard instance and load forecast
        instance.read_instance(file_instance)
        instance.load_forecast(data_forecasts)
        if data_actual:
            instance.load_actual(data_actual)
        # load minizinc solution from 'out'
        chkmzn.read_mznsolution(instance, out)

        if pretty_print or verbose >= 1:
            chkmzn.pretty_print(instance)

        instance.verify()
        errstr = instance.geterrorstring()
        if errstr:
            print "Error: Error trying to verify the instance: '%s'"%(errstr)
            print >> sys.stderr, errstr
        else:
            return instance

        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run and check a MZN model in ICON challenge data")
    parser.add_argument("file_mzn")
    parser.add_argument("file_instance", help="(can also be a directory to run everything matching 'day*.txt' in the directory)")
    parser.add_argument("file_forecast")
    parser.add_argument("--mzn-solver", help="the mzn solver to use (mzn-g12mip or mzn-gecode for example)", default='mzn-g12mip')
    parser.add_argument("--mzn-dir", help="optionally, if the binaries are not on your PATH, set this to the directory of the MiniZinc IDE", default="")
    parser.add_argument("--tmp", help="temp directory (default = automatically generated)")
    # debugging options:
    parser.add_argument("-p", "--print-pretty", help="pretty print the machines and tasks", action="store_true")
    parser.add_argument("-v", help="verbosity (0,1 or 2)", type=int, default=0)
    parser.add_argument("--print-output", help="print the output of minizinc", action="store_true")
    parser.add_argument("--tmp-keep", help="keep created temp subdir", action="store_true")
    args = parser.parse_args()

    # if you want to hardcode the MiniZincIDE path for the binaries, here is a resonable place to do that
    #args.mzn_dir = "/home/tias/local/src/MiniZincIDE-2.0.13-bundle-linux-x86_64"

    tmpdir = ""
    if args.tmp:
        tmpdir = args.tmp
        os.mkdir(args.tmp)
    else:
        tmpdir = tempfile.mkdtemp()

    # single or multiple instances
    f_instances = [args.file_instance]
    if os.path.isdir(args.file_instance):
        globpatt = os.path.join(args.file_instance, 'day*.txt')
        f_instances = sorted(glob.glob(globpatt))

    # prep data_forecasts (same for all instances here)
    data_forecasts = f2dzn.read_forecast(args.file_forecast)
    timestep = i2dzn.read_instance(f_instances[0])['time_step']
    data_forecasts = f2dzn.rescale(timestep, data_forecasts)

    # the actual stuff
    for (i,f) in enumerate(f_instances):
        (timing, out) = run(f, data_forecasts,
                                print_output=args.print_output,
                                verbose=args.v)
#        instance = mzn_toInstance(f, out, data_forecasts,
#                                  pretty_print=args.print_pretty,
#                                  verbose=args.v)
        # csv print:
#        chkmzn.print_instance_csv(f, args.file_forecast, instance, timing=timing, header=(i==0))

    if not args.tmp_keep:
        shutil.rmtree(tmpdir)
