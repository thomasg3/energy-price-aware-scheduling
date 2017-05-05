#!/usr/bin/env python

import base_line as bl
import linear
import svm
import nearest_neighbors as nn
import ensemble
import ann
import method2_learners as m2


learners = {
    # baseline (using SEMO prediction)
    'base_line': bl.base_line,
    # Bayesian Ridge Regression
    'bay_reg_few_feat_30_days': linear.bayesian_regression_few_features_30_days,
    'bay_reg_few_feat_90_days': linear.bayesian_regression_few_features_90_days,
    'bay_reg_few_feat_300_days': linear.bayesian_regression_few_features_300_days,
    'bay_reg_basic_feat_30_days': linear.bayesian_regression_basic_features_30_days,
    'bay_reg_basic_feat_90_days': linear.bayesian_regression_basic_features_90_days,
    'bay_reg_basic_feat_300_days': linear.bayesian_regression_basic_features_300_days,
    'bay_reg_all_feat_30_days': linear.bayesian_regression_all_features_30_days,
    'bay_reg_all_feat_90_days': linear.bayesian_regression_all_features_90_days,
    'bay_reg_all_feat_300_days': linear.bayesian_regression_all_features_300_days,
    # Support Vector Machine Regression
    'lin_svr_c1e3_few_feat_30_days': svm.lin_svr_c1e3_few_features_30_days,
    'lin_svr_c1e3_basic_feat_30_days': svm.lin_svr_c1e3_basic_features_30_days,
    'lin_svr_c1e3_all_feat_30_days': svm.lin_svr_c1e3_all_features_30_days,
    'lin_svr_c1e3_few_feat_90_days': svm.lin_svr_c1e3_few_features_90_days,
    'lin_svr_c1e3_basic_feat_90_days': svm.lin_svr_c1e3_basic_features_90_days,
    'lin_svr_c1e3_all_feat_90_days': svm.lin_svr_c1e3_all_features_90_days,
    'lin_svr_c1e3_few_feat_300_days': svm.lin_svr_c1e3_few_features_300_days,
    'lin_svr_c1e3_basic_feat_300_days': svm.lin_svr_c1e3_basic_features_300_days,
    'lin_svr_c1e3_all_feat_300_days': svm.lin_svr_c1e3_all_features_300_days,
    # Nearest Neighbours
    'knn_11nn_distance_few_feat_30_days': nn.knn_11nn_distance_few_feat_30_days,
    'knn_11nn_distance_few_feat_90_days': nn.knn_11nn_distance_few_feat_90_days,
    'knn_11nn_distance_few_feat_300_days': nn.knn_11nn_distance_few_feat_300_days,
    'knn_11nn_distance_basic_feat_30_days': nn.knn_11nn_distance_basic_feat_30_days,
    'knn_11nn_distance_basic_feat_90_days': nn.knn_11nn_distance_basic_feat_90_days,
    'knn_11nn_distance_basic_feat_300_days': nn.knn_11nn_distance_basic_feat_300_days,
    'knn_11nn_distance_all_feat_30_days': nn.knn_11nn_distance_all_feat_30_days,
    'knn_11nn_distance_all_feat_90_days': nn.knn_11nn_distance_all_feat_90_days,
    'knn_11nn_distance_all_feat_300_days': nn.knn_11nn_distance_all_feat_300_days,
    # Ensemble methods
    'random_forest_few_feat_30_days': ensemble.random_forest_few_features_30_days,
    'random_forest_basic_feat_30_days': ensemble.random_forest_basic_features_30_days,
    'random_forest_all_feat_30_days': ensemble.random_forest_all_features_30_days,
    'random_forest_few_feat_90_days': ensemble.random_forest_few_features_90_days,
    'random_forest_basic_feat_90_days': ensemble.random_forest_basic_features_90_days,
    'random_forest_all_feat_90_days': ensemble.random_forest_all_features_90_days,
    'random_forest_few_feat_300_days': ensemble.random_forest_few_features_300_days,
    'random_forest_basic_feat_300_days': ensemble.random_forest_basic_features_300_days,
    'random_forest_all_feat_300_days': ensemble.random_forest_all_features_300_days,
    # Multi-layer Perceptron Regressor
    'mlp_few_feat_30_days': ann.mlp_few_features_30_days,
    'mlp_basic_feat_30_days': ann.mlp_basic_features_30_days,
    'mlp_all_feat_30_days': ann.mlp_all_features_30_days,
    'mlp_few_feat_90_days': ann.mlp_few_features_90_days,
    'mlp_basic_feat_90_days': ann.mlp_basic_features_90_days,
    'mlp_all_feat_90_days': ann.mlp_all_features_90_days,
    'mlp_few_feat_300_days': ann.mlp_few_features_300_days,
    'mlp_basic_feat_300_days': ann.mlp_basic_features_300_days,
    'mlp_all_feat_300_days': ann.mlp_all_features_300_days,
}


def iterator():
    return learners.iteritems()


def method2():
    return {
        # Method 2 learners
        'm2_spearman_all_feat_300_days': m2.m2_spearman_all_feat_300_days,
        'm2_spearman_opt_all_feat_300_days': m2.m2_spearman_opt_all_feat_300_days,
        'm2_mae_all_feat_300_days': m2.m2_mae_all_feat_300_days,
        'm2_mae_opt_all_feat_300_days': m2.m2_mae_opt_all_feat_300_days,
        'm2_random_all_feat_300_days': m2.m2_random_all_feat_300_days,
    }.iteritems()
