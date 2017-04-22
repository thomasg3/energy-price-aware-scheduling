#!/usr/bin/env python

import sys
import os
import glob
import time as ttime
import cPickle as pickle
import csv
from collections import OrderedDict
from scripts.prices_data import *
from scripts.prices_regress import *
import scheduler
from learners.core import Prediction
from learners.unused import simple_learner


instances_location = 'instances'


def generic_run(dir_instances, start_date, learner, learner_name, export_location="results"):
    dir_instances = os.path.join(instances_location, dir_instances)
    if os.path.isdir(dir_instances):
        globpatt = os.path.join(dir_instances, 'day*.txt')
        instances_file_names = sorted(glob.glob(globpatt))
        instances = [scheduler.read_instance(instance) for instance in instances_file_names]
    else:
        raise RuntimeError("Instances should be a directory of instances")

    datafile = 'data/prices2013.dat'
    prediction_data = load_prices(datafile)

    for i, instance in enumerate(instances):
        today = start_date + timedelta(i)
        prediction = learner(today, prediction_data, instance)
        schedule = scheduler.schedule(instance, prediction.prediction_values)
        optimal = get_optimal(today, instance, instances_file_names[i] ,prediction.actual_values)
        result = RunResult(prediction, schedule, optimal, today, dir_instances, instances_file_names[i], learner_name)
        export(result, export_location)
        yield result


def export(result, location):
    export_run_location = os.path.join(location, "runs")
    if not os.path.isdir(export_run_location):
        os.makedirs(export_run_location)
    file_location = os.path.join(export_run_location, result.file_name(extension="csv"))
    with open(file_location, 'w') as export_file:
        data = result.dictionary()
        fields = data.keys()
        writer = csv.DictWriter(export_file, fieldnames=fields, dialect='excel')
        writer.writeheader()
        writer.writerow(data)
    pickle_location = os.path.join(export_run_location, result.file_name(extension="p"))
    with open(pickle_location, 'w') as pickle_file:
        pickle.dump(result, pickle_file)


class RunResult:
    def __init__(self, prediction, forecasted_schedule, optimal_schedule, date, load, instance_day, learner_name):
        self.prediction = prediction
        self.forecasted_schedule = forecasted_schedule
        self.optimal_schedule = optimal_schedule
        self.date = date
        self.load = load.split("/")[-1]
        self.instance_day = instance_day.split("/")[-1].split('.')[0]
        self.learner_name = learner_name

    def file_name(self, extension=""):
        base_file_name = "{0}-{1}-{2}-{3}".format(self.date, self.load, self.instance_day, self.learner_name)
        if extension:
            base_file_name += ".{0}".format(extension)
        return base_file_name

    def dictionary(self):
        dictionary = OrderedDict()
        dictionary['ml_name'] = self.learner_name
        dictionary['forecasted_price'] = self.forecasted_schedule.forecasted_price
        dictionary['actual_price'] = self.forecasted_schedule.cost(self.prediction.actual_values)
        dictionary['optimal_price'] = self.optimal_schedule.forecasted_price
        dictionary['regret'] = dictionary['actual_price'] - dictionary['optimal_price']
        for key, value in self.prediction.evaluate().iteritems():
            dictionary[key] = value
        return dictionary


def get_optimal(date, instance, instance_file_name, prices):
    if not os.path.isdir('tmp'):
        os.makedirs('tmp')
    optimal_file_name = os.path.join('tmp', date.isoformat()+clean_instance_file_name(instance_file_name)+'_optimal.p')
    if os.path.isfile(optimal_file_name):
        with open(optimal_file_name, 'r') as f:
            return pickle.load(f)
    else:
        optimal_schedule = scheduler.schedule(instance, prices)
        with open(optimal_file_name, 'w') as f:
            pickle.dump(optimal_schedule, f)
        return optimal_schedule


# instance_file_name is of form loadX/dayXX.txt
def clean_instance_file_name(instance_file_name):
    return instance_file_name.split('.')[0].replace('/', '-')


if __name__ == "__main__":
    start_time = ttime.time()
    loads = ["load" + repr(i) for i in range(1, 9)]
    for load in loads:
        load_start = ttime.time()
        print ">>> " + load
        for result in generic_run(load, datetime.strptime("2013-03-01", '%Y-%m-%d').date(), simple_learner, "test"):
            print result.file_name()
        print ">>> {0} took {1} seconds".format(load, ttime.time() - load_start)
    print ">>> Time: {0} seconds".format(ttime.time() - start_time)
