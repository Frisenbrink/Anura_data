import streamlit as st
import pandas as pd
#from streamlit_extras.chart_container import chart_container
import base64
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import mpld3



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
video2 = "Materials/Circular.mp4"
screen = "Materials/Screen.png"
zip = "Anura_data.zip"

#df = pd.read_csv("Circular_motion/00_80_e1_26_e7_16/1673620685.csv", skiprows=2, usecols=[0,1,2])
#df2 = pd.read_csv("No_name/00_80_e1_26_e7_16/1674153368.csv", skiprows=2, usecols=[0,1,2])
df = pd.read_csv("Circular_motion/Refdata_1.csv", skiprows=2, usecols=[0,1,2])
df2 = pd.read_csv("Circular_motion/Refdata_2.csv", skiprows=2, usecols=[0,1,2])

st.columns(3)[1].image(logo)

st.header("Download ReVibe Anura™ sample data")
st.markdown("We are pleased to offer you access to a set of data that has been procured through ReVibe Anura™. The files, which are available for download below, contain a series of detailed measurements that have been collected using Anura sensors. To ensure that you can make the most of this data, we recommend that you use Vibinspect or your preferred software package to analyze the files. Please see the Vibinspect section for a primer into using vibration analysis software.")
with open("Materials/Anura_data.zip", "rb") as fp:
    btn = st.columns(3)[1].download_button(
        label="Download Anura™ sample data files",
        data=fp,
        file_name="Anura_data.zip",
        mime="application/zip"
    )
st.image(screen, caption="Vibrating screen with ReVibe Anura™ sensor fitted.")
st.markdown("""---""")
# Change to matplotlib

#with chart_container(df):

    #st.line_chart(chart)
#st.line_chart(df)

fig, ax = plt.subplots(1,1)
ax.plot(df, linewidth=1.0)
ax.set_xlabel('Samples')
ax.set_ylabel('Amplitude (g)')
#st.pyplot(fig)
fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=460)
st.columns(3)[1].caption("Data from one (1) ReVibe Anura™ sensor. X, Y, Z axis")

st.video(video2)
st.columns(3)[1].caption("Video of Anura harvesting sensor node running on ReVibe test machine")


st.subheader("No name real world vibrating screen sample data")
st.markdown("Dry run vibration data captured by ReVibe Anura™ on a real world screen.")
fig, ax = plt.subplots(1,1)
ax.plot(df2, linewidth=1.0)
ax.set_xlabel('Samples')
ax.set_ylabel('Amplitude (g)')
ax.legend()
#st.pyplot(fig)
fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=460)
st.columns(3)[1].caption("Data from one (1) ReVibe Anura™ sensor. X, Y, Z axis")

st.markdown("""---""")
st.columns(3)[1].write("ReVibe Energy AB 2023")
    