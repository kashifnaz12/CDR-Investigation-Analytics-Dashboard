import pandas as pd

def tag_target_party(df: pd.DataFrame, target_msisdn: str) -> pd.DataFrame:
    df = df.copy()

    df["a_party_role"] = df["a_party"].astype(str).apply(
        lambda x: "TARGET" if x == target_msisdn else "OTHER"
    )

    df["b_party_role"] = df["b_party"].astype(str).apply(
        lambda x: "TARGET" if x == target_msisdn else "OTHER"
    )

    return df
