import streamlit as st
import numpy as np #Imports Python mathematical functions library
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



logo = "Materials/ReVibe.png"

video = "Materials/Vibinspect_demo.mp4"
zip = "Anura_data.zip"


st.columns(3)[1].image(logo, width=250)

st.header("Orbit plot")

cos = np.cos
pi = np.pi

a = 5
e = 0.3
theta = np.linspace(0,2*pi, 360)
r = (a*(1-e**2))/(1+e*cos(theta))
fig = plt.figure()
plt.polar(theta, r)

print(np.c_[r,theta])

plt.show()
