import streamlit as st
import os
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
zip = "Anura_data.zip"

st.columns(3)[1].image(logo, width=300)



st.cache()
def main():
    st.header("ReVibe Anura™ data")
    st.subheader("Introduction")
    st.markdown('This repository contains data and information that can be used as a reference or for in-depth analysis of the Anura sensoring system. It includes vibration data collected from both a circular motion rig and a linear shaker, as well as tips for software analysis. The vibration data was collected under controlled conditions and provides insights into the performance of the Anura sensoring system in response to different types of motion.')
    st.markdown("""---""")
    st.markdown("We are pleased to offer you access to a set of data that has been procured through Anura™. The files, which are available for download below, contain a series of detailed measurements that have been collected using Anura sensors. To ensure that you can make the most of this data, we recommend that you use Vibinspect or your preferred software package to analyze the files. Please see the Vibinspect section for a primer into using vibration analysis software.")
    with open("Materials/Anura_data.zip", "rb") as fp:
        btn = st.download_button(
            label="Download Anura™ example data files",
            data=fp,
            file_name="Anura_data.zip",
            mime="application/zip"
        )
    st.markdown("""---""")
    st.columns(3)[1].write("ReVibe Energy AB 2023")

if __name__ == '__main__':
    main()