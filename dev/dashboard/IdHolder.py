from enum import Enum, auto


class IdHolder(Enum):
    # controllers
    update = auto()
    update_metrics = auto()
    update_preds = auto()
    model_dropdown = auto()
    confusion_switch = auto()
    confusion_title = auto()

    # metrics
    tnr = auto()
    fpr = auto()
    fdr = auto()
    fnr = auto()
    tpr = auto()
    npv = auto()
    roc_auc = auto()
    f1_beta = auto()
    precision = auto()

    # graphs
    models_performance_graph = auto()
    predict_proba_graph = auto()
    tpr_fpr_graph = auto()
    roc_auc_graph = auto()
    precision_recall_graph = auto()
    confusion_matrix_graph = auto()
    correlation_matrix_graph = auto()
    feature_importance_graph = auto()
    partial_dependence_graph = auto()
