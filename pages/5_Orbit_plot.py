import streamlit as st
import numpy as np #Imports Python mathematical functions library
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components

logo = "Materials/ReVibe.png"

video = "Materials/Vibinspect_demo.mp4"
zip = "Anura_data.zip"

#x = np.genfromtxt("Circular_motion/00_80_e1_26_e7_16/1673620685.csv", delimiter=",", skip_header=2, usecols=[0])
#y = np.genfromtxt("Circular_motion/00_80_e1_26_e7_16/1673620685.csv", delimiter=",", skip_header=2, usecols=[1])

st.columns(3)[1].image(logo, width=250)

st.header("Orbit plot")

R = 1

n = 63

t = np.linspace(0, 2*np.pi, n+1)

x = R*np.cos(t)
y = R*np.sin(t)

fig = plt.figure()
plt.axis("equal")
plt.grid()
plt.plot(x, y)
fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=800)
    