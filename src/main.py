import argparse
import os
import time
from collections import defaultdict

import psutil

from data_generation import build_edges
from union_find import UnionFind


def get_memory_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def run_union_find(edges):
    union_find = UnionFind()

    for row in edges.itertuples(index=False):
        node_1 = f"{row.patient_id_1_type}|{row.patient_id_1}"
        node_2 = f"{row.patient_id_2_type}|{row.patient_id_2}"

        union_find.union(node_1, node_2)

    groups = defaultdict(list)

    for node in union_find.parent:
        root = union_find.find(node)
        groups[root].append(node)

    return union_find, groups


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark union-find for person disambiguation."
    )

    parser.add_argument(
        "--people",
        type=int,
        required=True,
        help="Number of synthetic people to generate.",
    )

    parser.add_argument(
        "--ids-per-person",
        type=int,
        required=True,
        help="Number of identifiers per person.",
    )

    args = parser.parse_args()

    memory_start = get_memory_mb()
    start_time = time.time()

    edges = build_edges(
        number_of_people=args.people,
        ids_per_person=args.ids_per_person,
    )

    memory_after_data = get_memory_mb()

    union_find, groups = run_union_find(edges)

    end_time = time.time()
    memory_end = get_memory_mb()

    print("\nBENCHMARK RESULTS\n")
    print(f"People generated: {args.people:,}")
    print(f"IDs per person: {args.ids_per_person:,}")
    print(f"Bridge rows generated: {len(edges):,}")
    print(f"Unique nodes: {len(union_find.parent):,}")
    print(f"Connected groups: {len(groups):,}")
    print(f"Runtime seconds: {end_time - start_time:.2f}")
    print(f"Memory start MB: {memory_start:.2f}")
    print(f"Memory after data MB: {memory_after_data:.2f}")
    print(f"Memory end MB: {memory_end:.2f}")
    print(f"Approx memory increase MB: {memory_end - memory_start:.2f}")


if __name__ == "__main__":
    main()