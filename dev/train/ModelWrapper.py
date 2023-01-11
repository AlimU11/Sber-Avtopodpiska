from typing import Optional

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils import class_weight


class ModelWrapper(BaseEstimator, ClassifierMixin):
    """Wrapper for resampler and classifier. Adapts resampler from smote_variants to sklearn pipeline API."""

    def __init__(self, resampler, classifier):
        self.resampler = resampler
        self.classifier = classifier

    def fit(self, X, y=None, **fit_params):
        X_resampled, y_resampled = (
            self.resampler.sample(X.values, getattr(y, 'values', y)) if self.resampler else (X, y)
        )

        sample_weights = class_weight.compute_sample_weight(
            class_weight='balanced',
            y=y_resampled,
        )

        self.classifier.fit(X_resampled, y_resampled, sample_weight=sample_weights, **fit_params)
        return self

    def predict(self, X):
        return self.classifier.predict(X)

    def predict_proba(self, X):
        return self.classifier.predict_proba(X)

    def get_params(self, deep=True):
        return {'resampler': self.resampler, 'classifier': self.classifier}

    def set_params(self, **params):
        for parameter, value in params.items():
            setattr(self, parameter, value)
        return self

    @property
    def feature_importances_(self) -> Optional[np.ndarray]:
        return getattr(self.classifier, 'feature_importances_', None)

    @property
    def evals_result_(self) -> Optional[dict]:
        return getattr(self.classifier, 'evals_result_', None)
