import pandas as pd

df = pd.read_parquet("data/person_mapping.parquet")
print(df.head(200))