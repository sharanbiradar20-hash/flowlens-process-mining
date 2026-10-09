import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pm4py
import os

# Automatically fix graphviz path for export script
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

df_kpis = pd.read_csv('data/processed/Ticket_KPIs.csv')
df_log = pd.read_csv('data/processed/Cleaned_EventLog.csv')

# --- FIGURE 1: MTTR HISTOGRAM ---
sns.set_theme(style="whitegrid")
mttr_median = df_kpis['Resolution_Hours'].median()
plt.figure(figsize=(10, 5))
sns.histplot(df_kpis[df_kpis['Resolution_Hours'] < 1000]['Resolution_Hours'], bins=50, kde=True)
plt.axvline(mttr_median, color='red', linestyle='--', label=f'Median: {mttr_median:.1f}h')
plt.title('Distribution of Ticket Resolution Time (Capped at 1000h for visibility)')
plt.xlabel('Resolution Time (Hours)')
plt.ylabel('Ticket Count')
plt.legend()
plt.savefig('figures/01_mttr_histogram.png', bbox_inches='tight')
plt.close()

# --- FIGURE 2: PING-PONG CHART ---
plt.figure(figsize=(8, 5))
sns.countplot(data=df_kpis[df_kpis['Ping_Pong_Count'] < 10], x='Ping_Pong_Count')
plt.title('Ping-Pong Effect: Reassignments per Ticket')
plt.xlabel('Number of Reassignments')
plt.ylabel('Ticket Count')
plt.savefig('figures/02_ping_pong_effect.png', bbox_inches='tight')
plt.close()

# --- FIGURE 3 & 4: PM4Py GRAPHS ---
df_log['Time'] = pd.to_datetime(df_log['Time'])
event_log = pm4py.format_dataframe(df_log, case_id='TicketNum', activity_key='Business_Status', timestamp_key='Time')

print("Generating Frequency DFG...")
dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)
pm4py.save_vis_dfg(dfg, start_activities, end_activities, 'figures/03_frequency_dfg.png')

print("Generating Performance DFG...")
performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(event_log)
pm4py.save_vis_performance_dfg(performance_dfg, start_activities, end_activities, 'figures/04_performance_dfg.png')

print("Generating BPMN Model...")
process_tree = pm4py.discover_process_tree_inductive(event_log)
bpmn_model = pm4py.convert_to_bpmn(process_tree)
pm4py.save_vis_bpmn(bpmn_model, 'figures/05_bpmn_model.png')

print("Successfully saved all 5 figures to the 'figures/' folder!")
