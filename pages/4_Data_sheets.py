import base64
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import os
import re


PDF1 = "./Materials/10064_Datasheet.pdf"
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

st.columns(3)[1].image(logo)

#st.cache()
def main():

    st.header("ReVibe Anura™ data sheets")
    st.markdown('This repository contains data and information that can be used as a reference or for in-depth analysis of the ReVibe Anura™ monitoring system for vibrating screens. It includes vibration data collected from circular motion machines, as well as examples of analysis software used to process and visualize the data from the system. The vibration data was collected under controlled conditions and provides insights into the performance of the Anura monitoring system in response to different types of motion.')
    
    def sort_key(filename):
        parts = re.split(r'(\d+)', filename)
        return [int(part) if part.isdigit() else part for part in parts]

    def file_selector(folder_path='./pdf'):
        filenames = os.listdir(folder_path)

        selected_filename = st.selectbox('Select a file', sorted(filenames, key=sort_key))
        return os.path.join(folder_path, selected_filename)

    filename = file_selector()
    
    pdf_viewer(filename)

    st.markdown("""---""")
    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()
