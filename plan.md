# FlowLens: IT Incident Process Mining & Optimization

## Project Objective
Transform the academic cloned notebook into an industry-grade, business-driven Data Analytics portfolio project that identifies IT service bottlenecks, tracks SLA compliance, and uncovers ticket "ping-pong" loops using the full 114k+ incident dataset.

## Target Directory Structure

The repository will be reorganized as follows:

```text
flowlens-process-mining/
├── data/
│   ├── raw/                 # Will contain AnonymizedEventData.csv (114k rows)
│   └── processed/           # Will contain cleaned & engineered datasets
├── notebooks/
│   ├── 01_data_cleaning_and_kpis.ipynb    # New: Data cleaning, MTTR, SLA Breach analysis
│   ├── 02_process_discovery.ipynb         # New: DFG maps, Happy Path, Ping-Pong analysis
│   └── Process mining_simplified_py.ipynb # Old: Will be kept temporarily for reference, then deleted
├── src/                     
│   └── data_preprocessing.py # New: Modular Python script to clean the data cleanly
├── dashboard/
│   └── app.py               # New: Streamlit interactive web dashboard
├── requirements.txt         # (Already created)
└── README.md                # To be completely rewritten with Business KPIs and STAR format metrics
```

## Step-by-Step Implementation Plan

### Phase 1: Data Engineering & Scaling
* **Files Affected**: Create `src/data_preprocessing.py` and `notebooks/01_data_cleaning_and_kpis.ipynb`
* **Changes**: 
  - Move away from the 990-row simple CSV and load `AnonymizedEventData.csv` (114,807 rows).
  - Parse `Time` strings into accurate datetime objects.
  - Map complex ITIL statuses into cleaner categories (e.g., group all alerts together).
  - Engineer new features: `Resolution_Time_Hours`, `Reassignment_Count`, `Is_SLA_Breached`.

### Phase 2: Business KPI Analytics
* **Files Affected**: `notebooks/01_data_cleaning_and_kpis.ipynb`
* **Changes**:
  - Calculate Data Analyst metrics that businesses care about.
  - Analyze MTTR (Mean Time to Resolution) overall and per `GroupName`.
  - Calculate SLA breach rates (assuming a standard 24h or 48h SLA).
  - Quantify the "Ping-Pong Effect" (how much time is wasted when tickets bounce between teams).

### Phase 3: Advanced Process Mining
* **Files Affected**: Create `notebooks/02_process_discovery.ipynb`
* **Changes**:
  - Re-implement PM4Py models on the full dataset with a business lens.
  - Filter out "Happy Path" vs "Deviant Path" tickets.
  - Generate clean Directly Follows Graphs (DFG) showing performance bottlenecks (time delays between specific statuses like `pending vendor` and `analysis`).

### Phase 4: Interactive Dashboard Delivery
* **Files Affected**: Create `dashboard/app.py`
* **Changes**: 
  - Build a professional presentation layer.
  - Create a Streamlit web app where users (or recruiters) can filter by support group and instantly see the bottleneck graph and MTTR metrics interactively.

### Phase 5: Documentation Polish
* **Files Affected**: Overwrite `README.md`
* **Changes**:
  - Include an Executive Summary, Tech Stack, Key Findings (with numbers!), and the exact STAR format Resume Bullet points.
