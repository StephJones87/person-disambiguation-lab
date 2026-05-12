from tqdm import tqdm
import pandas as pd


def build_edges(number_of_people: int, ids_per_person: int) -> pd.DataFrame:
    systems = [
        "database_a",
        "database_b",
        "database_c",
        "database_d",
        "database_e",
        "database_f",
        "database_g",
    ]

    rows = []

    for person_number in range(number_of_people):
        identifiers = []

        for identifier_number in range(ids_per_person):
            system_name = systems[identifier_number % len(systems)]
            patient_id = f"{system_name}_{person_number}"

            identifiers.append((patient_id, system_name))

        for left, right in zip(identifiers, identifiers[1:]):
            rows.append(
                {
                    "patient_id_1": left[0],
                    "patient_id_1_type": left[1],
                    "patient_id_2": right[0],
                    "patient_id_2_type": right[1],
                }
            )

    return pd.DataFrame(rows)