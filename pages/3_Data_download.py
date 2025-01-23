import streamlit as st
import os

logo = "Materials/ReVibe.png"
zip = "Anura_data.zip"
video = "Materials/Vibinspect_demo.mp4"

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2025</p>
</div>"""

st.columns(3)[1].image(logo)

st.header("Anura™ data download")
st.markdown("We are pleased to offer you access to a set of data that has been procured through ReVibe Anura™. The files, which are available for download below, contain a series of detailed measurements that have been collected using Anura sensors. To ensure that you can make the most of this data, we recommend that you use Vibinspect or your preferred software package to analyze the files. Please see the Vibinspect section for a primer into using vibration analysis software.")

def file_selector(folder_path='./sample_files'):
    filenames = os.listdir(folder_path)

    selected_filename = st.selectbox('Select a file', sorted(filenames))
    return os.path.join(folder_path, selected_filename)

filename = file_selector()

with open(filename, "rb") as fp:
    btn = st.columns(3)[1].download_button(label=(
        "Download selected file " + filename[15:]),
        data=fp,
        file_name=filename[7:],
        mime="application/zip"
    )
st.divider()
  
st.header("Vibinspect")
st.write("VibInspect vibration analysis software is a powerful tool for processing and visualization of acceleration data. The software can is free and open source and can be downloaded on https://revibeenergy.com/vibinspect-analysing-software/. You can use VibInspect to analyse the files provided in this package. The sample rate of the provided data is 832Hz and has a length of 3 seconds. Data from four (4) sensors is provided. They can be distinguished by their unique name in the following form (00_00_00_00_00_00) Every file comes with X,Y,Z axis data in the form of a .csv file. Please see video for tips on doing FFT and orbit plots.")

st.video(video)
st.columns(3)[1].caption("Short video primer on Vibinspect software")

st.write("0:00 - Open a Anura .csv file. Set samplerate and choose axes to plot. Select starting row")
st.write("0:30 - Make a FFT analysis")
st.write("0:50 - Make a Orbit plot")
st.divider()
st.markdown(footer_html, unsafe_allow_html=True)

    