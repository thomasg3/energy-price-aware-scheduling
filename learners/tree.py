#!/usr/bin/env python

import core
from sklearn import tree


basic_features = ['HolidayFlag', 'DayOfWeek', 'PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA', 'SMPEA']
all_features = ['HolidayFlag', 'DayOfWeek', 'WeekOfYear', 'Day', 'Month', 'Year', 'PeriodOfDay',
                'ForecastWindProduction', 'SystemLoadEA', 'SMPEA', 'ORKTemperature', 'ORKWindspeed',
                'CO2Intensity', 'ActualWindProduction', 'SystemLoadEP2']
few_features = ['PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA']
column_predict = 'SMPEP2'

simple_preprocessors = [core.interpolate_none]


def dtr_mse_depth_10_30_days(day, prediction_data, instance):
    historic_days = 30
    clf = tree.DecisionTreeRegressor(max_depth=10)
    predictions = core.generic_learner(basic_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'dtr_mse_depth_10_30_days', day, instance)
    return predictions


def dtr_mse_depth_10_few_feat_30_days(day, prediction_data, instance):
    historic_days = 30
    clf = tree.DecisionTreeRegressor(max_depth=10)
    predictions = core.generic_learner(few_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'dtr_mse_depth_10_few_feat_30_days', day, instance)
    return predictions
