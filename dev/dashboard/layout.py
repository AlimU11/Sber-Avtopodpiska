import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from IdHolder import IdHolder


def metrics_card(title, id):
    return dbc.Card(
        dbc.CardBody(
            children=[
                html.H5(f'{title}', className='card-title'),
                dbc.Spinner(
                    html.P('0%', className='card-text', id=id),
                ),
            ],
        ),
    )


def graph_card(title, id, config={}):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(f'{title}', className='card-title'),
                dbc.Spinner(
                    dcc.Graph(
                        id=id,
                        config=config,
                    ),
                ),
            ],
        ),
    )


layout = html.Div(
    children=[
        html.Div(
            [
                dbc.Button(id=IdHolder.update_metrics.name),
                dbc.Button(id=IdHolder.update_preds.name),
                dbc.Button(id=IdHolder.update.name),
            ],
            style='display: none',
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(children='Train Results for model'),
                        dcc.Dropdown(
                            id=IdHolder.model_dropdown.name,
                            options=[],
                            placeholder='Select a model',
                            clearable=False,
                            searchable=False,
                        ),
                    ],
                    className='grid-column card',
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                metrics_card('TNR', IdHolder.tnr.name),
                                metrics_card('FPR', IdHolder.fpr.name),
                                metrics_card('FDR', IdHolder.fdr.name),
                                metrics_card('FNR', IdHolder.fnr.name),
                                metrics_card('TPR', IdHolder.tpr.name),
                                metrics_card('NPV', IdHolder.npv.name),
                                metrics_card('ROC AUC', IdHolder.roc_auc.name),
                                metrics_card('F1', IdHolder.f1_beta.name),
                                metrics_card(
                                    'Precision',
                                    IdHolder.precision.name,
                                ),
                            ],
                            className='metrics-grid',
                        ),
                        # absolute and relative graph checkbox
                        graph_card(
                            'Models performance',
                            IdHolder.models_performance_graph.name,
                        ),
                    ],
                    className='grid-column',
                ),
                html.Div(
                    children=[
                        graph_card(
                            'Prediction probability histogram',
                            IdHolder.predict_proba_graph.name,
                        ),
                        graph_card(
                            'TPR and FPR over thresholds',
                            IdHolder.tpr_fpr_graph.name,
                        ),
                    ],
                    className='grid-column',
                ),
                html.Div(
                    children=[
                        graph_card(
                            'ROC AUC Curve',
                            IdHolder.roc_auc_graph.name,
                        ),
                        graph_card(
                            'Precision-Recall Curve',
                            IdHolder.precision_recall_graph.name,
                        ),
                    ],
                    className='grid-column',
                ),
                html.Div(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4(
                                        children=[
                                            html.Span(
                                                'Confusion Matrix',
                                                id=IdHolder.confusion_title.name,
                                            ),
                                            dbc.Checklist(
                                                options=[
                                                    {'value': 1},
                                                ],
                                                value=[1],
                                                id=IdHolder.confusion_switch.name,
                                                switch=True,
                                            ),
                                        ],
                                        className='card-title',
                                    ),
                                    dbc.Spinner(
                                        dcc.Graph(
                                            id=IdHolder.confusion_matrix_graph.name,
                                            config={'displayModeBar': False},
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        graph_card(
                            'Correlation Matrix',
                            IdHolder.correlation_matrix_graph.name,
                            config={'displayModeBar': False},
                        ),
                    ],
                    className='grid-column',
                ),
                html.Div(
                    children=[
                        graph_card(
                            'Feature Importance',
                            IdHolder.feature_importance_graph.name,
                            config={'displayModeBar': False},
                        ),
                        graph_card(
                            'Loss',
                            IdHolder.loss_graph.name,
                        ),
                    ],
                    className='grid-column',
                ),
            ],
            className='main-grid',
        ),
    ],
    className='main-container',
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = layout
