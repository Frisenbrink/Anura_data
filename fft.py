# Step 1: Import necessary libraries
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.signal import butter, filtfilt

def butterworth_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

cutoff = 25.0  # desired cutoff frequency of the filter, Hz
fs = 1024.0    # sample rate, Hz (samples per second)
order = 3     # filter order

# Step 2: Create a sample pandas DataFrame
# For example, let's create a DataFrame with a time series data
#np.random.seed(0)
#time = np.linspace(0, 1, 1024)
#signal = np.sin(2 * np.pi * 50 * time) + np.sin(2 * np.pi * 120 * time) + np.random.normal(0, 1, 500)
#data = pd.DataFrame({'time': time, 'signal': signal})

uri = "data.csv"
data = pd.read_csv(uri)
data = data[1:-1]

data['filtered_signal1'] = butterworth_filter(data['Timestamp'], cutoff, fs, order)

sampler = len(data.Samplerate)
time = np.linspace(0, 1, sampler)
# Step 3: Perform FFT using numpy
fft_result = np.fft.fft(data['filtered_signal1'])
fft_freq = np.fft.fftfreq(len(fft_result), d=(time[1] - time[0]))

# Only keep the positive frequencies
positive_freqs = fft_freq[:len(fft_freq)//2]
positive_fft = np.abs(fft_result[:len(fft_result)//2])

# Step 4: Prepare the data for plotting
fft_data = pd.DataFrame({'Frequency': positive_freqs, 'Amplitude': positive_fft})

# Step 5: Plot the FFT result using Plotly Express
fig = px.line(fft_data, x='Frequency', y='Amplitude', title='FFT of the Signal')
fig.show()
