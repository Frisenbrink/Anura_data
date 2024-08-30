import base64
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import os
import re

def add_bg_from_local(image_file):
    """Sets a background image for the Streamlit app."""
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def sort_key(filename):
    """Sorts filenames in a natural order (e.g., file2 before file10)."""
    parts = re.split(r'(\d+)', filename)
    return [int(part) if part.isdigit() else part for part in parts]

def list_pdfs(folder_path='./pdf'):
    """Lists all PDF files in the designated folder."""
    filenames = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')],
        key=sort_key
    )
    return filenames

def main():

    # Set background and logo
    #add_bg_from_local('Materials/frog.png')
    st.columns(3)[1].image("Materials/ReVibe.png")

    st.header("Anura™ Datasheets & Manuals")
    st.markdown(
        """This repository contains data and information that can be used as a 
        reference or for in-depth analysis of the ReVibe Anura™ monitoring system 
        for vibrating screens. It includes vibration data collected from circular 
        motion machines, as well as examples of analysis software used to process 
        and visualize the data from the system. The vibration data was collected 
        under controlled conditions and provides insights into the performance of 
        the Anura monitoring system in response to different types of motion."""
    )

    # List PDFs in the specified folder
    folder_path = './pdf'
    pdf_files = list_pdfs(folder_path)
    
    # Display PDFs in a 3-column grid layout
    cols = st.columns(3)
    for i, pdf_file in enumerate(pdf_files):
        with cols[i % 3]:
            filename = os.path.join(folder_path, pdf_file)
            
            # Display PDF thumbnail (first page)
            pdf_viewer(filename, pages_to_render=[1])
            
            # Download link
            with open(filename, "rb") as fp:
                st.download_button(
                    label=f"Download {pdf_file}",
                    data=fp,
                    file_name=pdf_file,
                    mime="application/pdf"
                )
        
        # Start a new row after every 3 PDFs
        if (i + 1) % 3 == 0:
            cols = st.columns(3)
    
    st.divider()
    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()
