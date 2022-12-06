from enum import Enum, auto


class IdHolder(Enum):
    model_dropdown = auto()

    # metrics
    precision = auto()
    tnr = auto()
    fpr = auto()
    cohen_kappa = auto()
    fnr = auto()
    tpr = auto()
    roc_auc = auto()
    f1_score = auto()
    avg_precision = auto()

    # graphs
    models_performance_graph = auto()
    roc_auc_graph = auto()
    tpr_fpr_graph = auto()
    confusion_matrix_graph = auto()
    correlation_matrix_graph = auto()
    feature_importance_graph = auto()
    partial_dependence_graph = auto()
