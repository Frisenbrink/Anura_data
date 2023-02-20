import streamlit as st
logo = "Materials/ReVibe.png"

video = "Materials/Vibinspect_demo.mp4"
zip = "Anura_data.zip"


st.columns(3)[1].image(logo, width=250)

st.header("Vibinspect")
st.write("ReVibe software package used for powerful analysis of signals. Download for free on https://revibeenergy.com/vibinspect-analysing-software/ Use this to analyse the files provided in this package. The samplerate of the provided data is 832Hz and has a length of 3 seconds. Data from four (4) sensors is provided they can be distinguished by their unique name in the following form (00_00_00_00_00_00) Every file comes with X,Y,Z axis data in the form of a .csv file. Please see video for tips on doing FFT and orbit plots")
st.video(video)

st.markdown("""---""")
st.write("The files available below are measurements procurred through Anura™. Please download and analyze these files with Vibinspect or preferred software package.")
with open("Materials/Anura_data.zip", "rb") as fp:
    btn = st.download_button(
        label="Download Anura™ example data files",
        data=fp,
        file_name="Anura_data.zip",
        mime="application/zip"
)

st.markdown("""---""")
st.columns(3)[1].write("ReVibe Energy AB 2023")
    