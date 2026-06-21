📡 CDR Investigation & Analytics Dashboard
📌 Project Overview

This project performs end-to-end analysis of Call Detail Records (CDR) collected from multiple heterogeneous sources (Excel and CSV).
The system normalizes, enriches, and analyzes telecom activity to support investigative and intelligence-driven use cases, and presents insights through an interactive Streamlit dashboard.

The workflow follows a professional data-engineering and analytics pipeline, from raw ingestion to visualization.

🎯 Objectives

Normalize multiple CDR formats into a unified schema

Identify and tag a target MSISDN

Perform behavioral and communication analysis

Generate analytical metrics (contacts, activity patterns, distributions)

Present results through an interactive dashboard

🗂️ Project Structure
cdr_dashboard/
│
├── data/
│   ├── raw/                # Original anonymized datasets (Excel / CSV)
│   └── processed/          # Cleaned & unified datasets
│
├── src/
│   ├── ingestion.py        # Data loading utilities
│   ├── cleaning.py         # Normalization & extraction logic
│   ├── enrichment.py       # Target tagging & role enrichment
│   └── utils.py            # Helper functions
│
├── app.py                  # Streamlit dashboard application
├── test-script.py          # Main pipeline execution script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

📥 Data Sources

The project uses three anonymized datasets:

Excel Dataset 1

Contains target intelligence

Used to extract the target MSISDN

Excel Dataset 2

Telecom activity records

Requires structural normalization

CSV Dataset

Event-based CDR records

Includes calls, SMS, timestamps, and directions

⚙️ Processing Pipeline
1️⃣ Data Ingestion

Files loaded using a unified loader

Column names normalized for consistency

Empty / unnamed columns removed

2️⃣ Data Normalization

All datasets are transformed into a common CDR schema, including:

event_datetime

a_party

b_party

event_type

direction

duration

location (if available)

3️⃣ Target Extraction

The target MSISDN is automatically extracted from Dataset 1

Validated before further processing

4️⃣ Data Enrichment

Records are enriched with:

a_party_role (TARGET / OTHER)

b_party_role (TARGET / OTHER)

5️⃣ Dataset Unification

All normalized datasets are concatenated into:

data/processed/unified_cdr.csv

📊 Analytical Features

The system computes:

📞 Top 10 Contacts

📊 Event Type Distribution

🔁 Direction Distribution

⏰ Hourly Activity Pattern

📌 Key Metrics (KPIs)

All analysis is data-driven and adapts automatically if the target is not present.

🖥️ Interactive Dashboard (Streamlit)

The Streamlit UI provides:

Sidebar filters (Event Type, Direction)

KPI cards (Total events, contacts, date range)

Bar charts for distributions

Target-centric contact analysis

Automatic fallback to global analysis if target is absent

Raw data preview

CSV export functionality

▶️ Run Dashboard
streamlit run app.py

🚀 How to Run the Project
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run Processing Pipeline
python test-script.py


This will generate:

unified_cdr.csv

analytical outputs in data/processed/

3️⃣ Launch Dashboard
streamlit run app.py

🧠 Design Philosophy

Modular & reusable code

Defensive programming (handles missing target cases)

Professional investigative workflow

Separation of concerns (ingestion, cleaning, enrichment, UI)

Transparent analytical assumptions

📌 Key Takeaway

This project demonstrates how raw telecom data can be transformed into structured intelligence using modern data engineering practices and interactive analytics.

✅ Status

✔ Data ingestion complete
✔ Normalization complete
✔ Target extraction & tagging complete
✔ Analysis complete
✔ Dashboard complete
