#!/usr/bin/env python

import os
import csv
from collections import OrderedDict

from scripts.prices_data import *
from scripts.prices_regress import *


def generic_learner(column_features, column_predict, preprocessors, model, day, complete_data, instance, historic_days):
    preprocessors = [interpret_column_values] + preprocessors

    data_previous_historic_days = get_data_prevdays(complete_data, day, timedelta(historic_days))
    x_train, y_train = features_and_preprocess(column_features, column_predict, preprocessors,
                                               data_previous_historic_days)

    model.fit(x_train, y_train)

    data_prediction_day = get_data_day(complete_data, day)
    x_test, y_test = features_and_preprocess(column_features, column_predict, preprocessors, data_prediction_day)

    return Prediction(model.predict(x_test), actual_values=y_test, instance=instance)


def features_and_preprocess(column_features, column_predict, preprocessors, data):
    xs, y = features(column_features, column_predict, data)
    xs = row2col(xs)
    for preprocessor in preprocessors:
        xs = [preprocessor(x) for x in xs]
        y = preprocessor(y)
    xs = col2row(xs)
    return xs, y


def row2col(rows):
    cols = [[] for _ in range(len(rows[0]))]
    for row in rows:
        for index, value in enumerate(row):
            cols[index].append(value)
    return cols


def col2row(cols):
    rows = [[] for _ in range(len(cols[0]))]
    for col in cols:
        for index, value in enumerate(col):
            rows[index].append(value)
    return rows


def features(column_features, column_predict, data):
    xs = [[v for (k, v) in row.iteritems() if k in column_features] for row in data]
    y = [row[column_predict] for row in data]
    return xs, y


# turns every None in the column to a value perfectly between it's two neighbours.
# if every value in the column is None, this function will fail.
def interpolate_none(column):
    result = []
    none_index = -1

    if column[0] is None:
        column[0] = next(v for v in column if v is not None)
    if column[-1] is None:
        column[-1] = next(v for v in reversed(column) if v is not None)

    if column[0] is int:
        converter = int
    else:
        converter = float

    for i, v in enumerate(column):
        if v is None:
            if none_index == -1:
                none_index = i
        else:
            if none_index != -1:
                start_v = result[none_index - 1]
                end_v = v
                step = (end_v - start_v) / float(i - none_index + 1)
                result.extend([converter(start_v + step * place) for place in range(1, i - none_index + 1)])
                none_index = -1
            result.append(v)
    return result


def interpret_column_values(column):
    return map(convert_to_value_or_null, column)


def convert_to_value_or_null(value):
    try:
        value = eval(value)
        return value
    except NameError:
        return None


def export(predictions, ml_name, day, instance):
    # prediction_export_location = "predictions"
    # if not os.path.isdir(prediction_export_location):
    #     os.makedirs(prediction_export_location)
    # file_location = os.path.join(prediction_export_location, "{0}-{1}.csv".format(ml_name, day))
    # data = [{'time_slot': i, 'actual': predictions.actual_values[i], 'forecasted': predictions.prediction_values[i]} for
    #         i in range(len(predictions.actual_values))]
    # fields = ['time_slot', 'forecasted', 'actual']
    # with open(file_location, 'w') as export_file:
    #     writer = csv.DictWriter(export_file, fieldnames=fields, dialect='excel')
    #     writer.writeheader()
    #     for d in data:
    #         writer.writerow(d)
    pass


