#test 1
from src.ingestion import load_file
from src.utils import normalize_column_names, drop_unnamed_columns

df_csv = load_file("data/raw/anonymized_923310461577.csv")
df_csv = normalize_column_names(df_csv)

df_excel2 = load_file("data/raw/anonymized_923034167919.xlsx")
df_excel2 = drop_unnamed_columns(df_excel2)
df_excel2 = normalize_column_names(df_excel2)

print(df_csv.head())
print(df_excel2.head())
#test 2
from src.ingestion import load_file
from src.utils import normalize_column_names
from src.cleaning import normalize_csv_cdr

df_csv = load_file("data/raw/anonymized_923310461577.csv")
df_csv = normalize_column_names(df_csv)

cdr_csv = normalize_csv_cdr(df_csv)

print(cdr_csv.head())
print(cdr_csv.info())

# test 3
from src.ingestion import load_file
from src.utils import normalize_column_names, drop_unnamed_columns
from src.cleaning import normalize_excel2_cdr

df_excel2 = load_file("data/raw/anonymized_923034167919.xlsx")
df_excel2 = drop_unnamed_columns(df_excel2)
df_excel2 = normalize_column_names(df_excel2)

cdr_excel2 = normalize_excel2_cdr(df_excel2)

print(cdr_excel2.head())
print(cdr_excel2.info())

# for third
# Excel Dataset 1 (Target Intelligence)


from src.ingestion import load_file
from src.cleaning import extract_target_msisdn
from src.utils import normalize_column_names

df_excel1 = load_file("data/raw/anonymized_3142281048_1001725.xlsx")
df_excel1 = normalize_column_names(df_excel1)

target_msisdn = extract_target_msisdn(df_excel1)
print("Target MSISDN:", target_msisdn)
# print(df_excel1.columns.tolist())

if target_msisdn is None:
    raise ValueError("Target MSISDN could not be extracted")

print(f"✔ Target MSISDN identified: {target_msisdn}")

# test enrichment

from src.cleaning import (
    normalize_excel1_cdr,
    normalize_excel2_cdr,
    normalize_csv_cdr,
    extract_target_msisdn
)


from src.enrichment import tag_target_party
from src.ingestion import load_file
from src.utils import normalize_column_names
import pandas as pd


# Load raw datasets

df_excel1 = load_file("data/raw/anonymized_3142281048_1001725.xlsx")
df_excel2 = load_file("data/raw/anonymized_923034167919.xlsx")
df_csv = load_file("data/raw/anonymized_923310461577.csv")

df_excel1 = normalize_column_names(df_excel1)
df_excel2 = normalize_column_names(df_excel2)
df_csv = normalize_column_names(df_csv)


# Extract target MSISDN

target_msisdn = extract_target_msisdn(df_excel1)

if target_msisdn is None:
    raise ValueError("Target MSISDN could not be extracted")

print(f"✔ Target MSISDN identified: {target_msisdn}")


# Normalize datasets

cdr_excel1 = normalize_excel1_cdr(df_excel1)
cdr_excel2 = normalize_excel2_cdr(df_excel2)
cdr_csv = normalize_csv_cdr(df_csv)


# Create master dataset

frames = [
    df for df in [cdr_excel1, cdr_excel2, cdr_csv]
    if df is not None and not df.empty
]

cdr_all = pd.concat(frames, ignore_index=True)


print("✔ Unified CDR created:", cdr_all.shape)


# Enrich with target roles

cdr_all = tag_target_party(cdr_all, target_msisdn)

print("✔ Target tagging completed")



#  Top contacts target-centric model

# Ensure string consistency
cdr_all["a_party"] = cdr_all["a_party"].astype(str)
cdr_all["b_party"] = cdr_all["b_party"].astype(str)

# Combine all contacted numbers
contacts = pd.concat(
    [
        cdr_all["a_party"],
        cdr_all["b_party"]
    ],
    ignore_index=True
)

# Remove empty / invalid values
contacts = contacts[contacts.notna() & (contacts != "")]

# Step 11.2: Call vs SMS Distribution

event_dist = (
    cdr_all["event_type"]
    .value_counts()
)

print("\n📊 Event Type Distribution:")
print(event_dist)


# Direction analysis


direction_dist = (
    cdr_all["direction"]
    .value_counts()
)

print("\n🔁 Direction Distribution:")
print(direction_dist)

#  Hourly activity pattern


cdr_all["hour"] = cdr_all["event_datetime"].dt.hour

hourly_activity = (
    cdr_all["hour"]
    .value_counts()
    .sort_index()
)

print("\n Hourly Activity:")
print(hourly_activity)

# Top 10 most frequent contacts
top_contacts = contacts.value_counts().head(10)

print("\n Top 10 Contacts:")
print(top_contacts)
from src.enrichment import tag_target_party

cdr_all = tag_target_party(cdr_all, target_msisdn)

cdr_all.to_csv("data/processed/unified_cdr.csv", index=False)

cdr_all.to_csv("data/processed/unified_cdr.csv", index=False)
top_contacts.to_csv("data/processed/top_contacts.csv")
hourly_activity.to_csv("data/processed/hourly_activity.csv")
event_dist.to_csv("data/processed/event_distribution.csv")
