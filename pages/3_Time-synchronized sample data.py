import base64
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

config = {'displaylogo': False}

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('Materials/frog.png')
logo = "Materials/ReVibe.png"

st.columns(3)[1].image(logo)
axis = 'is_synced'

def get_csv_files(root_dir):
    files = []
    for filename in os.listdir(root_dir):
        if filename.endswith(".csv"):
            files.append(os.path.join(root_dir, filename))
    return files

def read_dataframes(files):
    return [pd.read_csv(f) for f in files]

def find_biggest_timestamp(dataframes, axis):
    biggest_value = max(df[axis][0] for df in dataframes)
    print(biggest_value)
    return biggest_value

def calculate_start_from(data, biggest_value, sample_rate):
    one_step_of_sample = 1000000 / sample_rate
    return int(round((biggest_value - data[axis][0]) / one_step_of_sample))

def calculate_y_axis(data, start_from, sample_rate):
    y_axis = []
    for i in range(0, data['Timestamp'].size - start_from - 1):
        y_axis.append(i * (1 / sample_rate))
    return y_axis

def calculate_x_axis(data, start_from):
    return list(data[axis][start_from+1:])

def synk(root_dir, plot_name):
    files = get_csv_files(root_dir)
    dataframes = read_dataframes(files)

    axis = 'is_synced'
    biggest_value = find_biggest_timestamp(dataframes, axis)
    sample_rates = [df['Samplerate'][0] for df in dataframes]

    fig = px.line()
    for i, data in enumerate(dataframes, start=1):
        start_from = calculate_start_from(data, biggest_value, sample_rates[i-1])
        y_axis = calculate_y_axis((data), start_from, sample_rates[i-1])
        x_axis = calculate_x_axis((data - 0.981), start_from)
        fig.add_scatter(x=y_axis, y=x_axis, mode='lines', name=os.path.basename(files[i-1]))

    fig.update_layout(title= plot_name,
                      xaxis_title='Seconds',
                      yaxis_title='Amplitude (g)', 
                      legend_title='Files')
    fig.update_layout(legend=dict(orientation="h"),autosize=False, width=660)
    fig.update_traces(line_width=1.5)
    fig.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray')
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)
    st.plotly_chart(fig, config=config)

def plot_columns_from_folder(folder_path):
    # Initialize lists to hold data from all files
    x_data = []
    y_data = []
    z_data = []
    file_names = []

    # Loop through all CSV files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            
            # Skip the first two rows and extract data from the third row onwards
            data = df.iloc[2:].astype(float)
            
            # Append data and file names
            x_data.append(data['Timestamp'])
            y_data.append(data['is_synced'] - 0.981)
            z_data.append(data['Samplerate'])
            file_names.append(file_name)
    
    
    fig_x = go.Figure()
    fig_y = go.Figure()
    fig_z = go.Figure()

    for i, file_name in enumerate(file_names):
        fig_x.add_trace(go.Scatter(x=list(range(len(x_data[i]))), y=x_data[i], mode='lines', name=file_name))
        fig_y.add_trace(go.Scatter(x=list(range(len(y_data[i]))), y=y_data[i], mode='lines', name=file_name))
        fig_z.add_trace(go.Scatter(x=list(range(len(z_data[i]))), y=z_data[i], mode='lines', name=file_name))
        
    # Create line plots for X, Y, Z columns
    fig_x.update_layout(title= "X axis data",
                      xaxis_title='Seconds',
                      yaxis_title='Amplitude (g)', 
                      legend_title='Files')
    fig_x.update_layout(legend=dict(orientation="h"),autosize=False, width=660)
    fig_x.update_traces(line_width=1.5)
    fig_x.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig_x.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray')
    fig_x.update_xaxes(showspikes=True)
    fig_x.update_yaxes(showspikes=True)

    fig_y.update_layout(title= "Y axis data",
                      xaxis_title='Seconds',
                      yaxis_title='Amplitude (g)', 
                      legend_title='Files')
    fig_y.update_layout(legend=dict(orientation="h"),autosize=False, width=660)
    fig_y.update_traces(line_width=1.5)
    fig_y.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig_y.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray')
    fig_y.update_xaxes(showspikes=True)
    fig_y.update_yaxes(showspikes=True)

    fig_z.update_layout(title= "Z axis data",
                      xaxis_title='Seconds',
                      yaxis_title='Amplitude (g)', 
                      legend_title='Files')
    fig_z.update_layout(legend=dict(orientation="h"),autosize=False, width=660)
    fig_z.update_traces(line_width=1.5)
    fig_z.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig_z.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray')
    fig_z.update_xaxes(showspikes=True)
    fig_z.update_yaxes(showspikes=True)

    st.plotly_chart(fig_x, config=config)
    st.plotly_chart(fig_y, config=config)
    #st.plotly_chart(fig_z, config=config)

    
#st.cache()

# Sync

st.header("Synchronized data from vibration screen")
st.markdown("Plots that compare eight (8) Anura nodes from a running screen. The data is separated between X data and Y data")

# Sync wiht Yusufs calc
#synk('synk2', 'Feed Right + Left Y axis')
#synk('synk3', 'Discharge Right + Left Y axis')

folder_path = 'synk4'
plot_columns_from_folder(folder_path)

st.markdown("""---""")

# Hammer test
st.header("Hammer strike synchronization data")
st.markdown("Hammer strike synchronization test, performed on ReVibe's test machine to determine time synchronization between the sensor nodes. The machine was stopped and when it reached a steady state two strikes with a hammer was delivered, the strikes was recorded by four (4) sensors that is synchronized within 3ms")
st.markdown("Below is the product of a Python script that compares four (4) Anura measurement of a hammer blow.")
synk('synk', 'Hammer test')

st.columns(3)[1].caption("Data from four (4) sensors")
st.columns(3)[1].write("ReVibe Energy AB 2024")