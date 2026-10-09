# FlowLens: IT Incident Process Mining & Optimization

## 📖 Executive Summary
**FlowLens** is an advanced operational intelligence project that uses **Process Mining** to reconstruct and analyze IT Service Management (ITSM) workflows from raw event logs. By analyzing **114,807 real-world incident events**, this project shifts the focus from simple static reporting to dynamic, sequence-based bottleneck identification.

The goal of this project is to identify where time is wasted, track SLA compliance, and visually map out the inefficiencies in ticket routing (e.g., the "Ping-Pong" effect).

## 🚀 Key Business Findings & KPIs
Using PM4Py and data analytics, we uncovered the following insights from the data:
- **Mean Time to Resolution (MTTR):** Calculated median and 90th percentile resolution times across all support teams, highlighting outliers that took >500 hours to resolve.
- **SLA Breach Tracking:** Identified tickets that breached the standard 72-hour Service Level Agreement, allowing for deep-dive root cause analysis.
- **The "Ping-Pong" Effect:** Quantified internal inefficiency by tracking tickets that were repeatedly flagged as `reassigned-misrouted`. We found a significant subset of tickets experiencing up to 10+ reassignments before resolution.
- **Performance Bottleneck Maps:** Used Directly Follows Graphs (DFG) to visualize exactly where tickets stall (e.g., waiting on third-party vendors or complex internal analysis).

## 🛠 Tech Stack
- **Python 3.11**
- **Data Engineering:** `Pandas`, `NumPy`
- **Process Mining Engine:** `PM4Py`
- **Visualization:** `Streamlit`, `Seaborn`, `Matplotlib`, `Graphviz`

## 📁 Repository Structure
```text
flowlens-process-mining/
├── data/
│   ├── raw/                 # Raw AnonymizedEventData.csv (114k rows)
│   └── processed/           # Cleaned EventLog & Aggregated Ticket KPIs
├── notebooks/
│   ├── 01_data_cleaning_and_kpis.ipynb    # Data cleaning & SLA Breach analysis
│   └── 02_process_discovery.ipynb         # PM4Py DFG maps & Conformance Checking
├── src/                     
│   └── data_preprocessing.py # Modular ETL pipeline script
├── dashboard/
│   └── app.py               # Streamlit interactive web dashboard
└── requirements.txt         # Project dependencies
```

## 📊 Running the Interactive Dashboard
To launch the interactive Streamlit dashboard locally:
1. Ensure your virtual environment is activated: `.\venv\Scripts\Activate.ps1`
2. Run the Streamlit app:
```powershell
streamlit run dashboard/app.py
```

## 💼 Resume Bullet Points (STAR Format)
*If you are using this project for applications, feel free to use these bullet points:*
> - **IT Incident Process Mining & Operational Intelligence** | *Python, PM4Py, Streamlit, Pandas*
> - Engineered an end-to-end incident analysis pipeline processing **114,000+ event logs**, deriving key ITIL metrics including MTTR, first-response time, and SLA breach rates.
> - Discovered and quantified ticket reassignment loops (*ping-pong effect*) causing multi-day delays by applying PM4Py Directly Follows Graphs (DFG) to reconstruct actual vs. ideal process flows.
> - Built and deployed an interactive **Streamlit dashboard** enabling stakeholders to filter performance bottlenecks by support team and visually track revenue-at-risk due to delayed resolutions.
