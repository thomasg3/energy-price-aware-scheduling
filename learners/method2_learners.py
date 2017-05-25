#!/usr/bin/env python

import os
import csv
import core
import ann
import ensemble
import linear
import nearest_neighbors
import svm
from datetime import timedelta
import atexit
import random
import cPickle as pickle

basic_features = ['HolidayFlag', 'DayOfWeek', 'PeriodOfDay',
                  'ForecastWindProduction', 'SystemLoadEA', 'SMPEA']
all_features = ['HolidayFlag', 'DayOfWeek', 'WeekOfYear', 'Day', 'Month',
                'Year', 'PeriodOfDay',
                'ForecastWindProduction', 'SystemLoadEA', 'SMPEA',
                'ORKTemperature', 'ORKWindspeed',
                'CO2Intensity', 'ActualWindProduction', 'SystemLoadEP2']
few_features = ['PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA']
column_predict = 'SMPEP2'

simple_preprocessors = [core.interpolate_none]


def add_to_model_count(method, model):
    m2_results = os.path.join("results", "m2")
    file_location = os.path.join(m2_results, "model_count.p")
    if not os.path.isfile(file_location):
        model_count = {}
    else:
        with open(file_location, 'r') as f:
            model_count = pickle.load(f)
    model = model.__name__
    if method not in model_count.keys():
        model_count[method] = {'total': 0}
    if model_count[method].has_key(model):
        model_count[method][model] += 1
    else:
        model_count[method][model] = 1
    model_count[method]['total'] += 1
    with open(file_location, 'w') as f:
        pickle.dump(model_count, f)


def m2_spearman_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    evaluation_day = day - timedelta(days=1)
    results = [(model, model(evaluation_day, prediction_data, instance)) for
               model in models]
    best = max(results, key=lambda m: m[1].evaluate()['spearman'])
    add_to_model_count("spearman", best[0])
    return best[0](day, prediction_data, instance)


def m2_spearman_o3_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    evaluation_day = day - timedelta(days=1)
    results = [(model, model(evaluation_day, prediction_data, instance)) for
               model in models]
    best = max(results, key=lambda m: m[1].evaluate()['w_spearman_o3'])
    add_to_model_count("w_spearman_o3", best[0])
    return best[0](day, prediction_data, instance)


def m2_spearman_max_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    evaluation_day = day - timedelta(days=1)
    results = [(model, model(evaluation_day, prediction_data, instance)) for
               model in models]
    best = max(results, key=lambda m: m[1].evaluate()['w_spearman_max'])
    add_to_model_count("w_spearman_max", best[0])
    return best[0](day, prediction_data, instance)


def m2_mae_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    evaluation_day = day - timedelta(days=1)
    results = [(model, model(evaluation_day, prediction_data, instance)) for
               model in models]
    best = max(results, key=lambda m: m[1].evaluate()['mae'])
    add_to_model_count("mae", best[0])
    return best[0](day, prediction_data, instance)


def m2_random_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    best = random.choice(models)
    add_to_model_count("random", best)
    return best(day, prediction_data, instance)


@atexit.register
def save_model_count():
    m2_results = os.path.join("results", "m2")
    model_count_file = os.path.join(m2_results, "model_count.p")
    if os.path.isfile(model_count_file):
        with open(model_count_file, 'r') as f:
            model_count = pickle.load(f)
        data = []
        for method, counts in model_count.iteritems():
            result = {}
            for key, count in counts.iteritems():
                if key == 'total':
                    result['total'] = count
                else:
                    result[key] = count
            result['name'] = method
            data.append(result)

        if not os.path.isdir(m2_results):
            os.makedirs(m2_results)
        file_location = os.path.join(m2_results, "model_choice.csv")
        models = [ann.mlp_all_features_300_days,
                  ensemble.random_forest_all_features_300_days,
                  linear.bayesian_regression_all_features_300_days,
                  nearest_neighbors.knn_11nn_distance_all_feat_300_days,
                  svm.lin_svr_c1e3_all_features_300_days]
        fields = ['name', 'total'] + [model.__name__ for model in models]
        with open(file_location, 'w') as export_file:
            writer = csv.DictWriter(export_file, fieldnames=fields, dialect='excel')
            writer.writeheader()
            for d in data:
                writer.writerow(d)
