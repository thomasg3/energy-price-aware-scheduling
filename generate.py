#!/usr/bin/env python

import os
import argparse
import time
import random
import scheduler
from generator.ICONChallengeGenerator import Instance

number_of_loads = 8
days_in_load = 365

time_resolution = 30
number_of_tasks = 25
number_of_machines = 5
number_of_resources = 1

solve_time_threshold = 2  # seconds


def main(random_seed, save_location):
    random.seed(random_seed)
    if not os.path.isdir(save_location):
        os.makedirs(save_location)
    for load in range(1, number_of_loads + 1):
        load_location = os.path.join(save_location, 'load' + str(load))
        if not os.path.isdir(load_location):
            os.makedirs(load_location)
        instances = []
        number_of_time_outs = 14
        time_out = 0
        while len(instances) < days_in_load:
            day = len(instances) + 1
            generator_args = GeneratorArgs()
            generator_args.Nr_of_Machines = number_of_machines
            generator_args.Nr_of_Resources = number_of_resources
            generator_args.Nr_of_Tasks = number_of_tasks
            generator_args.Time_Resolution = time_resolution
            generator_args.seed = random.randint(0, 1000000)

            instance = Instance(generator_args)
            # instance.plot()

            file_name = 'day'
            if day < 9:
                file_name += '00'+str(day)
            elif day < 99:
                file_name += '0'+str(day)
            else:
                file_name += str(day)
            file_name += '.txt'

            file_location = os.path.join(load_location, file_name)
            instance.printInstance(file_location)
            if os.path.isfile(os.path.join(load_location, 'solution.txt')):
                os.remove(os.path.join(load_location, 'solution.txt'))

            start_time = time.time()
            scheduler.schedule(scheduler.read_instance(file_location), range(24 * (60 / time_resolution)))
            run_time = time.time() - start_time
            if run_time < solve_time_threshold:
                instances += [instance]
                print "{0} :: {1:.2f}s".format(file_location, run_time)

            else:
                time_out += 1
                if time_out > number_of_time_outs:
                    raise Exception("Number of timeouts exceeded!!!!")
        print ">>> Time outs: {0}".format(time_out)


class GeneratorArgs:
    def __init__(self):
        self.epsilon = 3
        self.splitStrategy = "point"
        self.maxScaling = 10
        self.minScaling = 1
        self.yOrig = 1000
        self.gamma = 2.0
        self.beta = 0.5
        self.kappa = 0.5
        self.nu = 1.0


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Generate instances")

    parser.add_argument('-d', help='Instances directory', default='instances')
    parser.add_argument('-s', help='random seed', type=int, default=42)

    args = parser.parse_args()

    main(args.s, args.d)
