from loguru import logger
from train import train


def main():
    logger.info('Initiating training...')

    train(logger)

    logger.info('Training finished.')


if __name__ == '__main__':
    main()
