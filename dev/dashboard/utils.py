import numpy as np
import pandas as pd
import plotly.graph_objects as go
from AppData import app_data
from plotly.subplots import make_subplots


def get_metrics():
    return [
        f'{app_data.tnr*100:.0f}%',
        f'{app_data.fpr*100:.0f}%',
        f'{app_data.fdr*100:.0f}%',
        f'{app_data.fnr*100:.0f}%',
        f'{app_data.tpr*100:.0f}%',
        f'{app_data.npv*100:.0f}%',
        f'{app_data.roc_auc*100:.0f}%',
        f'{app_data.f1_beta*100:.0f}%',
        f'{app_data.ppv*100:.0f}%',
    ]


def plot_models_performance():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=app_data.roc_auc_scores,
            x=app_data.model_ids,
            line=dict(width=3),
            mode='lines+markers',
            marker=dict(size=10),
        ),
    )

    fig.update_xaxes(title='<b>Model</b>')
    fig.update_yaxes(title='<b>ROC AUC</b>')

    fig.update_layout(
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        hovermode='x unified',
        margin=dict(l=0, r=0, t=15, b=60),
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
    )

    return fig


def plot_predict_proba():
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=app_data.predict_proba,
            xbins=dict(
                start=0,
                end=1,
                size=0.01,
            ),
        ),
    )

    fig.update_xaxes(range=[0, 1], title='<b>Threshold</b>')
    fig.update_yaxes(title='<b>Count</b>')
    fig.update_layout(
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        hovermode='x unified',
        margin=dict(l=0, r=0, t=25, b=0),
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
    )

    return fig


def plot_tpr_fpr():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=app_data.thresholds_roc,
            y=app_data.fpr_arr,
            mode='lines',
            name='False Positive Rate',
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=app_data.thresholds_roc,
            y=app_data.tpr_arr,
            mode='lines',
            name='True Positive Rate',
        ),
    )

    fig.update_xaxes(range=[0, 1], title='<b>Threshold</b>')
    fig.update_yaxes(range=[0, 1.05], title='<b>Rate</b>')
    fig.update_layout(
        margin=dict(l=0, r=25, t=50, b=50),
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='left',
            x=0,
        ),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
    )

    return fig


def plot_roc_auc():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=app_data.fpr_arr,
            y=app_data.tpr_arr,
            fill='tozeroy',
        ),
    )

    fig.add_shape(
        type='line',
        line=dict(
            dash='dash',
            color='rgb(242, 242, 242)',
        ),
        x0=0,
        y0=0,
        x1=1,
        y1=1,
    )

    fig.update_layout(
        xaxis=dict(
            title='<b>False Positive Rate</b>',
            range=[0, 1],
            tickmode='array',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            ticktext=['0', '0.25', '0.5', '0.75', '1'],
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        yaxis=dict(
            title='<b>True Positive Rate</b>',
            range=[0, 1.05],
            tickmode='array',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            ticktext=['0', '0.25', '0.5', '0.75', '1'],
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        margin=dict(l=0, r=0, t=50, b=50),
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        hovermode='x unified',
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
    )

    return fig


def plot_precision_recall():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=app_data.recall_arr,
            y=app_data.precision_arr,
            fill='tozeroy',
        ),
    )

    fig.add_shape(
        type='line',
        line=dict(
            dash='dash',
            color='rgb(242, 242, 242)',
        ),
        x0=0,
        x1=1,
        y0=1,
        y1=0,
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=50),
        xaxis=dict(
            title='<b>Recall</b>',
            range=[0, 1],
            tickmode='array',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            ticktext=['0', '0.25', '0.5', '0.75', '1'],
            constrain='domain',
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        yaxis=dict(
            title='<b>Precision</b>',
            range=[0, 1.05],
            tickmode='array',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            ticktext=['0', '0.25', '0.5', '0.75', '1'],
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        hovermode='x unified',
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
    )

    return fig


def plot_confusion_matrix(type=False):
    tn, fp, fn, tp = app_data.tn, app_data.fp, app_data.fn, app_data.tp

    fig = (
        _sankey(
            [
                [tn, fp],
                [fn, tp],
            ],
        )
        if type
        else _heatmap([[fn, tp], [tn, fp]], 20)
    )

    if not type:
        fig.update_layout(
            xaxis_title='<b>Predicted label</b>',
            yaxis_title='<b>True label</b>',
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['<b>0</b>', '<b>1</b>'],
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['<b>1</b>', '<b>0</b>'],
            ),
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=50),
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
        xaxis=dict(tickfont=dict(size=14, color='rgb(242, 242, 242)')),
        yaxis=dict(tickfont=dict(size=14, color='rgb(242, 242, 242)')),
    )

    return fig


def plot_corr_matrix():
    fig = _heatmap(np.rot90(app_data.corr.values), 10)

    fig.update_layout(
        width=800,
        height=700,
        xaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(len(app_data.corr.columns))],
            ticktext=app_data.corr.columns.values,
            tickangle=45,
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(len(app_data.corr.columns))],
            ticktext=app_data.corr.columns.values[::-1],
        ),
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
        margin=dict(l=0, r=0, t=50, b=50),
    )

    return fig


