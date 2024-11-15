import streamlit as st

# Title and introduction
st.title("VS1 Settings")
st.write("""
This app allows you to configure various sampling settings for the VS1 device, including:
- Sample Rate
- Sample Length
- Sampling Period
- Health Data Time Interval
""")

# Section 1: Sample Rate
st.subheader("1. Sample Rate")
sample_rate = st.selectbox(
    "Choose the sample rate (Hz):",
    options=[512, 1024, 2048, 4096, 8192, 16384],
    index=1
)
st.write(f"Selected Sample Rate: {sample_rate} Hz")

# Section 2: Sample Length
st.subheader("2. Sample Length")
duration_in_seconds = st.number_input(
    "Enter duration in seconds for each sample snippet:",
    min_value=0.1, max_value=60.0, value=3.0, step=0.5,
    format="%.1f"
)
snippet_num_samples = int(sample_rate * duration_in_seconds)
st.write(f"Sample Length: {snippet_num_samples} samples")
st.write(
    f"For example, at a base sample rate of {sample_rate} Hz for {duration_in_seconds:.1f} seconds:\n"
    f"{sample_rate} Hz × {duration_in_seconds:.1f} seconds = {snippet_num_samples} samples"
)

# Initialize session state for Sampling Period
if 'snippet_interval_ms' not in st.session_state:
    st.session_state['snippet_interval_ms'] = 60000
if 'snippet_interval_minutes' not in st.session_state:
    st.session_state['snippet_interval_minutes'] = st.session_state['snippet_interval_ms'] / 60000

# Initialize session state for Health Data Time Interval
if 'health_interval_ms' not in st.session_state:
    st.session_state['health_interval_ms'] = 60000
if 'health_interval_minutes' not in st.session_state:
    st.session_state['health_interval_minutes'] = st.session_state['health_interval_ms'] / 60000

# Callback functions to sync milliseconds and minutes
def update_snippet_interval_ms():
    st.session_state['snippet_interval_minutes'] = st.session_state['snippet_interval_ms'] / 60000

def update_snippet_interval_minutes():
    st.session_state['snippet_interval_ms'] = st.session_state['snippet_interval_minutes'] * 60000

def update_health_interval_ms():
    st.session_state['health_interval_minutes'] = st.session_state['health_interval_ms'] / 60000

def update_health_interval_minutes():
    st.session_state['health_interval_ms'] = st.session_state['health_interval_minutes'] * 60000

# Section 3: Sampling Period with synced inputs
st.subheader("3. Sampling Period")
#st.number_input(
#    "Set the sampling period (in milliseconds):",
#    min_value=1000, max_value=600000, step=1000,
#    key='snippet_interval_ms', on_change=update_snippet_interval_ms
#)
st.number_input(
    "Set the sampling period (in minutes):",
    min_value=0.1, max_value=60.0, step=0.5, value=1.0,
    key='snippet_interval_minutes', on_change=update_snippet_interval_minutes,
    format="%.2f"
)

# Section 4: Health Data Time Interval with synced inputs
st.subheader("4. Health Data Time Interval")
#st.number_input(
#    "Set the health data collection interval (in milliseconds):",
#    min_value=1000, max_value=600000, step=1000,
#    key='health_interval_ms', on_change=update_health_interval_ms
#)
st.number_input(
    "Set the health data collection interval (in minutes):",
    min_value=0.1, max_value=60.0, step=0.5, value=1.0,
    key='health_interval_minutes', on_change=update_health_interval_minutes,
    format="%.2f"
)

# Display all settings summary in a clean table format
st.subheader("Summary of Configured Settings")

# Create a dictionary to hold the settings for better formatting in a table
settings_summary = {
    "Setting": [
        "Sample Rate",
        "Sample Length",
        "Sampling Period",
        "Health Data Time Interval"
    ],
    "Value": [
        f"{sample_rate} Hz",
        f"{snippet_num_samples} samples", 
        f"{int(st.session_state['snippet_interval_ms'])} ms ({st.session_state['snippet_interval_minutes']:.2f} minutes)",
        f"{int(st.session_state['health_interval_ms'])} ms ({st.session_state['health_interval_minutes']:.2f} minutes)"
    ]
}

# Display the summary as a table
st.table(settings_summary)