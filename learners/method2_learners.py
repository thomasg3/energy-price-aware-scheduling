#!/usr/bin/env python

import core
import ann
import ensemble
import linear
import nearest_neighbors
import svm
from datetime import timedelta
import atexit
import random


basic_features = ['HolidayFlag', 'DayOfWeek', 'PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA', 'SMPEA']
all_features = ['HolidayFlag', 'DayOfWeek', 'WeekOfYear', 'Day', 'Month', 'Year', 'PeriodOfDay',
                'ForecastWindProduction', 'SystemLoadEA', 'SMPEA', 'ORKTemperature', 'ORKWindspeed',
                'CO2Intensity', 'ActualWindProduction', 'SystemLoadEP2']
few_features = ['PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA']
column_predict = 'SMPEP2'

simple_preprocessors = [core.interpolate_none]

model_count_spearman = {}
model_count_spearman_opt = {}
model_count_mae = {}
model_count_mae_opt = {}
model_count_random = {}


def add_to_model_count(model, counter):
    if counter.has_key(model):
        counter[model] += 1
    else:
        counter[model] = 1


def m2_spearman_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    evaluation_day = day - timedelta(days=1)
    results = [(model, model(evaluation_day, prediction_data, instance)) for model in models]
    best = max(results, key=lambda m: m[1].evaluate()['spearman'])
    add_to_model_count(best[0], model_count_spearman)
    return best[0](day, prediction_data, instance)


def m2_spearman_opt_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    evaluation_day = day
    results = [(model, model(evaluation_day, prediction_data, instance)) for model in models]
    best = max(results, key=lambda m: m[1].evaluate()['spearman'])
    add_to_model_count(best[0], model_count_spearman_opt)
    return best[0](day, prediction_data, instance)


def m2_mae_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    evaluation_day = day - timedelta(days=1)
    results = [(model, model(evaluation_day, prediction_data, instance)) for model in models]
    best = max(results, key=lambda m: m[1].evaluate()['mae'])
    add_to_model_count(best[0], model_count_mae)
    return best[0](day, prediction_data, instance)


def m2_mae_opt_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    evaluation_day = day
    results = [(model, model(evaluation_day, prediction_data, instance)) for model in models]
    best = max(results, key=lambda m: m[1].evaluate()['mae'])
    add_to_model_count(best[0], model_count_mae_opt)
    return best[0](day, prediction_data, instance)


def m2_random_all_feat_300_days(day, prediction_data, instance):
    models = [ann.mlp_all_features_300_days,
              ensemble.random_forest_all_features_300_days,
              linear.bayesian_regression_all_features_300_days,
              nearest_neighbors.knn_11nn_distance_all_feat_300_days,
              svm.lin_svr_c1e3_all_features_300_days]
    best = random.choice(models)
    add_to_model_count(best, model_count_random)
    return best(day, prediction_data, instance)


@atexit.register
def print_model_count():
    if len(model_count_spearman.keys()) > 0:
        print "Model distribution for m2 Spearman"
    for model in model_count_spearman.keys():
        print model.__name__, model_count_spearman[model]
    if len(model_count_spearman_opt.keys()) > 0:
        print "Model distribution for m2 Spearman optimal"
    for model in model_count_spearman_opt.keys():
        print model.__name__, model_count_spearman_opt[model]
    if len(model_count_mae.keys()) > 0:
        print "Model distribution for m2 MAE"
    for model in model_count_mae.keys():
        print model.__name__, model_count_mae[model]
    if len(model_count_mae_opt.keys()) > 0:
        print "Model distribution for m2 MAE optimal"
    for model in model_count_mae.keys():
        print model.__name__, model_count_mae_opt[model]
    if len(model_count_random.keys()) > 0:
        print "Model distribution for m2 Random"
    for model in model_count_random.keys():
        print model.__name__, model_count_random[model]
