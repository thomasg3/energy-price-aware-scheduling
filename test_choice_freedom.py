#!/usr/bin/env python

import os
import glob
import time
import scheduler
import argparse

periods_in_day = 48

def main(dir_instances):
    if os.path.isdir(dir_instances):
        globpatt = os.path.join(dir_instances, 'day*.txt')
        instances_file_names = sorted(glob.glob(globpatt))
        for instance_file_name in instances_file_names:
            test_one_instance(instance_file_name)



def test_one_instance(instance_file_name):
    costs = []
    monotone_price = generate_price(periods_in_day)
    for price in generate_prices():
        instance = scheduler.read_instance(instance_file_name)
        schedule = scheduler.schedule(instance, price)
        costs += [schedule.cost(monotone_price)]
    print "{0} :: {1}".format(instance_file_name, float(len(set(costs)))/float(len(costs)))


def generate_prices():
    for interval in range(1, periods_in_day+1):
        yield generate_price(interval)

def generate_price(interval):
    prices = range(1,interval+1)
    while len(prices) < periods_in_day:
        prices += reversed(prices)
    return prices[:periods_in_day]


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
