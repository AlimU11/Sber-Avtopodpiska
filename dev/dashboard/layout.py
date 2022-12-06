import dash_bootstrap_components as dbc
from dash import dcc, html
from IdHolder import IdHolder

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(children='Train Results for model'),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem('Model 1'),
                                dbc.DropdownMenuItem('Model 2'),
                                dbc.DropdownMenuItem('Model 3'),
                            ],
                            size='lg',
                            id=IdHolder.model_dropdown.name,
                            label='Model 1',
                            toggle_style={
                                'background': 'white',
                                'color': 'black',
                            },
                        ),
                    ],
                    className='grid-column card',
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5(
                                                'Precision',
                                                className='card-title',
                                            ),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5('TNR', className='card-title'),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5('FPR', className='card-title'),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5('Cohen Kappa', className='card-title'),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5('FNR', className='card-title'),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5('TPR', className='card-title'),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5('ROC AUC', className='card-title'),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5('F1', className='card-title'),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H5(
                                                'Avg. Precision',
                                                className='card-title',
                                            ),
                                            html.P('0%', className='card-text'),
                                        ],
                                    ),
                                ),
                            ],
                            className='metrics-grid',
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    html.H4(
                                        'Models performance',
                                        className='card-title',
                                    ),
                                    dcc.Graph(
                                        id=IdHolder.models_performance_graph.name,
                                    ),
                                ],
                            ),
                        ),
                    ],
                    className='grid-column',
                ),
                html.Div(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4('ROC AUC Curve', className='card-title'),
                                    dcc.Graph(
                                        id=IdHolder.roc_auc_graph.name,
                                    ),
                                ],
                            ),
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4('TPR and FPR over thresholds', className='card-title'),
                                    dcc.Graph(
                                        id=IdHolder.tpr_fpr_graph.name,
                                    ),
                                ],
                            ),
                        ),
                    ],
                    className='grid-column',
                ),
                html.Div(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4('Confusion Matrix', className='card-title'),
                                    dcc.Graph(
                                        id=IdHolder.confusion_matrix_graph.name,
                                    ),
                                ],
                            ),
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4(
                                        'Correlation Matrix',
                                        className='card-title',
                                    ),
                                    dcc.Graph(
                                        id=IdHolder.correlation_matrix_graph.name,
                                    ),
                                ],
                            ),
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
                                        'Feature Importance',
                                        className='card-title',
                                    ),
                                    dcc.Graph(
                                        id=IdHolder.feature_importance_graph.name,
                                    ),
                                ],
                            ),
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4('Partial Dependence', className='card-title'),
                                    dcc.Graph(
                                        id=IdHolder.partial_dependence_graph.name,
                                    ),
                                ],
                            ),
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
