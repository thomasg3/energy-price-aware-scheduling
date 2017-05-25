#!/usr/bin/env python

import os
import argparse
import learners.method1_validation as m1
import scripts.prices_data as prices_data
import scheduler
from datetime import datetime, timedelta
import numpy as np
import time
import csv


def main(model, days, day_step, start_day, random_forest_args):
    if 'mlp' in model or not model:
        test_models_and_save_results(m1.iterate_mlp_m1(), 'mlp.csv', days, day_step, start_day)
    if 'rf' in model or not model:
        test_models_and_save_results(m1.iterate_random_forest_m1(random_forest_args), 'random_forest.csv', days, day_step, start_day)


def test_models_and_save_results(models, file_name, number_of_days_to_test, day_step, start_day):
    price_data_location = 'data/prices2013.dat'
    price_data = prices_data.load_prices(price_data_location)

    instance = scheduler.read_instance('instances/load1/day001.txt')

    days = [datetime.strptime(start_day, '%Y-%m-%d').date() + timedelta(days=day_step * i) for i in
            range(number_of_days_to_test)]

    results = []

    for name, test in models:
        spearman_result = []
        mae_result = []
        print name
        start_time = time.time()
        for day in days:
            prediction = test(day, price_data, instance)
            evaluation = prediction.evaluate()
            spearman_result.append(evaluation['spearman'])
            mae_result.append(evaluation['mae'])
        run_time = time.time() - start_time
        results.append({
            'name': name,
            'run_time': run_time,
            'spearman_avg': np.mean(spearman_result),
            'spearman_var': np.var(spearman_result),
            'spearman_med': np.median(spearman_result),
            'mae_avg': np.mean(mae_result),
            'mae_var': np.var(mae_result),
            'mae_med': np.median(mae_result),
        })

    file_location = os.path.join('results', 'm1')
    if not os.path.isdir(file_location):
        os.makedirs(file_location)
    file_location = os.path.join(file_location, file_name)

    with open(file_location, 'w') as export_file:
        fields = ['name', 'run_time', 'spearman_avg', 'spearman_var', 'spearman_med', 'mae_avg', 'mae_var', 'mae_med']
        writer = csv.DictWriter(export_file, fieldnames=fields, dialect='excel')
        writer.writeheader()
        writer.writerows(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("M1 Validation method")

    parser.add_argument('-m', help="Models to test", default="")
    parser.add_argument('-d', help="Number of days to test the models on", default=365)
    parser.add_argument('-s', help="Day Step to take between two test days", default=1)
    parser.add_argument('--start', help="Start day", default='2013-01-01')
    parser.add_argument('--rf', help="Random Forest arguments", default="mse")

    args = parser.parse_args()

    main(args.m, args.d, args.s, args.start, args.rf)
