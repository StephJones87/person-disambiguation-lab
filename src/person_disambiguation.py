from collections import defaultdict

import hashlib
import pandas as pd
from tqdm import tqdm

from union_find import UnionFind


def build_person_disambiguation(edges: pd.DataFrame):
    union_find = UnionFind()

    for row in tqdm(
        edges.itertuples(index=False),
        total=len(edges),
        desc="Building person dismbiguation",
    ):
        node_1 = f"{row.patient_id_1_type}|{row.patient_id_1}"
        node_2 = f"{row.patient_id_2_type}|{row.patient_id_2}"

        union_find.union(node_1, node_2)

    groups = defaultdict(list)

    for node in tqdm(
        union_find.parent,
        desc="Collecting connected groups",
    ):
        root = union_find.find(node)
        groups[root].append(node)

    return union_find, groups


def person_disambiguation_to_dataframe(groups) -> pd.DataFrame:
    rows = []

    for root, members in groups.items():

        master_person_id = hashlib.md5(root.encode()).hexdigest()
        for member in members:
            patient_id_type, patient_id = member.split("|", 1)

            rows.append(
                {
                    "master_person_id": master_person_id,
                    "patient_id": patient_id,
                    "patient_id_type": patient_id_type,
                    "ids_per_person": len(members),
                }
            )

    return pd.DataFrame(rows)