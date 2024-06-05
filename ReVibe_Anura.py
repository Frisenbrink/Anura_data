import base64
import math
import numpy as np
import os
import pandas as pd
import plotly.express as px
import streamlit as st
import time
from scipy.fft import fft, fftfreq

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
family = "Materials/anura.png"
screen = "Materials/Screen2.png"
video = "Materials/ReVibe_tease.mp4"
video2 = "Materials/ReVibe_Anura_Orange_ver1.mp4"

st.columns(3)[1].image(logo)

#st.cache()
def main():

    config = {'displaylogo': False}

    st.header("ReVibe Anura™ resources")
    st.subheader("Introduction")
    st.markdown('This repository contains data and information that can be used as a reference or for in-depth analysis of the ReVibe Anura™ monitoring system for vibrating screens. It includes vibration data collected from circular motion machines, as well as examples of analysis software used to process and visualize the data from the system. The vibration data was collected under controlled conditions and provides insights into the performance of the Anura monitoring system in response to different types of motion.')
    #st.image(family, width=None, caption="ReVibe Anura™ system")
    st.video(video2, start_time=4)
    
    st.markdown("""---""")
    my_expander = st.expander(label='ReVibe test installation')

    with my_expander:
        st.header("ReVibe test installation")
        st.write("Schaktmassor får nytt liv. Vid byggnation av hus och vägar uppstår ofta ett överskott av schaktmassor. Dessa massor består inte sällan av brukbar jord. Vi sorterar den och erbjuder ett antal jordprodukter som anpassas utifrån det specifika ändamålet. Återvinning av betong och asfalt. Genom att ta emot och krossa betong eller asfalt från anläggningsprojekt i samhället, och blanda med bergkrossprodukter, går det att minska samhällets deponivolymer, minska uttaget av jungfruligt material och samtidigt spara pengar. Betong och asfalt återvinns bland annat vid rivning av gamla byggnader och i samband med att gamla vägar bryts upp eller repareras. Ofta hamnar materialet på deponi. Att istället återvinna materialet gynnar både miljön och samhället.")

        st.image(screen, caption="Vibrating screen with ReVibe Anura™ sensor fitted.")
        st.write("Sed vel porttitor nisl, sit amet malesuada leo. Integer tempus, diam accumsan ultricies gravida, massa dolor vestibulum felis, eget condimentum leo odio eu nulla. Morbi commodo pellentesque massa lobortis placerat. Nam tincidunt nisi nec ipsum sollicitudin auctor. Nam fringilla dictum massa et congue. Nam imperdiet, nulla non tempus pharetra, massa leo congue enim, nec porttitor lectus nisi vel nunc. Etiam at mauris sit amet ipsum elementum consectetur ac in augue. Maecenas dolor nibh, viverra in scelerisque vitae, mollis at risus.")

        st.video(video)
        st.columns(3)[1].caption("Anura installation")

    st.markdown("""---""")

    def plot_fft_from_csv(csv_file):
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Extract the sample rate from the third cell of the second row
        sample_rate = df.iloc[0, 2]
        
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
        
        # Create a DataFrame for plotting
        fft_df = pd.DataFrame({
            'Frequency (Hz)': np.tile(freqs, 3),
            'Amplitude': np.concatenate([fft_x, fft_y, fft_z]),
            'Axis': ['x'] * half_n + ['y'] * half_n + ['z'] * half_n
        })

        # Plot the FFT using Plotly Express
        fig = px.line(fft_df, x='Frequency (Hz)', y='Amplitude', color='Axis',
                    title='FFT of X, Y, Z axis data', labels={'Amplitude': 'Amplitude (g)'})
        fig.update_layout(legend=dict(orientation="h"),autosize=False, width=660)
        fig.update_traces(line_width=1.5)
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray')
        fig.update_xaxes(range = [0,50])
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        st.plotly_chart(fig, config=config)

    def space_plot(csv_file):
        df = pd.read_csv(csv_file, skiprows=2, nrows=temporal)
        peak_value = df.abs().max()
        peak_value = peak_value[1]
        print(peak_value)
        fig = px.line_3d(data_frame = df, x=df.iloc[:, 0], y=df.iloc[:, 2], z=df.iloc[:, 1] - 0.981, height=650, width=650, labels={
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
            width=650)
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
        fig = px.line(data_frame = df, x=df.iloc[:, 0], y=df.iloc[:, 1] - 0.891, height=650, width=650, color_discrete_sequence=["lightskyblue"])
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
        st.write("Timestamp:", time_stamp)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sample rate (Hz):", sample_rate)
        col2.metric("Number of samples:", n)
        col3.metric("Sample length (seconds):", n / sample_rate)



        st.write("Vibration data:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Frequency (Hz):", math.floor(dominant_freq_x))
        col2.metric("RPM:", math.floor(dominant_freq_x)*60)
        
        st.write("X axis:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Peak Acceleration (g):", calculate_peak_acceleration(x_data))
        col2.metric("RMS:", calc_rms(x_data))
        col3.metric("Crest factor:", calculate_crest_factor(x_data))
        #col4.metric("Stroke length", calculate_stroke_length(x_data))
        
        st.write("Y axis:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Peak Acceleration (g):", calculate_peak_acceleration(y_data))
        col2.metric("RMS:", calc_rms(y_data))
        col3.metric("Crest factor:", calculate_crest_factor(y_data))
        
        st.write("Z axis:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Peak Acceleration (g):", calculate_peak_acceleration(z_data))
        col2.metric("RMS:", calc_rms(z_data))
        col3.metric("Crest factor:", calculate_crest_factor(z_data))
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
        fig.update_layout(legend=dict(orientation="h"),autosize=False, width=660)
        fig.update_traces(line_width=1.0)
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray')
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        st.plotly_chart(fig, config=config)

    def file_selector(folder_path='./data'):
        datafiles = os.listdir(folder_path)
        selected_filename = st.selectbox('', sorted(datafiles))
        return os.path.join(folder_path, selected_filename)
    
    def process_file(file):
        plot_amplitude_data(file)
        
    def process_file2(file):
        plot_fft_from_csv(file)

    def process_file3(file):
        info_bar(file)

    my_expander = st.expander(label='Sample data')

    with my_expander:

        st.subheader("Sample data")
        st.write('Sed vel porttitor nisl, sit amet malesuada leo. Integer tempus, diam accumsan ultricies gravida, massa dolor vestibulum felis, eget condimentum leo odio eu nulla. Morbi commodo pellentesque massa lobortis placerat. Nam tincidunt nisi nec ipsum sollicitudin auctor. Nam fringilla dictum massa et congue. Nam imperdiet, nulla non tempus pharetra, massa leo congue enim, nec porttitor lectus nisi vel nunc. Etiam at mauris sit amet ipsum elementum consectetur ac in augue. Maecenas dolor nibh, viverra in scelerisque vitae, mollis at risus.')
        
        datafiles = file_selector()

        temporal = len(pd.read_csv(datafiles, skiprows=1))

        info_bar(datafiles)
        plot_amplitude_data(datafiles)
        #plot_fft_from_csv(datafiles)
        space_plot(datafiles)
        #orbit_plot(datafiles)
                

    st.markdown("""---""")

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

    st.markdown("""---""")
    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()