def plot_feature_importance():
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    fig.add_trace(
        go.Bar(
            x=[0.87 for i in app_data.feature_importance.importance],
            y=app_data.feature_importance.index,
            orientation='h',
            width=0.01,
        ),
    )

    fig.add_trace(
        go.Bar(
            x=app_data.feature_importance.importance,
            y=app_data.feature_importance.index,
            orientation='h',
            name='Feature importance',
            text=[f'<b>{i*100:.2f}%</b>' for i in app_data.feature_importance.importance],
            hovertemplate='<i>%{y}</i> importance: <b>%{text}</b><extra></extra>',
            textposition='none',
            hoverlabel=dict(
                font=dict(
                    size=16,
                    family='Inter',
                ),
            ),
            marker_color='#636EFA',
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(
            x=[1 for i in app_data.feature_importance.importance],
            y=app_data.feature_importance.index,
            orientation='h',
            marker_color='rgba(0, 0, 0, 0)',
            marker_line=dict(width=0),
            text=[f'<b>{i*100:.2f}%</b>' for i in app_data.feature_importance.importance],
            textfont=dict(
                color='rgb(242, 242, 242)',
                size=14,
                family='Inter',
            ),
            hovertemplate='<i>%{y}</i> importance: <b>%{text}</b><extra></extra>',
            hoverlabel=dict(
                align='left',
                namelength=-1,
                font=dict(
                    size=16,
                    family='Inter',
                ),
            ),
        ),
    )

    fig.update_layout(
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        margin=dict(l=0, r=0, t=25, b=50),
        xaxis=dict(
            title='<b>Importance</b>',
            range=[0, 1],
            showticklabels=False,
            showgrid=False,
        ),
        yaxis=dict(
            title='<b>Feature</b>',
            showgrid=False,
            tickfont=dict(size=14),
            categoryorder='total ascending',
        ),
        showlegend=False,
        height=600,
        dragmode=False,
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
        barmode='overlay',
    )

    return fig


def plot_loss():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[i for i in range(len(app_data.train_loss))],
            y=app_data.train_loss,
            name='Train loss',
            mode='lines',
            line=dict(color='#636EFA'),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=[i for i in range(len(app_data.val_loss))],
            y=app_data.val_loss,
            name='Validation loss',
            mode='lines',
            line=dict(color='#EF553B'),
        ),
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=75),
        xaxis=dict(
            title='<b>Iteration</b>',
            constrain='domain',
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        yaxis=dict(
            title='<b>Loss</b>',
            showline=True,
            linewidth=1,
            linecolor='rgb(242, 242, 242)',
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='left',
            x=0,
        ),
        height=600,
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        hovermode='x unified',
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
    )

    return fig


def _heatmap(cm, font_size):
    fig = go.Figure(
        data=go.Heatmap(
            z=cm,
            text=[np.round(i, 2) for i in cm],
            texttemplate='<b>%{text}</b>',
            textfont={'size': font_size},
            colorscale='RdBu',
        ),
    )

    fig.update_layout(
        width=700,
        height=600,
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
    )

    return fig


# TODO: refactor
def _sankey(cm):
    df = (
        pd.DataFrame(
            data=cm,
            index=[f"Actual {'Negative' if i ==0 else 'Positive'}" for i in range(len(cm))],
            columns=[f"Predicted {'Negative' if i ==0 else 'Positive'}" for i in range(len(cm))],
        )
        .stack()
        .reset_index()
        .rename(
            columns={
                'level_0': 'source',
                'level_1': 'target',
                0: 'value',
            },
        )
        .assign(
            colour=lambda _df: _df.apply(
                lambda x: 'rgba(211,255,216,0.6)'
                if x.source.split()[-1] == x.target.split()[-1]
                else 'rgba(245,173,168,0.6)',
                axis=1,
            ),
        )
    )

    labels = pd.concat([df.source, df.target]).unique()

    labels_indices = {label: index for index, label in enumerate(labels)}

    df[['source', 'target']] = df[['source', 'target']].applymap(
        lambda x: labels_indices[x],
    )

    df['tooltip'] = df.apply(
        lambda x: f"<b>{x['value']}</b> True {labels[x['target']].split()[-1]} instances"
        if x['colour'] == 'rgba(211,255,216,0.6)'
        else f"<b>{x['value']}</b> False {labels[x['source']].split()[-1]} instances",
        axis=1,
    )

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=20,
                    thickness=20,
                    line=dict(color='black', width=1.0),
                    label=labels,
                    hovertemplate='%{label} has total %{value:d} instances<extra></extra>',
                ),
                link=dict(
                    source=df.source,
                    target=df.target,
                    value=df.value,
                    color=df.colour,
                    customdata=df['tooltip'],
                    hovertemplate='%{customdata}<extra></extra>',
                    hoverlabel=dict(
                        font=dict(
                            size=16,
                            color='rgb(242, 242, 242)',
                            family='Inter',
                        ),
                        bgcolor='rgb(48, 48, 48)',
                    ),
                ),
            ),
        ],
    )

    fig.update_layout(
        width=700,
        height=650,
        font_size=16,
        hoverlabel=dict(
            font_size=16,
        ),
        paper_bgcolor='rgb(48, 48, 48)',
        plot_bgcolor='rgb(48, 48, 48)',
        font=dict(color='rgb(242, 242, 242)', family='Inter'),
    )

    return fig
