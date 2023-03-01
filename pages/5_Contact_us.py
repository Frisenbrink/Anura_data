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
family = "Materials/anura.png"
zip = "Anura_data.zip"

st.columns(3)[1].image(logo)



st.cache()
def main():
    st.header("Contact us")
    
    st.markdown('We’d love to get in touch with you to answer any questions you may have. Fill out the form below or reach out via phone or email.')
    st.write("Tel: +46 (0) 31 24 23 22")
    st.write("Email: contact@revibeenergy.com")
    with st.form("form1", clear_on_submit=True):
        Name = st.text_input("Enter your full name")
        email = st.text_input("Enter email")
        message = st.text_area("Question")

        submit = st.form_submit_button("Submit question")

    st.markdown("""---""")
    
    st.columns(3)[1].write("ReVibe Energy AB 2023")

if __name__ == '__main__':
    main()