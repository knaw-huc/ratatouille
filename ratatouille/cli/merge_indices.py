#!/usr/bin/env python3
import argparse
import sys

from loguru import logger

from ratatouille.index_merger import IndexMerger
from ratatouille.index_merger_config import IndexMergerConfig

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    colorize=True,
)


def main():
    parser = argparse.ArgumentParser(
        description="Merge Elastic indices of multiple collections into a single index"
    )
    parser.add_argument(
        "-c", "--config", help="Path to the configuration file", required=True, type=str
    )
    parser.add_argument("-f", "--logfile", help="Path to the log file", type=str)
    parser.add_argument(
        "-p", "--progress", help="Show progress information", action="store_true"
    )
    args = parser.parse_args()

    cf = IndexMergerConfig(
        collections_path=args.config,
        show_progress=args.progress,
        log_file_path=args.logfile,
    )
    warnings = IndexMerger(cf).merge()
    if warnings:
        for error in warnings:
            logger.warning(error)


if __name__ == "__main__":
    main()
