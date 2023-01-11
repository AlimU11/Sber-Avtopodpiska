import numpy as np
from sklearn.metrics import confusion_matrix, fbeta_score, roc_auc_score


def calculate_metrics(y_test, y_pred_proba):
    y_pred = np.argmax(y_pred_proba, axis=1)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])
    f_beta = fbeta_score(y_test, y_pred, beta=(y_test == 0).sum() / (y_test == 1).sum())

    return [tn, fp, fn, tp, roc_auc, f_beta]
