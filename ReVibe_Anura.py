import base64
import streamlit as st


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
family = "Materials/anura.png"
screen = "Materials/Screen2.png"
video = "Materials/ReVibe_tease.mp4"
video2 = "Materials/ReVibe_Anura_Orange_ver1.mp4"

st.columns(3)[1].image(logo)

#st.cache()
def main():
    st.header("ReVibe Anura™ resources")
    #st.subheader("Introduction")
    st.markdown('This repository contains data and information that can be used as a reference or for in-depth analysis of the ReVibe Anura™ monitoring system for vibrating screens. It includes vibration data collected from circular motion machines, as well as examples of analysis software used to process and visualize the data from the system. The vibration data was collected under controlled conditions and provides insights into the performance of the Anura monitoring system in response to different types of motion.')
    #st.image(family, width=None, caption="ReVibe Anura™ system")
    st.video(video2, start_time=4)
    st.markdown("""---""")
    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()
