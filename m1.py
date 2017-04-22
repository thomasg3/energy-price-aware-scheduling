#!/usr/bin/env python

import os
import learners.method1_validation as m1
import scripts.prices_data as prices_data
import scheduler
from datetime import datetime, timedelta
import numpy as np
import time
import csv

number_of_days_to_test = 30
day_step = 10


def main():
    # test_models_and_save_results(m1.iterate_random_forest_m1(), 'random_forest.csv')
    test_models_and_save_results(m1.iterate_mlp_m1(), 'mlp.csv')


def test_models_and_save_results(models, file_name):
    price_data_location = 'data/prices2013.dat'
    price_data = prices_data.load_prices(price_data_location)

    instance = scheduler.read_instance('instances/load1/day01.txt')

    days = [datetime.strptime('2013-01-01', '%Y-%m-%d').date() + timedelta(days=day_step * i) for i in
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
    main()
