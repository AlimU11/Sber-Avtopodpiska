import pickle
from typing import Optional

import sqlalchemy
from Config import config
from numpy import ndarray
from pandas import DataFrame
from sklearn.metrics import precision_recall_curve, roc_curve


class AppData:
    """Web App data holder class.

    Attributes
    ----------

    config : Config
        Config object with database connection string.

    engine : sqlalchemy.engine.Engine
        SQLAlchemy engine object.

    model_id : int
        Model id to present data for.

    fact : tuple[int], optional
        Real values on test set.

    predict_proba : tuple[float], optional
        Predicted probabilities on test set.

    fpr_arr : ndarray, optional
        Increasing false positive rates such that element i is the false positive rate of predictions with score >= thresholds[i].

    tpr_arr : ndarray, optional
        Increasing true positive rates such that element i is the true positive rate of predictions with score >= thresholds[i].

    thresholds_roc : ndarray, optional
        Decreasing thresholds on the decision function used to compute fpr and tpr. thresholds[0] represents no instances being predicted and is arbitrarily set to max(y_score) + 1.

    precision_arr : ndarray, optional
        Precision values such that element i is the precision of predictions with score >= thresholds[i] and the last element is 1.

    recall_arr : ndarray, optional
        Decreasing recall values such that element i is the recall of predictions with score >= thresholds[i] and the last element is 0.

    thresholds_precision_recall : ndarray, optional
        Increasing thresholds on the decision function used to compute precision and recall where n_thresholds = len(np.unique(probas_pred)).

    tn : float, optional
        True negatives count.

    fp : float, optional
        False positives count.

    fn : float, optional
        False negatives count.

    tp : float, optional
        True positives count.

    tnr : float, optional
        True negative rate.

    fpr : float, optional
        False positive rate.

    fdr : float, optional
        False discovery rate.

    fnr : float, optional
        False negative rate.

    tpr : float, optional
        True positive rate.

    npv : float, optional
        Negative predictive value.

    ppv : float, optional
        Positive predictive value.

    roc_auc : float, optional
        ROC AUC score.

    f1_beta : float, optional
        F1 score.

    feature_importance : DataFrame, optional
        Feature importances of the model.

    corr : DataFrame, optional
        Feature correlation matrix.

    train_loss : list[float], optional
        Loss values on train set.

    val_loss : list[float], optional
        Loss values on validation set.

    roc_auc_scores : list[float]
        ROC AUC scores of all models.

    model_ids : list[str]
        Model ids of all models.
    """

    def __init__(self):
        self.config = config
        self.engine = sqlalchemy.create_engine(self.config.db_url)

        self.model_id: int = -1

        self.fact: Optional[tuple[int]] = None
        self.predict_proba: Optional[tuple[float]] = None
        self.fpr_arr: Optional[ndarray] = None
        self.tpr_arr: Optional[ndarray] = None
        self.thresholds_roc: Optional[ndarray] = None
        self.precision_arr: Optional[ndarray] = None
        self.recall_arr: Optional[ndarray] = None
        self.thresholds_precision_recall: Optional[ndarray] = None

        self.tn: Optional[float] = None
        self.fp: Optional[float] = None
        self.fn: Optional[float] = None
        self.tp: Optional[float] = None

        self.tnr: Optional[float] = None
        self.fpr: Optional[float] = None
        self.fdr: Optional[float] = None
        self.fnr: Optional[float] = None
        self.tpr: Optional[float] = None
        self.npv: Optional[float] = None
        self.ppv: Optional[float] = None

        self.roc_auc: Optional[float] = None
        self.f1_beta: Optional[float] = None
        self.feature_importance: Optional[DataFrame] = None
        self.corr: Optional[DataFrame] = None
        self.train_loss: Optional[list[float]] = None
        self.val_loss: Optional[list[float]] = None
        self.roc_auc_scores: list[float] = []
        self.model_ids: list[str] = []

        self.update_models()
        self.update_selected_model()
        self.update_preds()
        self.update_metrics()

    def update_selected_model(self, model_idx=None):
        """Update model id to present data for."""
        self.model_id = model_idx if model_idx else self.model_ids[-1]

    def update_models(self):
        """Update model ids of all models."""
        self.model_ids = [
            i[0]
            for i in self.engine.execute(
                '''
                SELECT m.model_id
                FROM scores.models m
                GROUP BY m.model_id
                ORDER BY m.dt ASC
                ;
                ''',
            ).fetchall()
        ]

    def update_preds(self, model_id=None):
        """Update predictions and metrics based on model_id"""
        self.model_id = model_id if model_id else self.model_id

        c = self.engine.execute(
            '''
            SELECT t.fact, t.pred_proba
            FROM scores.train_pred t
            WHERE t.model_id = %s
            ;
            '''
            % self.model_id,
        )

        self.fact, self.predict_proba = zip(*c.fetchall())

        self.fpr_arr, self.tpr_arr, self.thresholds_roc = roc_curve(
            self.fact,
            self.predict_proba,
        )
        self.precision_arr, self.recall_arr, self.thresholds_precision_recall = precision_recall_curve(
            self.fact,
            self.predict_proba,
        )

    def update_metrics(self, model_id=None):
        """Update predictions and metrics based on model_id"""
        self.model_id = model_id if model_id else self.model_id

        c = self.engine.execute(
            '''
            SELECT *
            FROM scores.metrics m
            WHERE model_id = %s
            ;
            '''
            % self.model_id,
        )

        (
            _,
            self.tn,
            self.fp,
            self.fn,
            self.tp,
            self.roc_auc,
            self.f1_beta,
            self.feature_importance,
            self.corr,
            evals_result,
        ) = c.fetchone()

        evals_result = pickle.loads(evals_result)

        # NOTE: consider make logloss variable
        self.train_loss, self.val_loss = (
            evals_result['validation_0']['logloss'],
            evals_result['validation_1']['logloss'],
        )

        self.feature_importance = pickle.loads(self.feature_importance)
        self.corr = pickle.loads(self.corr)

        self.tnr = self.tn / (self.tn + self.fp)
        self.fpr = self.fp / (self.fp + self.tn)
        self.fdr = self.fp / (self.tp + self.fp)
        self.fnr = self.fn / (self.tp + self.fn)
        self.tpr = self.tp / (self.tp + self.fn)
        self.npv = self.tn / (self.tn + self.fn)
        self.ppv = self.tp / (self.tp + self.fp)

        # TODO: remove
        c = self.engine.execute(
            '''
            SELECT m.model_id, m.roc_auc
            FROM (
                SELECT i.model_id, MIN(i.roc_auc) as roc_auc
                FROM scores.metrics i
                GROUP by i.model_id
            ) m
            LEFT JOIN scores.models md
            ON m.model_id = md.model_id
            ORDER BY md.dt ASC
            ;
            ''',
        )
        self.roc_auc_scores = [i[1] for i in c.fetchall()]


app_data = AppData()
