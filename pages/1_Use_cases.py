import streamlit as st
import base64
import os

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
screen = "Materials/Screen2.png"
zip = "Anura_data.zip"
video = "Materials/Vibinspect_demo.mp4"

st.columns(3)[1].image(logo)

st.header("Download ReVibe Anura™ sample data")
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
st.markdown("""---""")
my_expander = st.expander(label='Info about Vibinspect')
with my_expander:
    #'Hello there!'
    #clicked = st.button('Click me!')
    
    st.header("Vibinspect")
    st.write("VibInspect vibration analysis software is a powerful tool for processing and visualization of acceleration data. The software can is free and open source and can be downloaded on https://revibeenergy.com/vibinspect-analysing-software/. You can use VibInspect to analyse the files provided in this package. The sample rate of the provided data is 832Hz and has a length of 3 seconds. Data from four (4) sensors is provided. They can be distinguished by their unique name in the following form (00_00_00_00_00_00) Every file comes with X,Y,Z axis data in the form of a .csv file. Please see video for tips on doing FFT and orbit plots.")

    st.video(video)
    st.columns(3)[1].caption("Short video primer on Vibinspect software")

    st.write("0:00 - Open a Anura .csv file. Set samplerate and choose axes to plot. Select starting row")
    st.write("0:30 - Make a FFT analysis")
    st.write("0:50 - Make a Orbit plot")
st.markdown("""---""")
my_expander = st.expander(label='Test section')
with my_expander:
    
    st.header("Test")
    st.write("Sed vel porttitor nisl, sit amet malesuada leo. Integer tempus, diam accumsan ultricies gravida, massa dolor vestibulum felis, eget condimentum leo odio eu nulla. Morbi commodo pellentesque massa lobortis placerat. Nam tincidunt nisi nec ipsum sollicitudin auctor. Nam fringilla dictum massa et congue. Nam imperdiet, nulla non tempus pharetra, massa leo congue enim, nec porttitor lectus nisi vel nunc. Etiam at mauris sit amet ipsum elementum consectetur ac in augue. Maecenas dolor nibh, viverra in scelerisque vitae, mollis at risus. Fusce et sapien commodo, bibendum tellus et, vehicula sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean nec magna vitae eros faucibus ullamcorper vitae eget mi. Nullam vehicula dignissim volutpat. Proin vel maximus justo, vel egestas nunc. Pellentesque at tortor bibendum, finibus enim sit amet, molestie orci. Fusce eget sem magna. Sed nibh metus, sagittis tincidunt magna eu, sodales lobortis ligula.")

st.markdown("""---""")
st.columns(3)[1].write("ReVibe Energy AB 2024")
    