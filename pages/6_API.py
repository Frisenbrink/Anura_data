import streamlit as st
import base64

logo = "Materials/ReVibe.png"
family = "Materials/anura2.png"

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

#add_bg_from_local('Materials/frog.png') 

st.columns(3)[1].image(logo)

st.cache()
def main():
    st.header("Loqui REST API")
    #st.subheader("API")
    st.markdown('ANURA Loqui REST API is an API used to configure the Anura sensor system. Follow the link below for a detailed description of the API')
    st.markdown('https://revibe-energy.github.io/loqui-api/prod/#/')
    st.divider()

    st.image(family, width=None, caption="ReVibe Anura™ system")

    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()