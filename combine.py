#!/usr/bin/env python

import csv
from os import listdir, remove
from os.path import isfile, join
from summarize import read_all


result_location = 'results'
combination_file_name = 'combination.csv'


def main():
    if isfile(join(result_location, combination_file_name)):
        remove(join(result_location, combination_file_name))
    files = [f for f in listdir(result_location) if isfile(join(result_location, f))]
    to_combine = []
    if 'summary.csv' in files:
        to_combine.append('summary.csv')
    loads = [l for l in files if 'load' in l and 'spearman' not in l]
    loads = sorted(loads)
    to_combine = to_combine + loads
    with open(join(result_location, combination_file_name), 'a') as combi:
        for load in to_combine:
            with open(join(result_location, load), 'r') as f:
                if 'load' in load:
                    combi.write(load+'\n')
                combi.write(f.read())
            additional_analysis(load)


def additional_analysis(file_name='summary.csv'):
    file_location = join(result_location, file_name)
    spearman_store = {}
    best_regret_store = {}
    best_regret_ml_store = {}
    for line in read_all(file_location):
        for key in line.keys():
            if '_rank' not in key and 'price' not in key and key != 'ml_name':
                if key not in spearman_store:
                    spearman_store[key] = []
                spearman_store[key].append(line[key+'_rank'])
                if eval(line[key+'_rank']) == 1:
                    best_regret_store[key] = eval(line['regret'])
                    best_regret_ml_store[key] = line['ml_name']
    for metric, rank_list in spearman_store.iteritems():
        spearman_store[metric] = [eval(r) for r in rank_list]
    for metric in spearman_store.keys():
        if metric != 'regret':
            n = len(spearman_store[metric])
            spearman_store[metric] = sum([(spearman_store['regret'][i] - spearman_store[metric][i]) ** 2 for i in range(n)])
            n = float(n)
            spearman_store[metric] = 1 - ((6 * spearman_store[metric]) / (n * (n ** 2 - 1)))
    data_to_store = []
    for metric in spearman_store.keys():
        if metric != 'regret':
            data_to_store.append({
                'metric': metric,
                'spearman': spearman_store[metric],
                'best_regret': best_regret_store[metric],
                'best_regret_ml_name': best_regret_ml_store[metric],
                'n': int(n),
            })
    data_to_store = sorted(data_to_store, key=lambda d: -d['spearman'])
    name = ".".join(file_name.split('.')[:-1])
    with open(join(result_location, name+'_spearman.csv'), 'w') as f:
        fields = ['metric', 'spearman', 'best_regret', 'best_regret_ml_name', 'n']
        writer = csv.DictWriter(f, fieldnames=fields, dialect='excel')
        writer.writeheader()
        writer.writerows(data_to_store)

if __name__ == '__main__':
    main()
