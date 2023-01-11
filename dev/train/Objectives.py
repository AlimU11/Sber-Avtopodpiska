import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.utils import class_weight
from xgboost import XGBClassifier


class Objectives:
    """Objective functions for hyperparameter optimization with Optuna."""

    def __init__(self, X_train, y_train, X_test, y_test, weighted=False):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.weighted = weighted

        self.sample_weights = class_weight.compute_sample_weight(
            class_weight='balanced',
            y=self.y_train,
        )

        self.class_weights = dict(
            zip(
                np.unique(self.y_train),
                class_weight.compute_class_weight(
                    class_weight='balanced',
                    classes=np.unique(self.y_train),
                    y=self.y_train,
                ),
            ),
        )

    def objective_XGBoost(self, trial):
        params = {
            'verbosity': 0,
            'objective': 'binary:logistic',
            'tree_method': 'gpu_hist',
            'learning_rate': trial.suggest_float('learning_rate', 1e-3, 1e-1),
            'booster': trial.suggest_categorical('booster', ['gbtree', 'dart']),
            'n_estimators': trial.suggest_int('n_estimators', 100, 350),
            'lambda': trial.suggest_float('lambda', 1e-8, 1.0, log=True),
            'alpha': trial.suggest_float('alpha', 1e-8, 1.0, log=True),
            'subsample': trial.suggest_float('subsample', 0.2, 1.0),
            'colsample_bytree': trial.suggest_float(
                'colsample_bytree',
                0.2,
                1.0,
            ),
            'use_label_encoder': False,
        }

        if params['booster'] in ['gbtree', 'dart']:
            params['max_depth'] = trial.suggest_int('max_depth', 3, 15, step=2)
            params['min_child_weight'] = trial.suggest_int(
                'min_child_weight',
                2,
                10,
            )
            params['eta'] = trial.suggest_float('eta', 1e-8, 1.0, log=True)
            params['gamma'] = trial.suggest_float('gamma', 1e-8, 1.0, log=True)
            params['grow_policy'] = trial.suggest_categorical(
                'grow_policy',
                ['depthwise', 'lossguide'],
            )

        if params['booster'] == 'dart':
            params['sample_type'] = trial.suggest_categorical(
                'sample_type',
                ['uniform', 'weighted'],
            )
            params['normalize_type'] = trial.suggest_categorical(
                'normalize_type',
                ['tree', 'forest'],
            )
            params['rate_drop'] = trial.suggest_float(
                'rate_drop',
                1e-8,
                1.0,
                log=True,
            )
            params['skip_drop'] = trial.suggest_float(
                'skip_drop',
                1e-8,
                1.0,
                log=True,
            )

        clf = XGBClassifier(**params)
        clf.fit(
            self.X_train,
            self.y_train,
            sample_weight=self.sample_weights if self.weighted else None,
        )

        score = roc_auc_score(self.y_test, clf.predict_proba(self.X_test)[:, 1])

        return score

    def objective_LogisticRegression(self, trial):
        params = {
            'C': trial.suggest_float('C', 1e-10, 1e10, log=True),
            'tol': trial.suggest_float('tol', 1e-10, 1e2),
            'solver': trial.suggest_categorical(
                'solver',
                [
                    'lbfgs',
                    'liblinear',
                    'newton-cg',
                    'newton-cholesky',
                    'sag',
                    'saga',
                ],
            ),
            'n_jobs': -1,
            'max_iter': 1000,
        }

        if params['solver'] in ['lbfgs', 'newton-cg', 'newton-cholesky', 'sag']:
            params['penalty'] = 'l2'

        if params['solver'] in ['liblinear', 'saga']:

            params['penalty'] = (trial.suggest_categorical('penalty', ['l1', 'l2']),)

        clf = LogisticRegression(
            class_weight=self.class_weights if self.weighted else None,
        )
        clf.fit(self.X_train, self.y_train)

        score = roc_auc_score(self.y_test, clf.predict_proba(self.X_test)[:, 1])

        return score

    def objective_GaussianNB(self, trial):
        params = {
            'var_smoothing': trial.suggest_categorical(
                'var_smoothing',
                [1e-12, 1e-11, 1e-10, 1e-9, 1e-8],
            ),
        }

        clf = GaussianNB(**params)
        clf.fit(
            self.X_train,
            self.y_train,
            sample_weight=self.sample_weights if self.weighted else None,
        )

        score = roc_auc_score(self.y_test, clf.predict_proba(self.X_test)[:, 1])

        return score

    def objective_AdaBoost(self, trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 25, 350),
            'learning_rate': trial.suggest_float('learning_rate', 1e-3, 1),
        }

        clf = AdaBoostClassifier(**params)
        clf.fit(self.X_train, self.y_train)

        score = roc_auc_score(self.y_test, clf.predict_proba(self.X_test)[:, 1])

        return score

    def objective_RandomForest(self, trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 25, 350),
            'criterion': trial.suggest_categorical(
                'criterion',
                ['gini', 'entropy', 'log_loss'],
            ),
            'max_depth': trial.suggest_int('max_depth', 3, 15, step=2),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'min_weight_fraction_leaf': trial.suggest_float(
                'min_weight_fraction_leaf',
                0,
                0.5,
            ),
            'max_features': trial.suggest_categorical(
                'max_features',
                ['sqrt', 'log2'],
            ),
            'max_leaf_nodes': trial.suggest_int('max_leaf_nodes', 2, 10),
            'bootstrap': True,
            'oob_score': trial.suggest_categorical('oob_score', [True, False]),
            'n_jobs': -1,
        }

        clf = RandomForestClassifier(
            class_weight=self.class_weights if self.weighted else None,
            **params,
        )
        clf.fit(self.X_train, self.y_train)

        score = roc_auc_score(self.y_test, clf.predict_proba(self.X_test)[:, 1])

        return score

    def objective_SVM(self, trial):
        params = {
            'tol': trial.suggest_float('tol', 1e-5, 1e-1),
            'C': trial.suggest_float('C', 1e-3, 1000),
            'dual': False,
        }

        clf = LinearSVC(
            class_weight=self.class_weights if self.weighted else None,
            **params,
        )

        calibrated_svc = CalibratedClassifierCV(
            clf,
            method='sigmoid',
            cv=3,
        )

        calibrated_svc.fit(self.X_train, self.y_train)

        score = roc_auc_score(
            self.y_test,
            calibrated_svc.predict_proba(self.X_test)[:, 1],
        )

        return score

    # def objective_CatBoost(self, trial):
    #     params = {
    #         "iterations": trial.suggest_int("iterations", 100, 500),
    #         "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2),
    #         "depth": trial.suggest_int("depth", 3, 15, step=2),
    #         "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1e-3, 1),
    #         "random_strength": trial.suggest_float(
    #             "random_strength", 1e-8, 10.0, log=True
    #         ),
    #         "bootstrap_type": trial.suggest_categorical(
    #             "bootstrap_type", ["Bayesian", "Bernoulli"]
    #         ),
    #         "grow_policy": trial.suggest_categorical(
    #             "grow_policy", ["SymmetricTree", "Lossguide"]
    #         ),
    #         "max_bin": trial.suggest_int("max_bin", 2, 10),
    #         "task_type": "GPU",
    #         "silent": True,
    #         "eval_metric": "AUC",
    #         "od_type": trial.suggest_categorical(
    #             "od_type", ["IncToDec", "Iter"]
    #         ),
    #         "od_wait": trial.suggest_int("od_wait", 10, 50),
    #         "allow_writing_files": False,
    #     }

    #     if params["grow_policy"] == "Lossguide":
    #         params["max_leaves"] = trial.suggest_int("max_leaves", 2, 10)
    #         params["min_data_in_leaf"] = trial.suggest_int(
    #             "min_data_in_leaf", 2, 10
    #         )

    #     if params["bootstrap_type"] == "Bayesian":
    #         params["bagging_temperature"] = trial.suggest_float(
    #             "bagging_temperature", 0, 10
    #         )

    #     if params["bootstrap_type"] == "Bernoulli":
    #         params["subsample"] = trial.suggest_float("subsample", 0.1, 1)

    #     clf = CatBoostClassifier(
    #         class_weights=self.class_weights if self.weighted else None,
    #         **params
    #     )
    #     clf.fit(self.X_train, self.y_train)

    #     score = roc_auc_score(self.y_test, clf.predict_proba(self.X_test)[:, 1])

    #     return score

    # def objective_LightGBM(self, trial):
    #     params = {
    #         "n_estimators": trial.suggest_int("n_estimators", 100, 350),
    #         "learning_rate": trial.suggest_float("learning_rate", 1e-3, 1),
    #         "num_leaves": trial.suggest_int("num_leaves", 2, 10),
    #         "max_depth": trial.suggest_int("max_depth", 3, 15, step=2),
    #         "min_child_samples": trial.suggest_int("min_child_samples", 2, 10),
    #         "subsample": trial.suggest_float("subsample", 0.2, 1.0),
    #         "subsample_freq": trial.suggest_int("subsample_freq", 1, 10),
    #         "colsample_bytree": trial.suggest_float(
    #             "colsample_bytree", 0.2, 1.0
    #         ),
    #         "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 1),
    #         "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 1),
    #         "n_jobs": -1,
    #         "device": "gpu",
    #     }

    #     clf = LGBMClassifier(
    #         class_weight=self.class_weights if self.weighted else None, **params
    #     )
    #     clf.fit(self.X_train, self.y_train)

    #     score = roc_auc_score(self.y_test, clf.predict_proba(self.X_test)[:, 1])

    #     return score
