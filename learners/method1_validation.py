#!/usr/bin/env python

import core
from sklearn import ensemble
from sklearn import neural_network

basic_features = ['HolidayFlag', 'DayOfWeek', 'PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA', 'SMPEA']
all_features = ['HolidayFlag', 'DayOfWeek', 'WeekOfYear', 'Day', 'Month', 'Year', 'PeriodOfDay',
                'ForecastWindProduction', 'SystemLoadEA', 'SMPEA', 'ORKTemperature', 'ORKWindspeed',
                'CO2Intensity', 'ActualWindProduction', 'SystemLoadEP2']
few_features = ['PeriodOfDay', 'ForecastWindProduction', 'SystemLoadEA']
column_predict = 'SMPEP2'

simple_preprocessors = [core.interpolate_none]


# RANDOM FOREST LEARNERS
def make_m1_random_forest_function(n_estimators, criterion, max_features, max_depth):
    historic_days = 300

    clf = ensemble.RandomForestRegressor(
        n_estimators=n_estimators,
        criterion=criterion,
        max_features=max_features,
        max_depth=max_depth
    )

    name = "m1_val_rf_{0}_trees_{1}_{2}_max_feat_{3}_max_depth".format(n_estimators,
                                                                       criterion, max_features, str(max_depth))

    def make_prediction(day, prediction_data, instance):
        predictions = core.generic_learner(all_features, column_predict, simple_preprocessors, clf,
                                           day, prediction_data, instance, historic_days)
        # core.export(predictions, 'm1_val_rf_10_trees_mse_auto_max_feat_none_max_depth', day, instance)
        return predictions

    return name, make_prediction


def make_m1_random_forest_function_base_line():
    historic_days = 300

    clf = ensemble.RandomForestRegressor()

    name = 'm1_val_rf_base_line_default_params'

    def make_prediction(day, prediction_data, instance):
        predictions = core.generic_learner(all_features, column_predict, simple_preprocessors, clf,
                                           day, prediction_data, instance, historic_days)
        # core.export(predictions, 'm1_val_rf_10_trees_mse_auto_max_feat_none_max_depth', day, instance)
        return predictions

    return name, make_prediction


def iterate_random_forest_m1(args):
    number_of_estimators = [5 * (2 ** i) for i in range(7)]
    criterion = [args]
    max_features = ["auto", "sqrt", "log2", 0.1, 0.5, 0.8]
    max_depth = [None] + [2 * i for i in range(1, 10)]

    for n in number_of_estimators:
        for c in criterion:
            for mf in max_features:
                for md in max_depth:
                    yield make_m1_random_forest_function(n, c, mf, md)
    yield make_m1_random_forest_function_base_line()


def best_spearman_random_forest(day, prediction_data, instance):
    n = 160
    c = "mse"
    mf = 0.5
    md = 6
    _, model = make_m1_random_forest_function(n, c, mf, md)
    return model(day, prediction_data, instance)


def second_spearman_random_forest(day, prediction_data, instance):
    n = 320
    c = "mse"
    mf = 0.5
    md = 6
    _, model = make_m1_random_forest_function(n, c, mf, md)
    return model(day, prediction_data, instance)


def best_mae_random_forest(day, prediction_data, instance):
    n = 80
    c = "mse"
    mf = "log2"
    md = 10
    _, model = make_m1_random_forest_function(n, c, mf, md)
    return model(day, prediction_data, instance)

def second_mae_random_forest(day, prediction_data, instance):
    n = 320
    c = "mse"
    mf = "sqrt"
    md = 10
    _, model = make_m1_random_forest_function(n, c, mf, md)
    return model(day, prediction_data, instance)



# MULTI LAYER PERCEPTRON
def make_m1_mlp_function(hidden_layer_size, activation, alpha):
    historic_days = 300

    clf = neural_network.MLPRegressor(
        hidden_layer_sizes=hidden_layer_size,
        activation=activation,
        alpha=alpha
    )

    name = "m1_val_mlp_{0}_alpha_{1}_activation_hidden_layers_".format(alpha, activation)
    for layer in hidden_layer_size:
        name += str(layer) + '_'
    name = name[:-1]

    def make_prediction(day, prediction_data, instance):
        predictions = core.generic_learner(all_features, column_predict, simple_preprocessors, clf,
                                           day, prediction_data, instance, historic_days)
        # core.export(predictions, 'm1_val_rf_10_trees_mse_auto_max_feat_none_max_depth', day, instance)
        return predictions

    return name, make_prediction


def make_m1_mlp_function_base_line():
    historic_days = 300

    clf = neural_network.MLPRegressor()

    name = "m1_val_mlp_base_line"

    def make_prediction(day, prediction_data, instance):
        predictions = core.generic_learner(all_features, column_predict, simple_preprocessors, clf,
                                           day, prediction_data, instance, historic_days)
        # core.export(predictions, 'm1_val_rf_10_trees_mse_auto_max_feat_none_max_depth', day, instance)
        return predictions

    return name, make_prediction


def iterate_mlp_m1():
    hidden_layers = [(10 * (2 ** i),) for i in range(7)]
    activations = ["identity", "logistic", "relu", 'tanh']
    alphas = [10 ** i for i in range(-8, 8)]

    for h in hidden_layers:
        for ac in activations:
            for al in alphas:
                yield make_m1_mlp_function(h, ac, al)
    yield make_m1_mlp_function_base_line()
