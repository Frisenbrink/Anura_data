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

    config = {'displaylogo': False}

    st.header("ReVibe test installation")
    st.write("ReVibe Anura reference installation in the city of Gothenburg")
    st.image(screen, caption="Vibrating screen with ReVibe Anura™ sensor fitted.")
    
    st.video(video)
    st.columns(3)[1].caption("Anura installation")

    st.markdown("""---""")

    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()
