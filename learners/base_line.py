#!/usr/bin/env python

from scripts.prices_data import get_data_day
import core


def base_line(day, prediction_data, instance):
    data_prediction_day = get_data_day(prediction_data, day)
    prediction, actual = core.features_and_preprocess(
        ['SMPEA'],
        'SMPEP2',
        [core.interpret_column_values, core.interpolate_none],
        data_prediction_day)
    prediction = [p[0] for p in prediction]
    return core.Prediction(prediction, actual_values=actual, instance=instance)