from db import write
from metrics import calculate_metrics
from train import get_pipeline


def main():
    pipeline = get_pipeline()
    metrics = calculate_metrics(pipeline)
    write(
        pipeline=pipeline,
        metrics=metrics,
    )


if __name__ == '__main__':
    main()
