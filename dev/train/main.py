from db import write
from metrics import calculate_metrics
from train import train


def main():
    print('train')
    pipeline, feature_importance, corr, y_test, pred_proba = train()

    print('calculate_metrics')
    metrics = calculate_metrics(y_test, pred_proba)

    print('write')
    write(
        pipeline=pipeline,
        metrics=metrics + [feature_importance, corr],
        train=(y_test, pred_proba[:, 1]),
    )


if __name__ == '__main__':
    main()
