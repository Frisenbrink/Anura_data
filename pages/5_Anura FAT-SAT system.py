import streamlit as st
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
family = "Materials/FAT_picture.png"
zip = "Anura_data.zip"

st.columns(3)[1].image(logo)



st.cache()
def main():
    st.header("Anura FAT/SAT system")
    #st.subheader("API")
    st.markdown('Anura FAT/SAT system is a free and open source software for Factory Acceptance Testing and Site Acceptance Testing. Click the button below to download a sample FAT report.')
    with open("Materials/FAT_report.pdf", "rb") as fp:
        btn = st.columns(3)[1].download_button(
            label="Download FAT report",
            data=fp,
            file_name="FAT_report.pdf",
            mime="application/pdf"
        )
    st.image(family, width=None, caption="ReVibe Anura™ system")
    st.markdown("""---""")
    
    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()