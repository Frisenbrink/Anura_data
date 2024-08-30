import base64
import streamlit as st

def add_background(image_path):
    """Sets a background image for the Streamlit app."""
    with open(image_path, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    # Set background image
    #add_background('Materials/frog.png')

    # Display the logo centered at the top
    logo_path = "Materials/ReVibe.png"
    st.columns(3)[1].image(logo_path)

    # Header and description
    st.header("Anura™ Resources")
    st.markdown(
        """This repository contains data and information that can be used as a reference or 
        for in-depth analysis of the ReVibe Anura™ monitoring system for vibrating screens. 
        It includes vibration data collected from circular motion machines, as well as examples 
        of analysis software used to process and visualize the data from the system. The vibration 
        data was collected under controlled conditions and provides insights into the performance 
        of the Anura monitoring system in response to different types of motion."""
    )

    # Display video with a start time
    video_path = "Materials/ReVibe_Anura_Orange_ver1.mp4"
    st.video(video_path, start_time=4)

    # Divider and footer text
    st.divider()
    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()
