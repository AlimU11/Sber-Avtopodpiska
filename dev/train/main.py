from argparse import ArgumentParser

from db import write
from loguru import logger
from metrics import calculate_metrics
from train import train


def parse():
    parser = ArgumentParser()
    parser.add_argument(
        '--config',
        type=str,
        required=False,
        help='Path to hyperparameters config. If not specified, will tune '
        'hyperparameters and write to file `model_config.json` in the same directory',
    )

    parser.add_argument(
        '--model',
        type=str,
        required=False,
        default='XGBoost',
        help='Model to use. Ignored, if config specified. Only models defined in `Objectives` class are supported. '
        'Default: XGBoost',
    )

    parser.add_argument(
        '--resampler',
        type=str,
        required=False,
        default='LVQ_SMOTE',
        help='Disabled. \n Resampler to use. Ignored, if config specified. Only resamplers implemented in smote-variants are supported. '
        'Default: LVQ_SMOTE',
    )

    return parser.parse_args()


def main():
    logger.info('Initiating training...')

    args = parse()

    logger.info('Training with args: {}', args)
    logger.info(
        'Resampler from both config and arguments is ignored. To use resampler, manually change the code in train.py (lines 210-211)',
    )

    pipeline, feature_importance, corr, evals_result, y_test, pred_proba = train(args, logger)

    logger.info('Training finished. Calculating metrics...')

    metrics = calculate_metrics(y_test, pred_proba)

    logger.info('Saving results to database...')

    write(
        pipeline=pipeline,
        metrics=metrics + [feature_importance, corr, evals_result],
        train=(y_test, pred_proba[:, 1]),
    )


if __name__ == '__main__':
    main()
