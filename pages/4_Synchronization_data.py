import matplotlib.pyplot as plt
import os
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.chart_container import chart_container
import pandas as pd
import mpld3
import base64

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
df2 = pd.read_csv("Hammer_test/00_80_e1_26_ea_23/1671789366.csv", skiprows=2, usecols=[1])
data1 = None
data2 = None
data3 = None
data4 = None
root_dir = 'data'

st.columns(3)[1].image(logo)

def synk():

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

    axis = 'Y'
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
    
st.cache()
st.header("Synchronization data")
st.markdown("Hammer strike syncronization test, performed on ReVibe's test machine to determine sync between the sensors. The machine was stopped and when it reached a steady state two strikes with a hammer was delivered, the strikes was recorded by four (4) sensors that is synchronized within 3ms")

st.markdown("Y axis from one (1) sensor")
fig, ax = plt.subplots(1,1)
ax.plot(df2, linewidth=1.0)
ax.set_xlabel('Samples')
ax.set_ylabel('Amplitude (g)')
#st.pyplot(fig)
fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, width=1280, height=600)
#with chart_container(df2):
    #st.markdown("Hammer strike Y axis")
    #st.line_chart(df2)

st.markdown("Below is the product of a Python script that compares the four (4) files also found in the .zip file provided above. For information about this script please contact ReVibe")

st.markdown("Y axis from four (4) sensor")
synk()

st.markdown("""---""")
st.columns(3)[1].write("ReVibe Energy AB 2023")
    