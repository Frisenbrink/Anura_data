import base64
from datetime import datetime
import math
import numpy as np
import os
import pandas as pd
import plotly.express as px
import streamlit as st
import re
from scipy.signal import get_window

logo = "Materials/ReVibe.png"

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

#add_bg_from_local('Materials/frog.png') 

st.columns(3)[1].image(logo)

#st.cache()
def main():

    config = {'displaylogo': False}

    from datetime import datetime

    def convert_unix_timestamp(timestamp):
        """Convert a UNIX timestamp in microseconds to a human-readable datetime string with millisecond precision."""
        # Convert timestamp from microseconds to seconds
        timestamp_seconds = timestamp / 1_000_000
        
        # Convert the timestamp to a datetime object
        dt = datetime.utcfromtimestamp(timestamp_seconds)
        
        # Format the datetime object to a human-readable string with millisecond precision
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    
    def plot_psd_from_csv(csv_file):
        """Plots the Power Spectral Density (PSD) from CSV data for x, y, z axes."""
        
        # Load the CSV file and extract the sample rate
        df = pd.read_csv(csv_file)
        sample_rate = math.floor(float(df.iloc[0, 2]))

        # Extract x, y, z axis data and convert to float
        x_data, y_data, z_data = (df.iloc[2:, i].astype(float) for i in range(3))

        # Number of samples
        n_samples = len(x_data)

        # Apply Hamming window to the data
        window = get_window('hamming', n_samples)
        x_data_windowed = x_data * window
        y_data_windowed = y_data * window
        z_data_windowed = z_data * window

        # Zero-padding to increase FFT resolution
        n_padded = 2 ** int(np.ceil(np.log2(n_samples)))

        # Compute FFT for each axis
        fft_x = np.fft.fft(x_data_windowed, n=n_padded)
        fft_y = np.fft.fft(y_data_windowed, n=n_padded)
        fft_z = np.fft.fft(z_data_windowed, n=n_padded)

        # Compute frequencies
        freqs = np.fft.fftfreq(n_padded, d=1/sample_rate)[:n_padded // 2]

        # Compute Power Spectral Density (PSD)
        def compute_psd(fft_data):
            psd = (np.abs(fft_data[:n_padded // 2]) ** 2) / (sample_rate * n_samples)
            psd[1:] *= 2  # Correct the amplitude for DC component
            return psd

        psd_x = compute_psd(fft_x)
        psd_y = compute_psd(fft_y)
        psd_z = compute_psd(fft_z)

        # Create a DataFrame for plotting
        psd_df = pd.DataFrame({
            'Frequency (Hz)': np.tile(freqs, 3),
            'PSD (g^2/Hz)': np.concatenate([psd_x, psd_y, psd_z]),
            'Axis': ['x'] * len(freqs) + ['y'] * len(freqs) + ['z'] * len(freqs)
        })

        # Plot the PSD using Plotly Express
        fig = px.line(
            psd_df, 
            x='Frequency (Hz)', 
            y='PSD (g^2/Hz)', 
            color='Axis',
            title='PSD of X, Y, Z Axis Data', 
            labels={'PSD (g^2/Hz)': 'PSD (g^2/Hz)'}
        )
        
        # Update plot layout
        fig.update_layout(legend=dict(orientation="h"))
        fig.update_traces(line_width=1.5)
        fig.update_xaxes(showgrid=True, gridcolor='lightgray', range=[0, 50], showspikes=True)
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray', showspikes=True)

        # Display the plot in Streamlit
        st.plotly_chart(fig)

    def plot_fft_from_csv(csv_file):
        """Plots the FFT (Fast Fourier Transform) from CSV data for x, y, z axes."""
        
        # Load the CSV file and extract the sample rate
        df = pd.read_csv(csv_file)
        sample_rate = math.floor(float(df.iloc[0, 2]))

        # Extract x, y, z axis data and convert to float
        x_data, y_data, z_data = (df.iloc[2:, i].astype(float) for i in range(3))

        # Number of samples
        n_samples = len(x_data)

        # Apply Hamming window to the data
        window = get_window('hamming', n_samples)
        x_data_windowed = x_data * window
        y_data_windowed = y_data * window
        z_data_windowed = z_data * window

        # Zero-padding to increase FFT resolution
        n_padded = 2 ** int(np.ceil(np.log2(n_samples)))

        # Compute FFT for each axis
        fft_x = np.fft.fft(x_data_windowed, n=n_padded)
        fft_y = np.fft.fft(y_data_windowed, n=n_padded)
        fft_z = np.fft.fft(z_data_windowed, n=n_padded)

        # Compute frequencies
        freqs = np.fft.fftfreq(n_padded, d=1/sample_rate)[:n_padded // 2]

        # Compute FFT amplitude
        def compute_amplitude(fft_data):
            amplitude = np.abs(fft_data[:n_padded // 2]) * 2 / n_samples
            amplitude[0] /= 2  # Correct the amplitude for DC component
            return amplitude

        fft_x = compute_amplitude(fft_x)
        fft_y = compute_amplitude(fft_y)
        fft_z = compute_amplitude(fft_z)

        # Create a DataFrame for plotting
        fft_df = pd.DataFrame({
            'Frequency (Hz)': np.tile(freqs, 3),
            'Amplitude': np.concatenate([fft_x, fft_y, fft_z]),
            'Axis': ['x'] * len(freqs) + ['y'] * len(freqs) + ['z'] * len(freqs)
        })

        # Plot the FFT using Plotly Express
        fig = px.line(
            fft_df, 
            x='Frequency (Hz)', 
            y='Amplitude', 
            color='Axis',
            title='FFT of X, Y, Z Axis Data', 
            labels={'Amplitude': 'Amplitude (g)'}
        )
        
        # Update plot layout
        fig.update_layout(
            legend=dict(orientation="h"),
            autosize=True,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        fig.update_traces(line_width=1.5)
        fig.update_xaxes(showgrid=True, gridcolor='lightgray', range=[0, 50], showspikes=True)
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray', showspikes=True)

        # Display the plot in Streamlit
        st.plotly_chart(fig)

    def space_plot(csv_file):
        df = pd.read_csv(csv_file, skiprows=2, nrows=temporal)
        peak_value = df.abs().max()
        peak_value = peak_value[1]
        print(peak_value)
        fig = px.line_3d(data_frame = df, x=df.iloc[:, 0], y=df.iloc[:, 2], z=df.iloc[:, 1] - 0.981, height=450, width=450, labels={
                     "x": "X",
                     "y": "Z",
                     "z": "Y"
                 })
        fig.update_scenes(aspectmode='cube')
        fig.update_layout(
            scene = dict(
                xaxis = dict(nticks=10, range=[-peak_value,peak_value],),
                            yaxis = dict(nticks=10, range=[- peak_value,peak_value],),
                            zaxis = dict(nticks=10, range=[-peak_value,peak_value],),),
            width=700)
        fig.update_layout(title= '3D Orbit of X, Y, Z axis data')
        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.0, y=-1.6, z=0.2))
        fig.update_layout(scene_camera=camera)    
        st.plotly_chart(fig, config=config)

    def orbit_plot(csv_file):
        df = pd.read_csv(csv_file, skiprows=2, nrows=temporal)
        # plot orbit
        fig = px.line(data_frame = df, x=df.iloc[:, 0], y=df.iloc[:, 1] - 0.891, height=650, color_discrete_sequence=["lightskyblue"])
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)
        fig.update_layout(title= 'Orbit plot',
                        xaxis_title='Amplitude (g)',
                        yaxis_title='Amplitude (g)',
                        yaxis_scaleanchor="x",
                        grid_pattern="independent",
                        showlegend=True)
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        st.plotly_chart(fig, config=config)

    def info_bar(csv_file):

        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Extract the sample rate from the third cell of the second row
        sample_rate = df.iloc[0, 2]
        time_stamp = df.iloc[0, 0]
        #print(int(time_stamp))
        
        
        # Ensure the sample rate is a float
        sample_rate = float(sample_rate)
        sample_rate = math.floor(sample_rate)
        
        # Extract x, y, z axis data
        x_data = df.iloc[2:, 0]
        y_data = df.iloc[2:, 1]
        z_data = df.iloc[2:, 2]
        
        # Number of samples
        n = len(x_data)
        
        # Time array
        t = np.arange(n) / sample_rate
        
        # Compute FFT
        fft_x = np.fft.fft(x_data)
        fft_y = np.fft.fft(y_data)
        fft_z = np.fft.fft(z_data)
        
        # Compute frequencies
        freqs = np.fft.fftfreq(n, d=1/sample_rate)
        
        # Only take the positive half of the spectrum for plotting
        half_n = n // 2 if n % 2 == 0 else (n // 2) + 1
        freqs = freqs[:half_n]

        fft_x = np.abs(fft_x[:half_n]) * 2 / n
        fft_y = np.abs(fft_y[:half_n]) * 2 / n
        fft_z = np.abs(fft_z[:half_n]) * 2 / n

        # Correct the amplitude for DC and Nyquist component
        fft_x[0] /= 2
        fft_y[0] /= 2
        fft_z[0] /= 2
        if n % 2 == 0:  # even length, Nyquist component exists
            fft_x[-1] /= 2
            fft_y[-1] /= 2
            fft_z[-1] /= 2
        
        dominant_freq_x = freqs[np.argmax(fft_x)]

        # Create a DataFrame for plotting
        fft_df = pd.DataFrame({
            'Frequency (Hz)': np.tile(freqs, 3),
            'Amplitude': np.concatenate([fft_x, fft_y, fft_z]),
            'Axis': ['x'] * half_n + ['y'] * half_n + ['z'] * half_n
        })

        def calculate_stroke_length(z_positions):
            max_position = z_positions.max()
            min_position = z_positions.min()
            stroke_length = max_position - min_position
            return round(stroke_length, 3)
        
        def calculate_amplitude(z_positions):
            mean_position = z_positions.mean()
            amplitude = (z_positions - mean_position).abs().max()
            return round(amplitude, 3)

        # Calculate displacement
        def calculate_displacement(z_positions):
            displacement = z_positions.max() - z_positions.min()
            return round(displacement, 3)
        
        def calculate_peak_acceleration(file_path):
            
            # Calculate the peak acceleration
            peak_acceleration = file_path.abs().max()
            
            return round(peak_acceleration, 3)
        
        def calc_rms(df):
            rms = df.copy()**2
            rms = rms.mean()**0.5
            return round(rms, 3)
        

        def stat_calc(df):
            df_stats = pd.concat([df.abs().max(), calc_rms(df)],axis=1)
            df_stats.columns = ['Acceleration Peak (g)','Acceleration RMS (g)']
            df_stats['Crest Factor'] = df_stats['Acceleration Peak (g)'] / df_stats['Acceleration RMS (g)']
            df_stats['Standard Deviation (g)'] = df.std()
            df_stats.index.name = 'Data Set'
            return df_stats

        #df_stats = stat_calc(x_data)
        #df_stats.round(3)
        
        def calculate_rms_acceleration(file_path):
            
            first_column = file_path
            
            # Calculate the RMS acceleration
            squared_values = first_column ** 2
            mean_of_squared_values = squared_values.mean()
            rms_acceleration = np.sqrt(mean_of_squared_values)
            
            return round(rms_acceleration, 3)
        
        def calculate_crest_factor(file_path):
            
            first_column = file_path
            
            # Calculate the peak value
            peak_value = first_column.abs().max()
            
            # Calculate the RMS value
            squared_values = first_column ** 2
            mean_of_squared_values = squared_values.mean()
            rms_value = np.sqrt(mean_of_squared_values)
            
            # Calculate the crest factor
            crest_factor = peak_value / rms_value
            
            return round(crest_factor, 3)
        
        # Make some nice litlle infos about data
        n = n + 1
        st.write("Information about the Anura measurement file:")
        st.write("Timestamp:", convert_unix_timestamp(time_stamp), time_stamp)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sample rate (Hz):", sample_rate)
        col2.metric("Number of samples:", n)
        col3.metric("Sample duration (seconds):", n / sample_rate)
        col4.metric("Frequency (Hz):", dominant_freq_x)
        #st.write("Vibration data:")
        #col1, col2, col3, col4 = st.columns(4)
        #col1.metric("Frequency (Hz):", math.floor(dominant_freq_x))
        #col1.metric("Frequency (Hz):", dominant_freq_x)
        #col2.metric("RPM:", math.floor(dominant_freq_x)*60)
        #col2.metric("RPM:", dominant_freq_x * 60)
        
        #st.write("X axis:")
        #col1, col2, col3, col4 = st.columns(4)
        #col1.metric("Peak Acceleration (g):", calculate_peak_acceleration(x_data))
        #col2.metric("RMS:", calc_rms(x_data))
        #col3.metric("Crest factor:", calculate_crest_factor(x_data))
        #col3.metric("Stroke length X", calculate_stroke_length(x_data))
        #col4.metric("Stroke length Y", calculate_stroke_length(y_data))
        
        #st.write("Y axis:")
        #col1, col2, col3, col4 = st.columns(4)
        #col1.metric("Peak Acceleration (g):", calculate_peak_acceleration(y_data))
        #col2.metric("RMS:", calc_rms(y_data))
        #col3.metric("Crest factor:", calculate_crest_factor(y_data))
        
        #st.write("Z axis:")
        #col1, col2, col3, col4 = st.columns(4)
        #col1.metric("Peak Acceleration (g):", calculate_peak_acceleration(z_data))
        #col2.metric("RMS:", calc_rms(z_data))
        #col3.metric("Crest factor:", calculate_crest_factor(z_data))
        #col3.metric("Y-Displacement", calculate_displacement(y_data))
        #col2.metric("Z-Amplitude", calculate_amplitude(z_data))
        #col3.metric("Z-Displacement", calculate_displacement(z_data))
        
    def plot_amplitude_data(csv_file):
        # Read the CSV file
        df = pd.read_csv(csv_file)
        # Extract the sample rate from the third cell of the second row (1-indexed: cell [1, 2])
        sample_rate = df.iloc[0, 2]
        rounded_down_num = math.floor(sample_rate)
        # Extract x, y, z amplitude data
        x_data = df.iloc[2:, 0].astype(float)  # Assuming x data starts from row 3 onwards
        y_data = df.iloc[2:, 1].astype(float)  # Assuming y data starts from row 3 onwards
        z_data = df.iloc[2:, 2].astype(float)  # Assuming z data starts from row 3 onwards
        # Calculate the number of samples
        num_samples = len(x_data)
        # Create a time axis in seconds
        time_axis = [i / rounded_down_num for i in range(num_samples)]
        # Create a DataFrame for plotting
        plot_df = pd.DataFrame({
            'Time (s)': time_axis,
            'X Amplitude (g)': x_data,
            'Y Amplitude (g)': y_data -0.981,
            'Z Amplitude (g)': z_data
        })
        # Plot the data using Plotly Express
        fig = px.line(plot_df, x='Time (s)', y=['X Amplitude (g)', 'Y Amplitude (g)', 'Z Amplitude (g)'],
                    labels={'value': 'Amplitude (g)', 'variable': 'Axis'},
                    title='Amplitude Data X,Y,Z axis')
        fig.update_layout(legend=dict(orientation="h"))
        fig.update_traces(line_width=1.0)
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray')
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        st.plotly_chart(fig, config=config)

    def sort_key(filename):
        parts = re.split(r'(\d+)', filename)
        return [int(part) if part.isdigit() else part for part in parts]

    def file_selector(folder_path='./data'):
        datafiles = os.listdir(folder_path)
        datafiles = sorted(datafiles, key=sort_key)
        
        selected_filename = st.selectbox('', datafiles)
        return os.path.join(folder_path, selected_filename)
    
    def process_file(file):
        plot_amplitude_data(file)
        
    def process_file2(file):
        plot_fft_from_csv(file)
        
    def process_file3(file):
        info_bar(file)

    def process_file4(file):
        space_plot(file)

    def process_file5(file):
        plot_psd_from_csv(file)

   
    st.header("Anura™ sample data")
    #st.subheader("Sample data")
    st.markdown(
        """This repository contains data and information that can be used as a 
        reference or for in-depth analysis of the ReVibe Anura™ monitoring system 
        for vibrating screens. It includes vibration data collected from circular 
        motion machines, as well as examples of analysis software used to process 
        and visualize the data from the system. The vibration data was collected 
        under controlled conditions and provides insights into the performance of 
        the Anura monitoring system in response to different types of motion."""
    )
    
    datafiles = file_selector()

    temporal = len(pd.read_csv(datafiles, skiprows=1))
    

    info_bar(datafiles)
    
    plot_amplitude_data(datafiles)

    space_plot(datafiles)  
    #orbit_plot(datafiles)

    #plot_fft_from_csv(datafiles)
    #plot_psd_from_csv(datafiles)            

    st.divider()

    my_expander = st.expander(label='Upload vibration data')

    with my_expander:       

        #files = st.file_uploader(label='upload your csv', type=['csv'])
        uploaded_files = st.file_uploader("Time plot", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Perform operations on each uploaded file
                process_file(uploaded_file)
            
        #files = st.file_uploader(label='upload your csv', type=['csv'])
        uploaded_files = st.file_uploader("FFT plot", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Perform operations on each uploaded file
                process_file2(uploaded_file)

        uploaded_files = st.file_uploader("General info", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Perform operations on each uploaded file
                process_file3(uploaded_file)

        uploaded_files = st.file_uploader("Space plot", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Perform operations on each uploaded file
                process_file4(uploaded_file)

        uploaded_files = st.file_uploader("PSD plot", accept_multiple_files=True)
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Perform operations on each uploaded file
                process_file5(uploaded_file)


    st.divider()
    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()
