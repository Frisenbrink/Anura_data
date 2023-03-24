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
manual = "Materials/Anura_manual_compressed.pdf"
zip = "Anura_data.zip"

st.columns(3)[1].image(logo)

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


st.cache()
def main():
    st.header("ReVibe Anura™ Manual")
    
    show_pdf(manual)
    st.markdown("""---""")
    
    st.columns(3)[1].write("ReVibe Energy AB 2023")

if __name__ == '__main__':
    main()