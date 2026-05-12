# Person Disambiguation Lab

A small experimental Python repo for exploring large-scale person / patient identity resolution using a union-find algorithm.

The goal of this project is to understand how to take a bridge table of linked identifiers and turn it into connected person groups (master person identifiers).

This repo is intentionally designed as an experimentation sandbox:
- understand graph connectivity
- benchmark scaling
- measure memory usage
- compare approaches
- separate algorithm behaviour from platform behaviour

---

# Problem

Input bridge table:

| patient_id_1 | patient_id_1_type | patient_id_2 | patient_id_2_type |
|---|---|---|---|
| 1001 | database_a | ABC123 | database_b |
| ABC123 | database_b | 9999999999 | database_c |

This means:

```text
database_a|1001 is linked to database_b|ABC123
database_b|ABC123 is linked to database_c|9999999999
```

Therefore all three identifiers belong to the same real-world person.

The challenge is:
- bridge tables can become extremely large
- recursive SQL approaches may run out of memory
- graph traversal can explode computationally

This repo explores whether union-find / disjoint set approaches behave better.

---

# Repo Structure

```text
person-disambiguation-lab/
│
├── data/
│
├── src/
│   ├── union_find.py
│   ├── data_generation.py
│   ├── person_disambiguation.py
│   └── main.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Concepts

## `union_find.py`

Low-level reusable union-find / disjoint-set data structure.

Responsible for:
- `find()`
- `union()`
- parent tracking
- path compression

This is the algorithm itself.

---

## `person_disambiguation.py`

Applies union-find to a bridge table.

Responsible for:
- building connected components
- grouping identifiers into person clusters
- generating master person IDs
- converting graph structures into tabular outputs

This is the domain/business layer.

---

## `data_generation.py`

Generates synthetic bridge tables for testing and benchmarking.

Useful for:
- scaling tests
- memory profiling
- experimentation
- avoiding real patient data

---

## `main.py`

CLI entry point.

Responsible for:
- generating synthetic datasets
- running person disambiguation
- benchmarking runtime
- measuring memory usage
- writing parquet outputs

---

# Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If dependencies are not yet saved:

```bash
pip install pandas pyarrow tqdm psutil
pip freeze > requirements.txt
```

---

# Why Parquet Instead of CSV?

Parquet is:
- columnar
- compressed
- typed
- significantly more efficient than CSV

CSV forces:
- text serialization
- string parsing
- large disk usage

Parquet is much closer to real data engineering workflows.

---

# Usage

This repo separates the workflow into two independent stages:

```text
1. Generate bridge data
2. Run person disambiguation on an existing bridge table
```

This mirrors the real-world problem more closely.

---

# 1. Generate Synthetic Bridge Data

Example:

```bash
python src/main.py generate \
    --people 25000 \
    --ids-per-person 5 \
    --output data/bridge.parquet
```

This creates:

```text
data/bridge.parquet
```

Approximate bridge row count:

```text
people × (ids_per_person - 1)
```

Example:

```text
25,000 people × 4 edges
≈ 100,000 bridge rows
```

---

# 2. Run Person Disambiguation

```bash
python src/main.py map \
    --input data/bridge.parquet \
    --output data/person_mapping.parquet
```

This:
- loads the bridge table
- builds connected components
- generates master person IDs
- writes output parquet

---

# Example Output

```text
MAPPING COMPLETE

Input file: data/bridge.parquet
Output file: data/person_mapping.parquet

Bridge rows read: 100,000
Output mapping rows: 125,000
Unique nodes: 125,000
Connected groups: 25,000

TIMING

Load seconds: 0.42
Mapping seconds: 1.89
Total runtime seconds: 2.41

MEMORY

Memory after load MB: 110.50
Memory end MB: 205.30
Memory increase MB: 125.40
```

---

# Output Structure

Example output mapping:

| master_person_id | patient_id | patient_id_type | ids_per_person |
|---|---|---|---|
| a7f2c1d9... | 1001 | database_a | 5 |
| a7f2c1d9... | ABC123 | database_b | 5 |
| a7f2c1d9... | 9999999999 | database_c | 5 |

Each connected identifier cluster becomes a single master person.

---

# How Master Person IDs Work

Internally the graph uses nodes like:

```text
database_a|1001
```

However the final output generates hashed master person IDs:

```text
md5(root_node)
```

This separates:
- graph representation
- canonical person identifiers

---

# Why Union-Find?

Recursive SQL graph traversal can:
- generate massive intermediate datasets
- repeatedly traverse paths
- spill to disk
- run out of warehouse memory

Union-find instead:
- processes one edge at a time
- merges groups incrementally
- avoids repeated graph traversal

Conceptually:

```text
If two IDs are connected,
put them into the same bucket.
```

---

# Scaling Experiments

Example small test:

```bash
python src/main.py generate \
    --people 1000 \
    --ids-per-person 5 \
    --output data/bridge_1k.parquet

python src/main.py map \
    --input data/bridge_1k.parquet \
    --output data/output_1k.parquet
```

Approx 100k rows:

```bash
python src/main.py generate \
    --people 25000 \
    --ids-per-person 5 \
    --output data/bridge_100k.parquet
```

Approx 1M rows:

```bash
python src/main.py generate \
    --people 250000 \
    --ids-per-person 5 \
    --output data/bridge_1m.parquet
```

---

# Things This Repo Helps Explore

- graph connectivity
- connected components
- union-find performance
- runtime scaling
- memory scaling
- parquet vs CSV
- Python object overhead
- large bridge table behaviour

---

# Important Notes

This repo is for:
- experimentation
- understanding
- benchmarking
- algorithm exploration

The `data/` folder should only contain synthetic or safe test datasets.

---
