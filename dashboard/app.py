import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="FlowLens Dashboard", layout="wide")

# -- Load Data --
@st.cache_data
def load_data():
    try:
        df_log = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'Cleaned_EventLog.csv'))
        df_kpi = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'Ticket_KPIs.csv'))
        return df_log, df_kpi
    except FileNotFoundError:
        return pd.DataFrame(), pd.DataFrame()

df_log, df_kpi = load_data()

# -- Sidebar --
st.sidebar.title("FlowLens Dashboard")
st.sidebar.markdown("### IT Incident Process Mining")
st.sidebar.write("This dashboard visualizes process bottlenecks, SLA breaches, and the 'Ping-Pong' reassignment effect from 114k+ IT service logs.")

if len(df_kpi) == 0:
    st.error("Processed data not found. Please run the data preprocessing script first.")
    st.stop()

# Interactive Filters
st.sidebar.markdown("---")
max_ping_pong = int(df_kpi['Ping_Pong_Count'].max())
ping_pong_filter = st.sidebar.slider("Filter: Min Ping-Pong (Reassignments)", 0, 10, 0)
sla_filter = st.sidebar.checkbox("Show Only SLA Breached Tickets (>72h)", value=False)

# Apply Filters
filtered_kpi = df_kpi[df_kpi['Ping_Pong_Count'] >= ping_pong_filter]
if sla_filter:
    filtered_kpi = filtered_kpi[filtered_kpi['Resolution_Hours'] > 72]

# -- Top KPI Cards --
st.title("Operational Intelligence: Bottleneck & SLA Tracker")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", f"{len(filtered_kpi):,}")
col2.metric("Median MTTR (Hours)", f"{filtered_kpi['Resolution_Hours'].median():.1f}")
col3.metric("Max MTTR (Hours)", f"{filtered_kpi['Resolution_Hours'].max():.1f}")

if len(filtered_kpi) > 0:
    breach_rate = (filtered_kpi['Resolution_Hours'] > 72).mean() * 100
else:
    breach_rate = 0.0
col4.metric("SLA Breach Rate (>72h)", f"{breach_rate:.1f}%")

st.markdown("---")

# -- Charts --
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Distribution of Resolution Time (MTTR)")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_kpi[filtered_kpi['Resolution_Hours'] < 500]['Resolution_Hours'], bins=40, kde=True, color='#2c3e50', ax=ax)
    ax.set_title("Resolution Time Capped at 500h")
    ax.set_xlabel("Hours to Resolve")
    ax.set_ylabel("Number of Tickets")
    st.pyplot(fig)

with col_right:
    st.subheader("The 'Ping-Pong' Effect")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.countplot(data=filtered_kpi[filtered_kpi['Ping_Pong_Count'] < 10], x='Ping_Pong_Count', palette="Reds_r", ax=ax2)
    ax2.set_title("Tickets by Number of Reassignments")
    ax2.set_xlabel("Reassignment Count")
    ax2.set_ylabel("Number of Tickets")
    st.pyplot(fig2)

# -- Data Table --
st.subheader("Raw Filtered Output")
st.dataframe(filtered_kpi.sort_values(by='Resolution_Hours', ascending=False).head(50))
