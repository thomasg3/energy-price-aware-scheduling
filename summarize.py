#!/usr/bin/env python

import os
import csv
import argparse
from itertools import groupby
from collections import OrderedDict


# gather all data for a specific query
# for specific load / day / date / leaner
# ./summarize.py -l load
#                | -i instance
#                | -d date

def retrieve_data(location, load, instance, year, month, day, applied_filter=''):
    run_location = os.path.join(location, "runs")

    def includes(f):
        result = True
        result &= f.split('.')[-1] == 'csv'
        chunks = f.split('-')
        if year:
            result &= chunks[0] == year
        if month:
            result &= chunks[1] == month
        if day:
            result &= chunks[2] == day
        if load:
            result &= chunks[3] == load
            if instance:
                result &= chunks[4] == instance
        return result

    if os.path.isdir(run_location):
        result_files = sorted(filter(includes, os.listdir(run_location)))
        return [read_one(os.path.join(run_location, file_name)) for file_name in result_files if applied_filter in file_name]
    else:
        return []


def read_one(file_name):
    with open(file_name, 'r') as f:
        reader = csv.DictReader(f, dialect='excel')
        for row in reader:
            return row


def read_all(file_name):
    with open(file_name, 'r') as f:
        reader = csv.DictReader(f, dialect='excel')
        for row in reader:
            yield row


def aggregate(result_set):
    # sort result_set on ml_name so the groupby will work correctly
    result_set = sorted(result_set, key=lambda r: r['ml_name'])
    aggregates = []
    for learner_name, group in groupby(result_set, lambda r: r['ml_name']):
        aggregate = OrderedDict()
        aggregate['ml_name'] = learner_name
        aggregate['forecasted_price'] = []
        aggregate['actual_price'] = []
        aggregate['optimal_price'] = []
        aggregate['regret_rank'] = [0]
        aggregate['regret'] = []
        for r in group:
            for key, value in r.items():
                if key != 'ml_name':
                    if key in aggregate:
                        aggregate[key].append(value)
                    else:
                        aggregate[key + '_rank'] = [0]
                        aggregate[key] = [value]
        aggregates.append(combine(aggregate))
    if aggregates:
        ranks = [r for r in aggregates[0].keys() if '_rank' in str(r)]
        for rank in ranks:
            metric = '_'.join(rank.split('_')[:-1])
            sorted_aggregates = sort_aggregates(aggregates, metric)
            for i in range(len(sorted_aggregates)):
                sorted_aggregates[i][rank] = i + 1
    return aggregates


def sort_aggregates(aggregates, metric):
    if 'spearman' in metric:
        return list(reversed(sorted(aggregates, key=lambda a: a[metric])))
    if metric == 'regret':
        return sorted(aggregates, key=lambda a: a[metric])
    else:
        return sorted(aggregates, key=lambda a: abs(a[metric]))


def combine(aggregate):
    result = OrderedDict()
    result['ml_name'] = aggregate['ml_name']
    for key, value_list in aggregate.items():
        if key != 'ml_name':
            result[key] = sum([float(v) for v in value_list]) / len(value_list)
    return result


def export(aggregates, location, load, instance, year, month, day):
    file_name = [load, instance, year, month, day]
    file_name = [part for part in file_name if part]
    file_name = '-'.join(file_name)
    file_name = 'summary' if not file_name else file_name
    file_name += '.csv'
    file_location = os.path.join(location, file_name)
    aggregates = sorted(aggregates, key=lambda a: a['regret_rank'])
    with open(file_location, 'w') as export_file:
        fields = aggregates[0].keys()
        writer = csv.DictWriter(export_file, fieldnames=fields, dialect='excel')
        writer.writeheader()
        for aggregate in aggregates:
            writer.writerow(aggregate)


def summarize(location, load='', instance='', year='', month='', day='', applied_filter=''):
    results = retrieve_data(location, load, instance, year, month, day, applied_filter)
    if results:
        aggregates = aggregate(results)
        export(aggregates, location, load, instance, year, month, day)


if __name__ == '__main__':
    result_location = "results"
    parser = argparse.ArgumentParser("Summarize experiment measure points")
    parser.add_argument("--load", help="filter on one specific load", default="")
    parser.add_argument("--instance",
                        help="filter on one specific instance in the load (only has effect when also a load is specified)",
                        default="")
    parser.add_argument("--year", help="filter on one specific year", default="")
    parser.add_argument("--month", help="filter on one specific month (ex. 03 or 12)", default="")
    parser.add_argument("--day", help="filter on one specific day (ex. 03 or 12)", default="")
    parser.add_argument("--filter", help="filter the results based on filename", default="")
    args = parser.parse_args()

    summarize(result_location, load=args.load, instance=args.instance, year=args.year, month=args.month, day=args.day)
