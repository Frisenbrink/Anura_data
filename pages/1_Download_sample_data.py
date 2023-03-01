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
screen = "Materials/Screen.png"
zip = "Anura_data.zip"

st.columns(3)[1].image(logo)



st.cache()
def main():
    st.header("Download ReVibe Anura™ sample data")
    st.markdown("We are pleased to offer you access to a set of data that has been procured through ReVibe Anura™. The files, which are available for download below, contain a series of detailed measurements that have been collected using Anura sensors. To ensure that you can make the most of this data, we recommend that you use Vibinspect or your preferred software package to analyze the files. Please see the Vibinspect section for a primer into using vibration analysis software.")
    with open("Materials/Anura_data.zip", "rb") as fp:
        btn = st.download_button(
            label="Download Anura™ sample data files",
            data=fp,
            file_name="Anura_data.zip",
            mime="application/zip"
        )
    
    st.image(screen, caption="Vibrating screen with ReVibe Anura™ sensor fitted.")
    st.markdown("""---""")
    st.columns(3)[1].write("ReVibe Energy AB 2023")

if __name__ == '__main__':
    main()