class Prediction:
    def __init__(self, prediction_values, actual_values=[], instance=None):
        self.prediction_values = prediction_values
        self.actual_values = actual_values
        self.instance = instance

    # returns {quality_metric_name: value}
    def evaluate(self):
        instance_analysis = self.instance.analyse()

        # option 1 is max - min
        w_option_1 = combine_lists(instance_analysis.max_load, instance_analysis.min_load, lambda x, y: x - y)
        w_option_1 = normalize(w_option_1)
        # option 2 is max - exp
        w_option_2 = combine_lists(instance_analysis.max_load, instance_analysis.exp_load, lambda x, y: x - y)
        w_option_2 = normalize(w_option_2)
        # option 3 is exp - min
        w_option_3 = combine_lists(instance_analysis.exp_load, instance_analysis.min_load, lambda x, y: x - y)
        w_option_3 = normalize(w_option_3)

        instance_analysis = instance_analysis.normalize()

        evaluation = OrderedDict()
        mse = self.mse()

        mae = self.mae()
        w_mae_min = self.weighted_mae(instance_analysis.min_load)
        w_mae_max = self.weighted_mae(instance_analysis.max_load)
        w_mae_exp = self.weighted_mae(instance_analysis.exp_load)
        w_mae_o1 = self.weighted_mae(w_option_1)
        w_mae_o2 = self.weighted_mae(w_option_2)
        w_mae_o3 = self.weighted_mae(w_option_3)

        spearman = self.spearman_rank_correlation()
        w_spearman_min = self.weighted_spearman_rank_correlation(instance_analysis.min_load)
        w_spearman_max = self.weighted_spearman_rank_correlation(instance_analysis.max_load)
        w_spearman_exp = self.weighted_spearman_rank_correlation(instance_analysis.exp_load)
        w_spearman_o1 = self.weighted_spearman_rank_correlation(w_option_1)
        w_spearman_o2 = self.weighted_spearman_rank_correlation(w_option_2)
        w_spearman_o3 = self.weighted_spearman_rank_correlation(w_option_3)

        evaluation['mse'] = mse
        evaluation['mae'] = mae
        evaluation['w_mae_min'] = w_mae_min
        evaluation['w_mae_max'] = w_mae_max
        evaluation['w_mae_exp'] = w_mae_exp
        evaluation['w_mae_o1'] = w_mae_o1
        evaluation['w_mae_o2'] = w_mae_o2
        evaluation['w_mae_o3'] = w_mae_o3

        evaluation['spearman'] = spearman
        evaluation['w_spearman_min'] = w_spearman_min
        evaluation['w_spearman_max'] = w_spearman_max
        evaluation['w_spearman_exp'] = w_spearman_exp
        evaluation['w_spearman_o1'] = w_spearman_o1
        evaluation['w_spearman_o2'] = w_spearman_o2
        evaluation['w_spearman_o3'] = w_spearman_o3
        return evaluation

    def mse(self):
        predictions = range(len(self.prediction_values))
        return sum([(self.prediction_values[i] - self.actual_values[i]) ** 2 for i in predictions]) / len(predictions)

    def mae(self):
        predictions = range(len(self.prediction_values))
        return sum([abs(self.prediction_values[i] - self.actual_values[i]) for i in predictions]) / len(predictions)

    def weighted_mae(self, weights):
        predictions = range(len(self.prediction_values))
        return sum([weights[i] * abs(self.prediction_values[i] - self.actual_values[i]) for i in
                         predictions]) / len(predictions)


    # https://en.wikipedia.org/wiki/Spearman's_rank_correlation_coefficient
    def spearman_rank_correlation(self):
        n = len(self.prediction_values)
        sorted_predictions = sorted(self.prediction_values)
        sorted_actuals = sorted(self.actual_values)
        summation = sum(
            [(sorted_predictions.index(self.prediction_values[i]) - sorted_actuals.index(self.actual_values[i])) ** 2
             for i in range(n)])
        n = float(n)
        spearman_rank_corr = 1 - ((6 * summation) / (n * (n ** 2 - 1)))
        return spearman_rank_corr

    # 1 - 6 * sum( w * d ** 2) / n * (n ** 2 - 1)
    def weighted_spearman_rank_correlation(self, weights):
        n = len(self.prediction_values)
        sorted_predictions = sorted(self.prediction_values)
        sorted_actuals = sorted(self.actual_values)
        summation = sum(
            [weights[i] * (sorted_predictions.index(self.prediction_values[i]) - sorted_actuals.index(self.actual_values[i])) ** 2
             for i in range(n)])
        n = float(n)
        spearman_rank_corr = 1 - ((6 * summation) / (n * (n ** 2 - 1)))
        return spearman_rank_corr


def combine_lists(a, b, f):
    c = []
    for i in range(len(a)):
        c.append(f(a[i], b[i]))
    return c


def normalize(a):
    s = sum(a)
    return map(lambda x: x/s, a)
