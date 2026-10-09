import pandas as pd
import numpy as np
import os

def load_and_clean_data(file_path):
    """
    Loads the raw IT Incident CSV, cleans the status column, and standardizes dates.
    """
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    
    # Standardize column names
    df.columns = [col.strip() for col in df.columns]
    
    # Parse DateTime
    print("Parsing datetime...")
    df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%y %H:%M')
    
    # Sort by Ticket and Time
    df = df.sort_values(by=['TicketNum', 'Time']).reset_index(drop=True)
    
    return df

def categorize_status(df):
    """
    Groups complex raw statuses into higher-level business categories.
    """
    print("Categorizing statuses...")
    
    # Define mapping
    status_mapping = {
        'Open': 'Open',
        'Closed': 'Closed',
        'Assignment': 'Assigned',
        'reassigned-misrouted': 'Reassigned - Misrouted',
        'reassigned-addl work required': 'Reassigned - Rework',
        'analysis/research/tech note': 'Analysis',
        'acknowledged notification': 'Notification Acknowledged',
        'restored to service': 'Resolved',
    }
    
    # Map known statuses, group 'alert' stages together, and keep 'pending' states structured
    def map_status(val):
        if pd.isna(val):
            return 'Unknown'
        val_str = str(val)
        if val_str in status_mapping:
            return status_mapping[val_str]
        elif 'alert' in val_str.lower():
            return 'Alert / Escalated'
        elif 'pending' in val_str.lower():
            return val_str.title()
        elif 'communication' in val_str.lower():
            return 'Communication'
        else:
            return val_str.title()
            
    df['Business_Status'] = df['Status'].apply(map_status)
    return df

def engineer_kpi_features(df):
    """
    Calculates MTTR and Ping-Pong counts per ticket.
    """
    print("Engineering KPI features...")
    
    # Calculate Lead Time (Resolution Time) per ticket
    # Assuming 'Open' is start and 'Closed' is end
    ticket_times = df.groupby('TicketNum')['Time'].agg(['min', 'max'])
    ticket_times['Resolution_Hours'] = (ticket_times['max'] - ticket_times['min']).dt.total_seconds() / 3600.0
    
    # Calculate Reassignment / Ping-Pong count per ticket
    reassignments = df[df['Business_Status'].str.contains('Reassigned', case=False, na=False)]
    ping_pong_counts = reassignments.groupby('TicketNum').size().reset_index(name='Ping_Pong_Count')
    
    # Merge back to a Ticket-Level aggregate dataframe
    ticket_kpis = pd.merge(ticket_times, ping_pong_counts, on='TicketNum', how='left')
    ticket_kpis['Ping_Pong_Count'] = ticket_kpis['Ping_Pong_Count'].fillna(0)
    
    return df, ticket_kpis

if __name__ == "__main__":
    # Handle paths robustly regardless of execution dir
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_PATH = os.path.join(base_dir, "data", "raw", "AnonymizedEventData.csv")
    PROCESSED_LOG_PATH = os.path.join(base_dir, "data", "processed", "Cleaned_EventLog.csv")
    PROCESSED_KPI_PATH = os.path.join(base_dir, "data", "processed", "Ticket_KPIs.csv")
    
    # Fallback to current directory if not in proper structure
    if not os.path.exists(RAW_PATH):
        RAW_PATH = "AnonymizedEventData.csv"
    
    if os.path.exists(RAW_PATH):
        df_clean = load_and_clean_data(RAW_PATH)
        df_clean = categorize_status(df_clean)
        df_clean, df_kpis = engineer_kpi_features(df_clean)
        
        print(f"Saving processed event log to {PROCESSED_LOG_PATH}...")
        os.makedirs(os.path.dirname(PROCESSED_LOG_PATH), exist_ok=True)
        df_clean.to_csv(PROCESSED_LOG_PATH, index=False)
        
        print(f"Saving KPI aggregates to {PROCESSED_KPI_PATH}...")
        df_kpis.to_csv(PROCESSED_KPI_PATH, index=False)
        
        print("Data Preprocessing Complete!")
    else:
        print(f"Error: Could not find raw data at {RAW_PATH}")
