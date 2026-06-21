
import pandas as pd
from src.schema import UNIFIED_COLUMNS


def normalize_csv_cdr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize CSV CDR dataset into unified schema.
    """

    normalized = pd.DataFrame()

    # Timestamps
    normalized["event_datetime"] = pd.to_datetime(
        df["start_time"], errors="coerce", dayfirst=True
    )
    normalized["end_datetime"] = pd.to_datetime(
        df["end_time"], errors="coerce", dayfirst=True
    )

    # Parties
    normalized["a_party"] = df["a_number"]
    normalized["b_party"] = df["b_number"]

    # Event metadata
    normalized["event_type"] = df["type"].str.upper()
    normalized["direction"] = df["direction"].str.upper()

    # Duration
    normalized["duration_minutes"] = pd.to_numeric(
        df["duration"], errors="coerce"
    )

    # Device identifiers |force string safety|
    normalized["imei"] = df["imei"].astype(str)
    normalized["imsi"] = df["imsi"].astype(str)

    # Network & location
    normalized["service_provider"] = df["service_provider"].str.upper()
    normalized["cell_id"] = df["cell_id"]
    normalized["cell_sector"] = df.get("cell_sector")

    normalized["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    normalized["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    normalized["location_text"] = df["location"]

    # Source
    normalized["source_file"] = df["source_file"]

    # Ensure schema consistency
    normalized = normalized.reindex(columns=UNIFIED_COLUMNS)

    # Deduplicate
    normalized = normalized.drop_duplicates(
        subset=[
            "event_datetime",
            "a_party",
            "b_party",
            "event_type",
            "direction",
        ]
    )

    return normalized
def normalize_excel1_cdr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Excel Dataset 1 (intelligence / target-centric dataset)
    into unified CDR schema.
    """

    normalized = pd.DataFrame()

    # Timestamp (best available)
    normalized["event_datetime"] = pd.to_datetime(
        df.get("date_time") or df.get("datetime"),
        errors="coerce"
    )
    normalized["end_datetime"] = None

    # Parties (target is usually embedded here)
    normalized["a_party"] = df.get("a_party")
    normalized["b_party"] = df.get("b_party")

    # Event metadata
    normalized["event_type"] = df.get("event_type", "UNKNOWN")
    normalized["direction"] = df.get("direction")

    # Duration
    normalized["duration_minutes"] = pd.to_numeric(
        df.get("duration"), errors="coerce"
    )

    # Device identifiers
    normalized["imei"] = df.get("imei").astype(str) if "imei" in df else None
    normalized["imsi"] = df.get("imsi").astype(str) if "imsi" in df else None

    # Network & location
    normalized["service_provider"] = df.get("service_provider")
    normalized["cell_id"] = df.get("cell_id")
    normalized["cell_sector"] = df.get("cell_sector")

    normalized["latitude"] = pd.to_numeric(
        df.get("latitude"), errors="coerce"
    )
    normalized["longitude"] = pd.to_numeric(
        df.get("longitude"), errors="coerce"
    )

    normalized["location_text"] = df.get("location")

    # Source tracking
    normalized["source_file"] = df.get("source_file")

    # Enforce unified schema
    normalized = normalized.reindex(columns=UNIFIED_COLUMNS)

    # Drop empty intelligence rows
    normalized = normalized.dropna(
        subset=["event_datetime", "a_party", "b_party"], how="all"
    )

    return normalized

#code for second dataset
def normalize_excel2_cdr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Excel Dataset 2 into unified CDR schema.
    """

    normalized = pd.DataFrame()

    # Timestamp
    normalized["event_datetime"] = pd.to_datetime(
        df["date_&_time"], errors="coerce"
    )
    normalized["end_datetime"] = None

    # Parties
    normalized["a_party"] = df["a_party"]
    normalized["b_party"] = df["b_party"]

    # Event type & direction
    normalized["event_type"] = df["call_type"].str.upper()
    normalized["direction"] = None

    # Duration
    normalized["duration_minutes"] = pd.to_numeric(
        df["duration"], errors="coerce"
    )

    # Device info
    normalized["imei"] = df["imei"].astype(str)
    normalized["imsi"] = df["imsi"].astype(str)

    # Network & location
    normalized["service_provider"] = None
    normalized["cell_id"] = df["cell_id"]
    normalized["cell_sector"] = None

    #  Safe latitude / longitude parsing
    if "longitude_and_latitude" in df.columns:
        lat_long = df["longitude_and_latitude"].astype(str).str.split(",", expand=True)

        # Latitude always comes from column 0
        normalized["latitude"] = pd.to_numeric(
            lat_long.iloc[:, 0], errors="coerce"
        )

        # Longitude ONLY if it exists
        if lat_long.shape[1] > 1:
            normalized["longitude"] = pd.to_numeric(
                lat_long.iloc[:, 1], errors="coerce"
            )
        else:
            normalized["longitude"] = None
    else:
        normalized["latitude"] = None
        normalized["longitude"] = None

    normalized["location_text"] = df.get("site")

    # Source
    normalized["source_file"] = df["source_file"]

    # Enforce schema
    normalized = normalized.reindex(columns=UNIFIED_COLUMNS)

    # Remove empty rows
    normalized = normalized.dropna(
        subset=["event_datetime", "a_party", "b_party"], how="all"
    )

    return normalized


#code for third dataset
def extract_target_msisdn(df: pd.DataFrame) -> str | None:
    """
    Robust extraction of target MSISDN from intelligence Excel file.
    Scans all cells for phone-number-like values.
    """

    for col in df.columns:
        series = df[col].dropna().astype(str)

        for value in series:
            value_clean = value.strip()

            # Basic MSISDN heuristic
            if value_clean.isdigit() and 8 <= len(value_clean) <= 15:
                return value_clean

    return None

