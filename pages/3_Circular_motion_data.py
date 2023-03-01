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

df = pd.read_csv("Circular_motion/00_80_e1_26_e7_16/1673620685.csv", skiprows=2, usecols=[0,1,2])
df2 = pd.read_csv("No_name/00_80_e1_26_e7_16/1674153368.csv", skiprows=2, usecols=[0,1,2])

st.columns(3)[1].image(logo)

st.header("Circular motion data")
st.subheader("ReVibe test machine")
st.markdown("A circular motion machine designed by ReVibe for development purposes. Due to it’s size and requirement for mobility, the circular motion is not a clean signal. But is susceptible to noise in the form of motion/vibrations of the whole machine.")
    
# Change to matplotlib

#with chart_container(df):
    
st.write("Data from one (1) ReVibe Anura™ sensor. X, Y, Z axis")
    #st.line_chart(chart)
#st.line_chart(df)

fig, ax = plt.subplots(1,1)
ax.plot(df, linewidth=1.0)
ax.set_xlabel('Samples')
ax.set_ylabel('Amplitude (g)')
#st.pyplot(fig)
fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, width=1280, height=600)

st.write("Video of Anura harvesting sensor node running on ReVibe test machine")
st.video(video2)

st.subheader("No name real world vibrating screen")
st.markdown("Dry run vibration data captured bu ReVibe Anura™ on a real world screen.")
st.write("Data from one (1) ReVibe Anura™ sensor. X, Y, Z axis")
fig, ax = plt.subplots(1,1)
ax.plot(df2, linewidth=1.0)
ax.set_xlabel('Samples')
ax.set_ylabel('Amplitude (g)')
ax.legend()
#st.pyplot(fig)
fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, width=1280, height=600)

st.markdown("""---""")
st.columns(3)[1].write("ReVibe Energy AB 2023")
    