import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# page configuration

st.set_page_config(
    page_title="CDR Investigation Dashboard",
    page_icon="📡",
    layout="wide"
)


# header

st.title("📡 CDR Investigation Dashboard")
st.caption(
    "Unified analysis of Call Detail Records (CDR) for investigative intelligence"
)

st.divider()


# Load processed data
@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/unified_cdr.csv",
        parse_dates=["event_datetime", "end_datetime"]
    )

cdr_all = load_data()


# Sidebar filters

st.sidebar.header("🔍 Filters")

event_types = st.sidebar.multiselect(
    "Event Type",
    options=sorted(cdr_all["event_type"].dropna().unique()),
    default=sorted(cdr_all["event_type"].dropna().unique())
)

directions = st.sidebar.multiselect(
    "Direction",
    options=sorted(cdr_all["direction"].dropna().unique()),
    default=sorted(cdr_all["direction"].dropna().unique())
)

filtered = cdr_all[cdr_all["event_type"].isin(event_types)]

if directions:
    filtered = filtered[
        (filtered["direction"].isin(directions)) |
        (filtered["direction"].isna())
    ]


# KPI section

st.subheader("📌 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Events", f"{len(filtered):,}")

with col2:
    unique_contacts = pd.unique(
        filtered[["a_party", "b_party"]].values.ravel()
    )
    st.metric("Unique Contacts", f"{len(unique_contacts):,}")

with col3:
    st.metric(
        "Start Date",
        filtered["event_datetime"].min().strftime("%Y-%m-%d")
    )

with col4:
    st.metric(
        "End Date",
        filtered["event_datetime"].max().strftime("%Y-%m-%d")
    )

st.divider()

# Charts Row

col_left, col_right = st.columns(2)

# ---- Event Type Distribution
with col_left:
    st.subheader("📊 Event Type Distribution")
    event_dist = filtered["event_type"].value_counts()

    fig, ax = plt.subplots()
    event_dist.plot(kind="bar", ax=ax)
    ax.set_xlabel("Event Type")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Direction Distribution
with col_right:
    st.subheader("🔁 Direction Distribution")
    direction_dist = filtered["direction"].value_counts()

    fig, ax = plt.subplots()
    direction_dist.plot(kind="bar", ax=ax)
    ax.set_xlabel("Direction")
    ax.set_ylabel("Count")
    st.pyplot(fig)

st.divider()


# Hourly activity

st.subheader("⏰ Hourly Activity Pattern")

filtered = filtered.copy()
filtered["hour"] = filtered["event_datetime"].dt.hour
hourly_activity = filtered["hour"].value_counts().sort_index()

fig, ax = plt.subplots()
hourly_activity.plot(kind="bar", ax=ax)
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Number of Events")
st.pyplot(fig)

st.divider()


# Contact analysis

st.subheader("📞 Contact Analysis")

target_mask = (
    (filtered.get("a_party_role") == "TARGET") |
    (filtered.get("b_party_role") == "TARGET")
)

target_df = filtered[target_mask] if "a_party_role" in filtered.columns else pd.DataFrame()

if not target_df.empty:
    st.success("🎯 Target MSISDN activity detected in CDR records.")

    target_df = target_df.copy()
    target_df["contact_number"] = target_df.apply(
        lambda r: r["b_party"]
        if r["a_party_role"] == "TARGET"
        else r["a_party"],
        axis=1
    )

    top_contacts = (
        target_df["contact_number"]
        .value_counts()
        .head(10)
    )

    st.markdown("### 🎯 Top 10 Contacts (Target-Centric)")
    st.dataframe(
        top_contacts.rename("Interactions")
        .reset_index()
        .rename(columns={"index": "Contact Number"}),
        use_container_width=True
    )

else:
    st.warning(
        "Target MSISDN not observed in the available CDR records. "
        "Displaying global contact frequency instead."
    )

    all_contacts = pd.concat(
        [
            filtered["a_party"].astype(str),
            filtered["b_party"].astype(str)
        ],
        ignore_index=True
    )

    all_contacts = all_contacts[
        all_contacts.notna() & (all_contacts != "")
    ]

    top_contacts = all_contacts.value_counts().head(10)

    st.markdown("### 🌐 Top 10 Contacts (Global)")
    st.dataframe(
        top_contacts.rename("Interactions")
        .reset_index()
        .rename(columns={"index": "Contact Number"}),
        use_container_width=True
    )

st.divider()

# Data Preview & Export

with st.expander("📄 Preview Unified CDR Data"):
    st.dataframe(filtered.head(100), use_container_width=True)

# st.download_button(
#     label="⬇️ Download Filtered CDR Data (CSV)",
#     data=filtered.to_csv(index=False),
#     file_name="filtered_cdr_data.csv",
#     mime="text/csv"
# )
