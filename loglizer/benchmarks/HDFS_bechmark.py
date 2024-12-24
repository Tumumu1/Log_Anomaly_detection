#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../results')#解决找不到文件的路径问题
import pandas as pd
from ..loglizer.models import *
from ..loglizer import dataloader, preprocessing
from io import StringIO
run_models = ['PCA', 'InvariantsMiner', 'LogClustering', 'IsolationForest', 'LR', 
              'SVM', 'DecisionTree']
#struct_log = '../data/HDFS/HDFS_100k.log_structured.csv' # The benchmark dataset
#log_label = '../data/HDFS/anomaly_label.csv' # The benchmark dataset
save_path = 'results/'
def model_using(struct_log,log_label):
    (x_tr, y_train), (x_te, y_test) = dataloader.load_HDFS(struct_log,label_file=log_label,
                                                           window='session', 
                                                           train_ratio=0.5,
                                                           split_type='uniform')
    benchmark_results = []
    file_name = struct_log.replace('upload/', '')
    for _model in run_models:
        print('Evaluating {} on HDFS:'.format(_model))
        if _model == 'PCA':
            feature_extractor = preprocessing.FeatureExtractor()
            x_train = feature_extractor.fit_transform(x_tr, term_weighting='tf-idf', 
                                                      normalization='zero-mean')
            model = PCA()
            model.fit(x_train)
            x_test = feature_extractor.transform(x_te)
            y_pred = model.predict(x_test)
            print("y_pred:", y_pred)
            df = pd.DataFrame(y_pred, columns=['status'])
            print("df:", df)
            df.to_csv(save_path+file_name+'_pre.csv', index=False)
    return y_pred
        # elif _model == 'InvariantsMiner':
        #     feature_extractor = preprocessing.FeatureExtractor()
        #     x_train = feature_extractor.fit_transform(x_tr)
        #     model = InvariantsMiner(epsilon=0.5)
        #     model.fit(x_train)
        #
        # elif _model == 'LogClustering':
        #     feature_extractor = preprocessing.FeatureExtractor()
        #     x_train = feature_extractor.fit_transform(x_tr, term_weighting='tf-idf')
        #     model = LogClustering(max_dist=0.3, anomaly_threshold=0.3)
        #     model.fit(x_train[y_train == 0, :]) # Use only normal samples for training
        #
        # elif _model == 'IsolationForest':
        #     feature_extractor = preprocessing.FeatureExtractor()
        #     x_train = feature_extractor.fit_transform(x_tr)
        #     model = IsolationForest(random_state=2019, max_samples=0.9999, contamination=0.03,
        #                             n_jobs=4)
        #     model.fit(x_train)
        #
        # elif _model == 'LR':
        #     feature_extractor = preprocessing.FeatureExtractor()
        #     x_train = feature_extractor.fit_transform(x_tr, term_weighting='tf-idf')
        #     model = LR()
        #     model.fit(x_train, y_train)
        #
        # elif _model == 'SVM':
        #     feature_extractor = preprocessing.FeatureExtractor()
        #     x_train = feature_extractor.fit_transform(x_tr, term_weighting='tf-idf')
        #     model = SVM()
        #     model.fit(x_train, y_train)
        #
        # elif _model == 'DecisionTree':
        #     feature_extractor = preprocessing.FeatureExtractor()
        #     x_train = feature_extractor.fit_transform(x_tr, term_weighting='tf-idf')
        #     model = DecisionTree()
        #     model.fit(x_train, y_train)
        #
        # x_test = feature_extractor.transform(x_te)
        # print('Train accuracy:')
        # precision, recall, f1 = model.evaluate(x_train, y_train)
        # benchmark_results.append([_model + '-train', precision, recall, f1])
        # print('Test accuracy:')
        # precision, recall, f1 = model.evaluate(x_test, y_test)
        # benchmark_results.append([_model + '-test', precision, recall, f1])

   # pd.DataFrame(benchmark_results, columns=['Model', 'Precision', 'Recall', 'F1']) \
     # .to_csv('benchmark_result.csv', index=False)
