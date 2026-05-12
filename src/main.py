import argparse
import os
import time

import pandas as pd
import psutil

from data_generation import build_edges
from person_disambiguation import (
    build_person_disambiguation, 
    person_disambiguation_to_dataframe,
)


def get_memory_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def generate_data(args):
    start_time = time.time()
    memory_start = get_memory_mb()

    edges = build_edges(
        number_of_people=args.people,
        ids_per_person=args.ids_per_person,
    )

    edges.to_parquet(args.output, index=False)

    end_time = time.time()
    memory_end = get_memory_mb()

    print("\nGENERATION COMPLETE\n")
    print(f"People generated: {args.people:,}")
    print(f"IDs per person: {args.ids_per_person:,}")
    print(f"Bridge rows generated: {len(edges):,}")
    print(f"Output file: {args.output}")
    print(f"Runtime seconds: {end_time - start_time:.2f}")
    print(f"Memory increase MB: {memory_end - memory_start:.2f}")


def map_existing_data(args):
    start_time = time.time()
    memory_start = get_memory_mb()

    load_start = time.time()
    edges = pd.read_parquet(args.input)
    load_end = time.time()

    memory_after_load = get_memory_mb()

    mapping_start = time.time()
    union_find, groups = build_person_disambiguation(edges)
    mapping_end = time.time()

    output_df = person_disambiguation_to_dataframe(groups)

    output_df.to_parquet(args.output, index=False)

    end_time = time.time()
    memory_end = get_memory_mb()

    print("\nMAPPING COMPLETE\n")
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print(f"Bridge rows read: {len(edges):,}")
    print(f"Output mapping rows: {len(output_df):,}")
    print(f"Unique nodes: {len(union_find.parent):,}")
    print(f"Connected groups: {len(groups):,}")

    print("\nTIMING\n")
    print(f"Load seconds: {load_end - load_start:.2f}")
    print(f"Mapping seconds: {mapping_end - mapping_start:.2f}")
    print(f"Total runtime seconds: {end_time - start_time:.2f}")

    print("\nMEMORY\n")
    print(f"Memory after load MB: {memory_after_load:.2f}")
    print(f"Memory end MB: {memory_end:.2f}")
    print(f"Memory increase MB: {memory_end - memory_start:.2f}")
    print(f"Memory increase MB: {memory_end - memory_start:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="Person disambiguation lab using union-find."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate synthetic bridge data and save it to CSV.",
    )

    generate_parser.add_argument("--people", type=int, required=True)
    generate_parser.add_argument("--ids-per-person", type=int, required=True)
    generate_parser.add_argument("--output", type=str, required=True)

    map_parser = subparsers.add_parser(
        "map",
        help="Run union-find mapping on an existing CSV bridge table.",
    )

    map_parser.add_argument("--input", type=str, required=True)
    map_parser.add_argument("--output", type=str, required=True)

    args = parser.parse_args()

    if args.command == "generate":
        generate_data(args)

    elif args.command == "map":
        map_existing_data(args)


if __name__ == "__main__":
    main()