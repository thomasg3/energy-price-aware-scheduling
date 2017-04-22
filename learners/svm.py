#!/usr/bin/env python

import core
from sklearn import svm


basic_features = ['HolidayFlag', 'DayOfWeek', 'PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA', 'SMPEA']
all_features = ['HolidayFlag', 'DayOfWeek', 'WeekOfYear', 'Day', 'Month', 'Year', 'PeriodOfDay',
                'ForecastWindProduction', 'SystemLoadEA', 'SMPEA', 'ORKTemperature', 'ORKWindspeed',
                'CO2Intensity', 'ActualWindProduction', 'SystemLoadEP2']
few_features = ['PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA']
column_predict = 'SMPEP2'

simple_preprocessors = [core.interpolate_none]


def lin_svr_c1e3_few_features_30_days(day, prediction_data, instance):
    historic_days = 30
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(few_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_few_feat_30_days', day, instance)
    return predictions


def lin_svr_c1e3_basic_features_30_days(day, prediction_data, instance):
    historic_days = 30
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(basic_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_basic_feat_30_days', day, instance)
    return predictions


def lin_svr_c1e3_all_features_30_days(day, prediction_data, instance):
    historic_days = 30
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(all_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_all_feat_30_days', day, instance)
    return predictions


def lin_svr_c1e3_few_features_90_days(day, prediction_data, instance):
    historic_days = 90
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(few_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_few_feat_90_days', day, instance)
    return predictions


def lin_svr_c1e3_basic_features_90_days(day, prediction_data, instance):
    historic_days = 90
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(basic_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_basic_feat_90_days', day, instance)
    return predictions


def lin_svr_c1e3_all_features_90_days(day, prediction_data, instance):
    historic_days = 90
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(all_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_all_feat_90_days', day, instance)
    return predictions


def lin_svr_c1e3_few_features_300_days(day, prediction_data, instance):
    historic_days = 300
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(few_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_few_feat_300_days', day, instance)
    return predictions


def lin_svr_c1e3_basic_features_300_days(day, prediction_data, instance):
    historic_days = 300
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(basic_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_basic_feat_300_days', day, instance)
    return predictions


def lin_svr_c1e3_all_features_300_days(day, prediction_data, instance):
    historic_days = 300
    clf = svm.LinearSVR(C=1e3, tol=1e-6)
    predictions = core.generic_learner(all_features, column_predict, simple_preprocessors, clf,
                                       day, prediction_data, instance, historic_days)
    core.export(predictions, 'lin_svr_c1e3_all_feat_300_days', day, instance)
    return predictions
