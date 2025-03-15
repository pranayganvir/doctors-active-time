import streamlit as st
import pandas as pd
import datetime

# Fetching Details
def fetch_details(dataframe, target_time):
    df   = dataframe.copy()
    
    df['Login Time'] = pd.to_datetime(df['Login Time'])
    df['Logout Time'] = pd.to_datetime(df['Logout Time'])
    
    # start_time = target_time.time()
    # start_time = str(start_time)

    # Subtracting 30 minutes
    new_time = target_time - pd.Timedelta(minutes=30)
    start_time = new_time.time()
    start_time = str(start_time)
    
    # Add 30 minutes using Timedelta
    new_time = target_time + pd.Timedelta(minutes=30)
    end_time = new_time.time()
    end_time = str(end_time)
    
    df = df.set_index('Login Time')
    df_filter = df.between_time(start_time, end_time)
    
    # Selecting that data where Usage Time is Greater than 30 minutes
    df_filter = df_filter[df_filter['Usage Time (mins)'] > 30]
    
    # Minimum Survey Attempt should be 4 
    df_filter = df_filter[df_filter['Count of Survey Attempts'] >= 4]
    
    # Resetting Index
    df = df.reset_index()
    
    new_order = ['NPI', 'State', 'Login Time', 'Logout Time', 'Usage Time (mins)', 'Region', 'Speciality', 'Count of Survey Attempts']
    df = df[new_order]

    return df_filter
    
    



# Load dataset (Replace with your actual file)
@st.cache_data
def load_data():
    df = pd.read_csv("dummy_npi_data.csv")  # Replace with actual file
    return df

# Load Data
df = load_data()

# Streamlit UI
st.title("Doctor Survey Time Filter App")
st.write("Enter a time, and we'll show the doctors who were active at that time.")

# User Input for Time
user_time = st.time_input("Select a time", datetime.time(6, 0))  # Default: 06:00 AM

# Convert input time to datetime
user_datetime = datetime.datetime.combine(datetime.date.today(), user_time)
# print(type(user_datetime))

# Filter doctors who were active during this time
filtered_df = fetch_details(df, user_datetime)

# Show results
st.subheader("Doctors Active at This Time")
st.dataframe(filtered_df)

# Optional: Export filtered data
if not filtered_df.empty:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data", data=csv, file_name="filtered_doctors.csv", mime="text/csv")

