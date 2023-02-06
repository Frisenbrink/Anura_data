import streamlit as st
import numpy as np
from scipy.signal import resample
import mpld3
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

apptitle = 'Anura data'
st.set_page_config(page_title=apptitle)

zip = "Anura_data.zip"

video = "Materials/Vibinspect_demo.mp4"
video2 = "Materials/Circular.mp4"

code = '''def hello():
    print("Hello, Streamlit!")'''

data_circular = np.genfromtxt("Circular_motion/00_80_e1_26_e7_16/1673620685.csv", delimiter=",", skip_header=2, usecols=[0])
circular = resample(data_circular, 832 * 3, axis=0)

data_linear = np.genfromtxt("Linear_motion/00_80_e1_26_e9_4a/1675253710.csv", delimiter=",", skip_header=2, usecols=[2])
data_linear -= 1
linear = resample(data_linear, 832 * 3, axis=0)

data_hammer = np.genfromtxt("Hammer_test/00_80_e1_26_ea_23/1671789366.csv", delimiter=",", skip_header=2, usecols=[2])
hammer = resample(data_hammer, 832 * 3, axis=0)

data1 = None
data2 = None
data3 = None
data4 = None

def synk():
    import matplotlib.pyplot as plt
    import mpld3
    import streamlit.components.v1 as components
    import os
    import pandas as pd

    root_dir = 'data'
    files = []
    for filename in os.listdir(root_dir):
        if filename.endswith(".csv"):
            files.append(os.path.join(root_dir, filename))
            continue
        else:
            continue
    # create a list of the dataframes
    dataframes = [pd.read_csv(f) for f in files]
    # create list of variables for each dataframe dynamically
    for i, df in enumerate(dataframes):
        globals()['data%s' % (i+1)] = df
    y_axis1 = []
    y_axis2 = []
    y_axis3 = []
    y_axis4 = []

    axis = 'X'
    data1_timestamp = data1['X'][0]
    data2_timestamp = data2['X'][0]
    data3_timestamp = data3['X'][0]
    data4_timestamp = data4['X'][0]

    sample_rate1 = data1['Z'][0] / 10
    sample_rate2 = data2['Z'][0] / 10
    sample_rate3 = data3['Z'][0] / 10
    sample_rate4 = data4['Z'][0] / 10

    print("samplerate of data1:",sample_rate1)
    print("samplerate of data2:",sample_rate2)
    print("samplerate of data3:",sample_rate3)
    print("samplerate of data4:",sample_rate4)

    biggest_value = data1_timestamp
    if(data2_timestamp > biggest_value):
        biggest_value = data2_timestamp
    if(data3_timestamp > biggest_value):
        biggest_value = data3_timestamp
    if(data4_timestamp > biggest_value):
        biggest_value = data4_timestamp

    print(biggest_value)
    one_step_of_sample1 = 1000000 / sample_rate1
    one_step_of_sample2 = 1000000 / sample_rate2
    one_step_of_sample3 = 1000000 / sample_rate3
    one_step_of_sample4 = 1000000 / sample_rate4

    data1_start_from = int(round((biggest_value - data1_timestamp) / one_step_of_sample1))
    print("data1 starts from:",data1_start_from)
    data2_start_from = int(round((biggest_value - data2_timestamp) / one_step_of_sample2))
    print("data2 starts from:",data2_start_from)
    data3_start_from = int(round((biggest_value - data3_timestamp) / one_step_of_sample3))
    print("data3 starts from:",data3_start_from)
    data4_start_from = int(round((biggest_value - data4_timestamp) / one_step_of_sample4))
    print("data4 starts from:",data4_start_from)

    for i in range(0,data1['X'].size-data1_start_from-1):
        y_axis1.append(i*(1/sample_rate1))
    for i in range(0,data2['X'].size-data2_start_from-1):
        y_axis2.append(i*(1/sample_rate2))
    for i in range(0,data3['X'].size-data3_start_from-1):
        y_axis3.append(i*(1/sample_rate3))
    for i in range(0,data4['X'].size-data4_start_from-1):
        y_axis4.append(i*(1/sample_rate4))

    x_axis1 = []
    for i in range(1+data1_start_from,data1[axis].size):
        x_axis1.append(data1[axis][i])
    x_axis2 = []
    for i in range(1+data2_start_from,data2[axis].size):
        x_axis2.append(data2[axis][i])
    x_axis3 = []
    for i in range(1+data3_start_from,data3[axis].size):
        x_axis3.append(data3[axis][i])
    x_axis4 = []
    for i in range(1+data4_start_from,data4[axis].size):
        x_axis4.append(data4[axis][i])

    fig = plt.figure()
    plt.plot(y_axis1,x_axis1)
    plt.plot(y_axis2,x_axis2)
    plt.plot(y_axis3,x_axis3)
    plt.plot(y_axis4,x_axis4)
    plt.legend(files)
    #plt.show()
    #st.pyplot(fig)
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, width=1280, height=600)


def main():
    st.title("ReVibe Anura™ data for analysis")
    
    st.subheader("Introduction")
    st.write("This repository contains data and information that can be used for reference or analysis of the Anura sensoring system. It contains vibration data from a circular motion rig and also a linear shaker. And tips for software analysis")
    
    st.write("The files available below are measurements procurred through Anura™. Please download and analyze these files with Vibinspect or preferred software package.")
    with open("Materials/Anura_data.zip", "rb") as fp:
        btn = st.download_button(
            label="Download Anura ™ data files",
            data=fp,
            file_name="Anura_data.zip",
            mime="application/zip"
    )


    st.subheader("Circular motion")
    st.write("Used by ReVibe for development purposes. Due to it’s size and requirement for mobility, the circular motion is not a clean signal. But is susceptible to noise in the form of motion/vibrations of the whole machine.")
    
    st.line_chart(circular)
    #X = np.fft.fft(circular)
    #fig, ax = plt.subplots()
    #ax.plot(np.abs(X))
    #fig_html = mpld3.fig_to_html(fig)
    #components.html(fig_html, width=1280, height=600)
    st.video(video2)

    st.subheader("Linear motion")
    st.write("Produces a cleaner waveform in one axis.")
    st.line_chart(linear)

    st.subheader("Hammer strike")
    st.write("Hammer strikes to determine sync between the sensors")
    st.line_chart(hammer)
    st.write("The button below loads a script that syncs the four (4) files also found in the .zip file provided above.")
    #if st.button("4 sensor sync analysis script"):
        #subprocess.run([f"{sys.executable}", "synk.py"])
    #if st.button("4 sensor sync analysis script 2"):
        #synk()
    synk()


    st.subheader("Vibinspect")
    st.write("ReVibe software package used for powerful analysis of signals. Download for free on https://revibeenergy.com/vibinspect-analysing-software/ Use this to analyse the files provided in this package. The samplerate of the provided data is 832Hz and has a length of 3 seconds. Data from four (4) sensors is provided they can be distinguished by their unique name in the following form (00_00_00_00_00_00) Every file comes with X,Y,Z axis data in the form of a .csv file. PLease see video for tips on doing FFT and orbit plots")

    st.video(video)

if __name__ == '__main__':
    main()
