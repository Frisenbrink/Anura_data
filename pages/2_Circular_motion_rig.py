import streamlit as st
import pandas as pd
from streamlit_extras.chart_container import chart_container

logo = "Materials/ReVibe.png"
video2 = "Materials/Circular.mp4"

df = pd.read_csv("Circular_motion/00_80_e1_26_e7_16/1673620685.csv", skiprows=2, usecols=[0,1,2])

st.columns(3)[1].image(logo, width=250)

st.header("Circular motion rig")
st.markdown("Used by ReVibe for development purposes. Due to it’s size and requirement for mobility, the circular motion is not a clean signal. But is susceptible to noise in the form of motion/vibrations of the whole machine.")
    
# Change to matplotlib

with chart_container(df):
    
    st.markdown("Data from 4 Anura sensors")
    #st.line_chart(chart)
    st.line_chart(df)

st.video(video2)


st.markdown("""---""")
st.columns(3)[1].write("ReVibe Energy AB 2023")
    