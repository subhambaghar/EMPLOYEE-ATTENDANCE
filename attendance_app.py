import pandas as pd
import streamlit as st
from io import BytesIO

path = "employee_attendance_july_2025_named.csv"

@st.cache_data
def loaddata():
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def filterdata(df, start, end, status):
    mask = (df['Date'] >= start) & (df['Date'] <= end)
    filtered_df = df.loc[mask]

    if status.lower() != "all":
        filtered_df = filtered_df[filtered_df['Attendance_Status'].str.lower() == status.lower()]
    return filtered_df

def toexcel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        processed_data = output.getvalue()
        return processed_data

# --- Streamlit App ---
st.set_page_config(
    page_title="EMPLOYEE MANAGEMENT SYSTEM",
    layout="wide"
)
st.title("EMPLOYEE ATTENDANCE PORTAL")
df = loaddata()

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    start_date = st.date_input("Start Date", value=df['Date'].min().date())
with col2:
    end_date = st.date_input("End Date", value=df['Date'].max().date())
with col3:
    status = st.selectbox("Attendance Status", ["All", "Present", "Absent", "Leave"])

# Filter button
if st.button("Filter Data"):
    filtered_df = filterdata(df, pd.to_datetime(start_date), pd.to_datetime(end_date), status)

    if filtered_df.empty:
        st.warning("No data found for the given criteria.")
    else:
        st.success(f"Found {len(filtered_df)} records.")
        st.dataframe(filtered_df, use_container_width=True)

        # Download button
        excel_data = toexcel(filtered_df)
        st.download_button(
            label="📥 Download as Excel",
            data=excel_data,
            file_name="filtered_attendance.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )