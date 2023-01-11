import numpy as np
import pandas as pd
import plotly.graph_objects as go
from AppData import app_data
from dash import Input, Output, State, callback, ctx, html
from IdHolder import IdHolder
from layout import app
from utils import (
    get_metrics,
    plot_confusion_matrix,
    plot_corr_matrix,
    plot_feature_importance,
    plot_loss,
    plot_models_performance,
    plot_precision_recall,
    plot_predict_proba,
    plot_roc_auc,
    plot_tpr_fpr,
)


@app.callback(
    [
        Output(IdHolder.update.name, 'n_clicks'),
        Output(IdHolder.model_dropdown.name, 'value'),
    ],
    [
        Input(IdHolder.model_dropdown.name, 'value'),
    ],
)
def update(v):
    app_data.update_models()
    app_data.update_selected_model(v)
    return [0, app_data.model_id]


@app.callback(
    Output(IdHolder.update_metrics.name, 'n_clicks'),
    Input(IdHolder.update.name, 'n_clicks'),
    State(IdHolder.model_dropdown.name, 'value'),
    prevent_initial_call=True,
)
def update_metrics(n_clicks, model_id):
    app_data.update_metrics(model_id)
    return n_clicks + 1


@app.callback(
    Output(IdHolder.update_preds.name, 'n_clicks'),
    Input(IdHolder.update.name, 'n_clicks'),
    State(IdHolder.model_dropdown.name, 'value'),
    prevent_initial_call=True,
)
def update_preds(n_clicks, model_id):
    app_data.update_preds(model_id)
    return n_clicks + 1


@app.callback(
    Output(IdHolder.model_dropdown.name, 'options'),
    Input(IdHolder.update.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_model_dropdown(n_clicks):
    return [
        {
            'label': html.Span(
                f'Model {model_id}',
                style={
                    'color': 'rgb(242, 242, 242)',
                    'background-color': '#4f4f4f',
                    'display': 'block',
                    'width': '100%',
                    'height': '100%',
                },
                className='model-select',
            ),
            'value': model_id,
        }
        for model_id in app_data.model_ids
    ]


@app.callback(
    [
        Output(IdHolder.tnr.name, 'children'),
        Output(IdHolder.fpr.name, 'children'),
        Output(IdHolder.fdr.name, 'children'),
        Output(IdHolder.fnr.name, 'children'),
        Output(IdHolder.tpr.name, 'children'),
        Output(IdHolder.npv.name, 'children'),
        Output(IdHolder.roc_auc.name, 'children'),
        Output(IdHolder.f1_beta.name, 'children'),
        Output(IdHolder.precision.name, 'children'),
    ],
    Input(IdHolder.update_metrics.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_metrics_(_):
    return get_metrics()


@app.callback(
    Output(IdHolder.models_performance_graph.name, 'figure'),
    Input(IdHolder.update_metrics.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_models_performance(_):
    return plot_models_performance()


@app.callback(
    Output(IdHolder.predict_proba_graph.name, 'figure'),
    Input(IdHolder.update_preds.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_predict_proba(_):
    return plot_predict_proba()


@app.callback(
    Output(IdHolder.tpr_fpr_graph.name, 'figure'),
    Input(IdHolder.update_preds.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_tpr_fpr(_):
    return plot_tpr_fpr()


@app.callback(
    Output(IdHolder.roc_auc_graph.name, 'figure'),
    Input(IdHolder.update_preds.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_roc_auc(_):
    return plot_roc_auc()


@app.callback(
    Output(IdHolder.precision_recall_graph.name, 'figure'),
    Input(IdHolder.update_preds.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_precision_recall(_):
    return plot_precision_recall()


@app.callback(
    [
        Output(IdHolder.confusion_matrix_graph.name, 'figure'),
        Output(IdHolder.confusion_title.name, 'children'),
    ],
    [
        Input(IdHolder.update_metrics.name, 'n_clicks'),
        Input(IdHolder.confusion_switch.name, 'value'),
    ],
    prevent_initial_call=True,
)
def update_confusion_matrix(_, confusion_switch):
    return [
        plot_confusion_matrix(type=bool(len(confusion_switch))),
        'Confusion Sankey' if len(confusion_switch) else 'Confusion Matrix',
    ]


@app.callback(
    Output(IdHolder.correlation_matrix_graph.name, 'figure'),
    Input(IdHolder.update_metrics.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_correlation_matrix(_):
    return plot_corr_matrix()


@app.callback(
    Output(IdHolder.feature_importance_graph.name, 'figure'),
    Input(IdHolder.update_metrics.name, 'n_clicks'),
    prevent_initial_call=True,
)
def update_feature_importance(_):
    return plot_feature_importance()


@app.callback(
    Output(IdHolder.loss_graph.name, 'figure'),
    Input(IdHolder.model_dropdown.name, 'value'),
    State(IdHolder.loss_graph.name, 'figure'),
    prevent_initial_call=True,
)
def update_loss(_, loss_graph):
    return plot_loss() if ctx.triggered_id == IdHolder.model_dropdown.name or not ctx.triggered_id else loss_graph
