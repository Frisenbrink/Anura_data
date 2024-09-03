import streamlit as st

# Base sizes for Protobuf and CSV at 1024 Hz for 3 seconds
base_sample_size = {
    "Protobuf": 37.0,  # in kB for 1024 Hz over 3 seconds
    "CSV": 234.5,      # in kB for 1024 Hz over 3 seconds
}

# Define other data options with fixed sizes and frequencies
fixed_data_options = {
    "Node Health (Protobuf)": {"size_kb": 254 / 1024, "frequency_sec": 60},
    "Aggregated (Protobuf)": {"size_kb": 173 / 1024, "frequency_sec": 1},
    "Aggregated (JSON)": {"size_kb": 482 / 1024, "frequency_sec": 1},
    "System Logs": {"size_kb": 1500, "frequency_sec": 3600},  # 1.5 MB per 60 min
}

# Streamlit App
st.header("Anura™ Data Usage Calculator")
st.markdown(
    """This repository contains data and information that can be used as a 
    reference or for in-depth analysis of the ReVibe Anura™ monitoring system 
    for vibrating screens. It includes vibration data collected from circular 
    motion machines, as well as examples of analysis software used to process 
    and visualize the data from the system. The vibration data was collected 
    under controlled conditions and provides insights into the performance of 
    the Anura monitoring system in response to different types of motion."""
)

# Sample rate slider for raw data
sample_rate = st.slider("Select Sample Rate for Raw Data (Hz)", min_value=1024, max_value=16384, step=1024)

# Sample duration slider (up to 10 seconds)
sample_duration = st.slider("Select Sample Duration (Seconds)", min_value=1, max_value=10, value=3)

# Raw data sampling frequency slider
sampling_frequency = st.slider("Select Frequency of Raw Data Sampling (Minutes)", min_value=1, max_value=60, value=1)

# Node multiplier slider
node_multiplier = st.slider("Select Number of Nodes", min_value=1, max_value=32, value=1)

# Calculate the number of samples based on the sample rate and duration
num_samples = sample_rate * sample_duration

# Calculate sizes based on selected sample rate and duration (scaling linearly)
protobuf_size = base_sample_size["Protobuf"] * (num_samples / 3072)  # 3072 samples = 3 seconds at 1024 Hz
csv_size = base_sample_size["CSV"] * (num_samples / 3072)

# Dynamic data options including the calculated raw data sizes
data_options = {
    f"Raw Data (Protobuf, {sample_rate} Hz, {sample_duration} sec)": {"size_kb": protobuf_size, "frequency_sec": sampling_frequency * 60},
    f"Raw Data (CSV, {sample_rate} Hz, {sample_duration} sec)": {"size_kb": csv_size, "frequency_sec": sampling_frequency * 60},
}

# Combine fixed data options
data_options.update(fixed_data_options)

# Multi-select box for data types
selected_data_types = st.multiselect(
    "Select Data Types",
    options=data_options.keys(),
    default=list(data_options.keys())
)

# Time slider for duration
time_hours = st.slider("Select Duration (Hours)", min_value=1, max_value=24, value=1)

# Calculate total time in seconds
total_time_sec = time_hours * 3600

# Function to calculate total data usage
def calculate_total_data(selected_data_types, total_time_sec, node_multiplier):
    total_data_kb = 0
    for data_type in selected_data_types:
        value = data_options[data_type]
        num_transmissions = total_time_sec / value["frequency_sec"]
        total_data_kb += value["size_kb"] * num_transmissions * node_multiplier
    return total_data_kb

# Calculate total data in kilobytes
total_data_kb = calculate_total_data(selected_data_types, total_time_sec, node_multiplier)

# Convert to megabytes
total_data_mb = total_data_kb / 1024

# Display the result in a more prominent and visually appealing way
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Total Data Usage</h2>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; font-size: 48px; color: #FF5722;'>{total_data_mb:.2f} MB</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center; color: #555;'>over {time_hours} hour(s) for {node_multiplier} node(s)</h4>", unsafe_allow_html=True)
