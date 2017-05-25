#!/usr/bin/env python

import glob
import os
import time as ttime
from datetime import datetime

import learners.list as learners
from predict_and_schedule import get_optimal, RunResult, export, load_prices, \
    timedelta, instances_location
import scheduler
from learners.linear import bayesian_regression_all_features_90_days
from learners.svm import  lin_svr_c1e3_all_features_90_days
from learners.ensemble import random_forest_few_features_90_days


def main():
    export_location = "results"

    learner = random_forest_few_features_90_days
    learner_name = "rf_ff_90d"

    dir_instances = "load5"
    today = datetime.strptime("2013-06-20", '%Y-%m-%d').date()
    dir_instances = os.path.join(instances_location, dir_instances)

    instance_file_name = os.path.join(dir_instances, 'day171.txt')
    instance = scheduler.read_instance(instance_file_name)

    datafile = 'data/prices2013.dat'
    prediction_data = load_prices(datafile)

    prediction = learner(today, prediction_data, instance)
    schedule = scheduler.schedule(instance, prediction.prediction_values)
    optimal = get_optimal(today, instance, instance_file_name,
                          prediction.actual_values)
    result = RunResult(prediction, schedule, optimal, today, dir_instances,
                       instance_file_name, learner_name)
    export(result, export_location)


if __name__ == '__main__':
    main()
