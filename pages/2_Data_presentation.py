import math
import numpy as np
import os
import pandas as pd
import plotly.express as px
import re
import streamlit as st
from datetime import datetime
from scipy.signal import get_window

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2025</p>
</div>"""

logo = "Materials/ReVibe.png"

st.columns(3)[1].image(logo)

def main():
    config = {'displaylogo': False}
    
    def convert_unix_timestamp(timestamp):
        try:
            timestamp = int(timestamp)
            timestamp_seconds = timestamp / 1_000_000
            dt = datetime.utcfromtimestamp(timestamp_seconds)
            milliseconds = int((timestamp % 1_000_000) / 1_000)
            return dt.strftime('%Y-%m-%d %H:%M:%S.') + f'{milliseconds:03}'
        
        except (TypeError, ValueError, OverflowError) as e:
            return f"Error: {e}"
    
    def plot_psd_from_csv(csv_file):
        df = pd.read_csv(csv_file)
        sample_rate = math.floor(float(df.iloc[0, 2]))
        x_data, y_data, z_data = (df.iloc[2:, i].astype(float) for i in range(3))

        n_samples = len(x_data)

        window = get_window('hamming', n_samples)
        x_data_windowed = x_data * window
        y_data_windowed = y_data * window
        z_data_windowed = z_data * window

        n_padded = 2 ** int(np.ceil(np.log2(n_samples)))

        fft_x = np.fft.fft(x_data_windowed, n=n_padded)
        fft_y = np.fft.fft(y_data_windowed, n=n_padded)
        fft_z = np.fft.fft(z_data_windowed, n=n_padded)

        freqs = np.fft.fftfreq(n_padded, d=1/sample_rate)[:n_padded // 2]

        def compute_psd(fft_data):
            psd = (np.abs(fft_data[:n_padded // 2]) ** 2) / (sample_rate * n_samples)
            psd[1:] *= 2
            return psd

        psd_x = compute_psd(fft_x)
        psd_y = compute_psd(fft_y)
        psd_z = compute_psd(fft_z)

        psd_df = pd.DataFrame({
            'Frequency (Hz)': np.tile(freqs, 3),
            'PSD (g^2/Hz)': np.concatenate([psd_x, psd_y, psd_z]),
            'Axis': ['x'] * len(freqs) + ['y'] * len(freqs) + ['z'] * len(freqs)
        })

        fig = px.line(
            psd_df, 
            x='Frequency (Hz)', 
            y='PSD (g^2/Hz)', 
            color='Axis',
            title='PSD of X, Y, Z Axis Data', 
            labels={'PSD (g^2/Hz)': 'PSD (g^2/Hz)'}
        )
        
        fig.update_layout(legend=dict(orientation="h"))
        fig.update_traces(line_width=1.5)
        fig.update_xaxes(showgrid=True, gridcolor='lightgray', range=[0, 50], showspikes=True)
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray', showspikes=True)

        st.plotly_chart(fig, config=config)

    def plot_fft_from_csv(csv_file):
        
        df = pd.read_csv(csv_file)
        sample_rate = math.floor(float(df.iloc[0, 2]))

        x_data, y_data, z_data = (df.iloc[2:, i].astype(float) for i in range(3))

        n_samples = len(x_data)

        window = get_window('hamming', n_samples)
        x_data_windowed, y_data_windowed, z_data_windowed = [data * window for data in (x_data, y_data, z_data)]

        n_padded = 2 ** int(np.ceil(np.log2(n_samples)))

        fft_x = np.fft.fft(x_data_windowed, n=n_padded)
        fft_y = np.fft.fft(y_data_windowed, n=n_padded)
        fft_z = np.fft.fft(z_data_windowed, n=n_padded)

        freqs = np.fft.fftfreq(n_padded, d=1/sample_rate)[:n_padded // 2]


        def compute_amplitude(fft_data):
            amplitude = np.abs(fft_data[:n_padded // 2]) * 2 / n_samples
            amplitude[0] /= 2
            return amplitude

        fft_x = compute_amplitude(fft_x)
        fft_y = compute_amplitude(fft_y)
        fft_z = compute_amplitude(fft_z)

        fft_df = pd.DataFrame({
            'Frequency (Hz)': np.tile(freqs, 3),
            'Amplitude': np.concatenate([fft_x, fft_y, fft_z]),
            'Axis': ['x'] * len(freqs) + ['y'] * len(freqs) + ['z'] * len(freqs)
        })

        fig = px.line(
            fft_df, 
            x='Frequency (Hz)', 
            y='Amplitude', 
            color='Axis',
            title='FFT of X, Y, Z Axis Data', 
            labels={'Amplitude': 'Amplitude (g)'}
        )
        
        fig.update_layout(
            legend=dict(orientation="h"),
            autosize=True,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        fig.update_traces(line_width=1.5)
        fig.update_xaxes(showgrid=True, gridcolor='lightgray', range=[0, 50], showspikes=True)
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', zerolinecolor='gray', showspikes=True)

        st.plotly_chart(fig, config=config)

    def space_plot(csv_file):
        try:
            df = pd.read_csv(csv_file, skiprows=2, nrows=temporal)
        
            if df.empty or len(df.columns) < 3:
                raise ValueError("CSV file does not contain sufficient data for plotting.")
            
            peak_value = df.abs().max()[1]
            print(peak_value)
            
            fig = px.line_3d(
                data_frame=df,
                x=df.iloc[:, 0], y=df.iloc[:, 2], z=df.iloc[:, 1] - 0.981, 
                height=450, width=450,
                labels={"x": "X", "y": "Z", "z": "Y"}
            )

            fig.update_scenes(aspectmode='cube')
            fig.update_layout(
                scene=dict(
                    xaxis=dict(nticks=10, range=[-peak_value, peak_value]),
                    yaxis=dict(nticks=10, range=[-peak_value, peak_value]),
                    zaxis=dict(nticks=10, range=[-peak_value, peak_value])
                ),
                width=700,
                title='3D Orbit of X, Y, Z axis data'
            )

            camera = dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.0, y=-1.6, z=0.2)
            )
            fig.update_layout(scene_camera=camera)

            st.plotly_chart(fig, config=config)

        except FileNotFoundError:
            st.error("CSV file not found. Please upload a valid file.")
        except pd.errors.EmptyDataError:
            st.error("The file is empty. Please upload a valid CSV file.")
        except ValueError as ve:
            st.error(f"Value error: {ve}")
        except KeyError as ke:
            st.error(f"Data format error: {ke}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    def orbit_plot(csv_file):
        try:
            df = pd.read_csv(csv_file, skiprows=2, nrows=temporal)
            
            if df.empty or len(df.columns) < 2:
                raise ValueError("CSV file does not contain sufficient data for plotting.")
            
            fig = px.line(
                data_frame=df,
                x=df.iloc[:, 0],
                y=df.iloc[:, 1] - 0.891,
                height=650,
                color_discrete_sequence=["lightskyblue"]
            )
            
            fig.update_xaxes(showgrid=True, showspikes=True)
            fig.update_yaxes(showgrid=True, showspikes=True, scaleanchor="x")
            fig.update_layout(
                title='Orbit plot',
                xaxis_title='Amplitude (g)',
                yaxis_title='Amplitude (g)',
                grid_pattern="independent",
                showlegend=True
            )
            
            st.plotly_chart(fig, config=config)

        except FileNotFoundError:
            st.error("CSV file not found. Please upload a valid file.")
        except pd.errors.EmptyDataError:
            st.error("The file is empty. Please upload a valid CSV file.")
        except ValueError as ve:
            st.error(f"Value error: {ve}")
        except KeyError as ke:
            st.error(f"Data format error: {ke}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    def info_bar(csv_file):
        try:
            df = pd.read_csv(csv_file)

            if df.empty or len(df.columns) < 3 or len(df) < 3:
                raise ValueError("CSV file does not contain sufficient data for processing.")

            time_stamp = df.iloc[0, 0]
            sample_rate = math.floor(float(df.iloc[0, 2]))

            x_data, y_data, z_data = df.iloc[2:, 0], df.iloc[2:, 1], df.iloc[2:, 2]

            if x_data.empty or y_data.empty or z_data.empty:
                raise ValueError("X, Y, or Z data columns are empty.")

            n = len(x_data)
            fft_x, fft_y, fft_z = np.fft.fft(x_data), np.fft.fft(y_data), np.fft.fft(z_data)
            freqs = np.fft.fftfreq(n, d=1/sample_rate)

            half_n = n // 2 if n % 2 == 0 else (n // 2) + 1
            freqs = freqs[:half_n]

            fft_x, fft_y, fft_z = [np.abs(fft[:half_n]) * 2 / n for fft in (fft_x, fft_y, fft_z)]

            for fft in (fft_x, fft_y, fft_z): 
                fft[0] /= 2

            if n % 2 == 0:
                for fft in (fft_x, fft_y, fft_z): 
                    fft[-1] /= 2

            dominant_freq_x = freqs[np.argmax(fft_x)]
            n += 1

            st.write("Information about the Anura measurement file:")
            st.write("Timestamp:", convert_unix_timestamp(time_stamp), time_stamp)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Sample rate (Hz):", sample_rate)
            col2.metric("Number of samples:", n)
            col3.metric("Sample duration (seconds):", n / sample_rate)

            st.write("Vibration data:")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Operational Frequency (Hz):", math.floor(dominant_freq_x))
            col2.metric("RPM:", math.floor(dominant_freq_x) * 60)

        except FileNotFoundError:
            st.error("CSV file not found. Please upload a valid file.")
        except pd.errors.EmptyDataError:
            st.error("The file is empty. Please upload a valid CSV file.")
        except ValueError as ve:
            st.error(f"Value error: {ve}")
        except KeyError as ke:
            st.error(f"Data format error: {ke}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    def plot_amplitude_data(csv_file):
        try:
            df = pd.read_csv(csv_file)
            
            if df.empty or len(df.columns) < 3 or len(df) < 3:
                raise ValueError("CSV file does not contain sufficient data for plotting.")

            sample_rate = math.floor(df.iloc[0, 2])
            x_data, y_data, z_data = df.iloc[2:, 0].astype(float), df.iloc[2:, 1].astype(float), df.iloc[2:, 2].astype(float)
            
            num_samples = len(x_data)
            time_axis = np.arange(num_samples) / sample_rate

            plot_df = pd.DataFrame({
                'Time (s)': time_axis,
                'X Amplitude (g)': x_data,
                'Y Amplitude (g)': y_data - 0.981, 
                'Z Amplitude (g)': z_data
            })

            fig = px.line(
                plot_df,
                x='Time (s)',
                y=['X Amplitude (g)', 'Y Amplitude (g)', 'Z Amplitude (g)'],
                labels={'value': 'Amplitude (g)', 'variable': 'Axis'},
                title='Amplitude Data X, Y, Z Axis'
            )

            fig.update_layout(
                legend=dict(orientation="h"),
                xaxis=dict(showgrid=True, gridcolor='lightgray', showspikes=True),
                yaxis=dict(showgrid=True, gridcolor='lightgray', zerolinecolor='gray', showspikes=True),
                margin=dict(l=0, r=0, t=30, b=0)
            )
            fig.update_traces(line_width=1.0)

            st.plotly_chart(fig, config=config)

        except FileNotFoundError:
            st.error("CSV file not found. Please upload a valid file.")
        except pd.errors.EmptyDataError:
            st.error("The file is empty. Please upload a valid CSV file.")
        except ValueError as ve:
            st.error(f"Value error: {ve}")
        except KeyError as ke:
            st.error(f"Data format error: {ke}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    def sort_key(filename):
        try:
            parts = re.split(r'(\d+)', filename)

            return [int(part) if part.isdigit() else part for part in parts]

        except TypeError as te:
            raise ValueError(f"Invalid filename provided: {filename}. It must be a string.") from te
        except Exception as e:
            raise ValueError(f"An unexpected error occurred while processing the filename: {e}")

    def file_selector(folder_path='./data'):
        try:
            if not os.path.isdir(folder_path):
                raise FileNotFoundError(f"The directory '{folder_path}' does not exist.")

            datafiles = os.listdir(folder_path)
            
            if not datafiles:
                raise FileNotFoundError(f"No files found in the directory '{folder_path}'.")

            datafiles = sorted(datafiles, key=sort_key)
            
            selected_filename = st.selectbox('Select a file', datafiles)
            
            return os.path.join(folder_path, selected_filename)

        except FileNotFoundError as fnf_error:
            st.error(fnf_error)
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    def process_file(file, processing_function):
        processing_function(file)

    st.header("Anura™ sample data")

    st.markdown(
        """This repository contains data and information that can be used as a 
        reference or for in-depth analysis of the ReVibe Anura™ monitoring system 
        for vibrating screens. It includes vibration data collected from circular 
        motion machines. The vibration data was collected 
        under controlled conditions and provides insights into the performance of 
        the Anura monitoring system in response to different types of motion."""
    )
    
    datafiles = file_selector()

    temporal = len(pd.read_csv(datafiles, skiprows=1))

    def display_options(datafiles):
        """Allows the user to choose which plots or info to display."""
        
        options = {
            "Sample Info": info_bar,
            "Amplitude Plot": plot_amplitude_data,
            "3D Orbit Plot": space_plot,
            "Orbit Plot": orbit_plot,
            "Plot FFT": plot_fft_from_csv,
            "Plot PSD": plot_psd_from_csv,
        }

        default_selections = ["Sample Info", "Amplitude Plot", "3D Orbit Plot"]
        
        selected_options = st.multiselect(
            "Choose what you want to display:",
            list(options.keys()),
            default=default_selections
        )
        
        for option in selected_options:
            options[option](datafiles) 

    display_options(datafiles)      

    st.divider()

    def handle_file_upload(label, processing_function):
        uploaded_files = st.file_uploader(label, accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                process_file(uploaded_file, processing_function)

    my_expander = st.expander(label='Upload vibration data')

    with my_expander:
        upload_labels_and_functions = [
            ("Time plot", plot_amplitude_data),
            ("FFT plot", plot_fft_from_csv),
            ("General info", info_bar),
            ("Space plot", space_plot),
            ("PSD plot", plot_psd_from_csv)
        ]
        
        for label, func in upload_labels_and_functions:
            handle_file_upload(label, func)

    st.divider()
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
