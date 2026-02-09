#!/usr/bin/env python3
from ratatouille.index_merger import IndexMerger
from ratatouille.index_merger_config import IndexMergerConfig


def main():
    cf = IndexMergerConfig(
        source_indices=[
            "http://localhost:9201/brederode",
            "http://localhost:9202/israels",
        ],
        mapping_path="./unified_mapping.json",
        show_progress=True,
        # log_file_path="merge_log.txt",
    )
    errors = IndexMerger(cf).merge()
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
