#! /usr/bin/env python3

import argparse
import sys

from elasticsearch8 import Elasticsearch
from elasticsearch8.exceptions import NotFoundError, ConnectionError
from loguru import logger

# 1. Setup Loguru Configuration
# Loguru comes with a default handler. We can customize it easily.
logger.remove()  # Remove default handler to apply our custom format
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    colorize=True
)


def get_index_mapping(hostname, port, index_name):
    """
    Fetches the mapping for a specific Elasticsearch index.
    """
    # Initialize the client
    # Note: For ES 8.x+, use 'https' if security is enabled
    es = Elasticsearch([f"http://{hostname}:{port}"])

    try:
        # Fetch the mapping
        response = es.indices.get_mapping(index=index_name)
        mapping = response[index_name]['mappings']
        logger.info(f"Successfully retrieved: {index_name}")
        return mapping

    except NotFoundError:
        logger.error(f"Error: Index '{index_name}' not found.")
    except ConnectionError:
        logger.critical(f"Error: Could not connect to Elasticsearch at {hostname}:{port}.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

    return None


def main():
    parser = argparse.ArgumentParser(description='Merge multiple Elastic indices to a unified index')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    args = parser.parse_args()

    if args.quiet:
        verbosity = -1
    elif args.verbose:
        verbosity = 1
    else:
        verbosity = 0

    print(f'Verbosity: {verbosity}')

    mapping = get_index_mapping('localhost', 9202, 'israels')
    print(mapping)


if __name__ == '__main__':
    main()
