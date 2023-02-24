import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components
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

x1 = np.genfromtxt("Circular_motion/00_80_e1_26_e7_16/1673620685.csv", delimiter=",", skip_header=2, usecols=[1])
y1 = np.genfromtxt("Circular_motion/00_80_e1_26_e7_16/1673620685.csv", delimiter=",", skip_header=2, usecols=[1])

st.columns(3)[1].image(logo, width=300)

st.header("Orbit plot")

R = 1

n = len(y1/3)

t = np.linspace(0, 2*np.pi, n)

x = y1*np.cos(t)
y = y1*np.sin(t)

fig = plt.figure()
plt.axis("equal")
#plt.grid()
plt.plot(x, y)
fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=800)