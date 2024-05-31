import streamlit as st
logo = "Materials/ReVibe.png"

video = "Materials/Vibinspect_demo.mp4"
zip = "Anura_data.zip"
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

st.columns(3)[1].image(logo)

st.header("Vibinspect")
st.write("VibInspect vibration analysis software is a powerful tool for processing and visualization of acceleration data. The software can is free and open source and can be downloaded on https://revibeenergy.com/vibinspect-analysing-software/. You can use VibInspect to analyse the files provided in this package. The sample rate of the provided data is 832Hz and has a length of 3 seconds. Data from four (4) sensors is provided. They can be distinguished by their unique name in the following form (00_00_00_00_00_00) Every file comes with X,Y,Z axis data in the form of a .csv file. Please see video for tips on doing FFT and orbit plots.")

st.video(video)
st.columns(3)[1].caption("Short video primer on Vibinspect software")

st.write("0:00 - Open a Anura .csv file. Set samplerate and choose axes to plot. Select starting row")
st.write("0:30 - Make a FFT analysis")
st.write("0:50 - Make a Orbit plot")



st.markdown("""---""")

st.columns(3)[1].write("ReVibe Energy AB 2024")
    