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

st.columns(3)[1].image(logo, width=300)

st.header("ReLog")
st.markdown("Step by step guide")
st.markdown("“Although the bump test is one of the most fundamental methods used to determine the natural frequencies of a structure, not much literature is available regarding the detailed procedures and techniques required for an accurate reading of natural frequencies. A series of recommended practices for conducting a successful bump test are summarized in this article. An example illustrates their application for the accurate assessment of natural frequencies. If an exciting frequency matches a structural natural frequency, resonance occurs. At resonance, vibration amplitude can be controlled only by damping; however, artificially-introduced damping is not preferred because it consumes energy. In general, resonance should be avoided in any system. In addition, structural natural frequencies should be separated from potential exciting frequencies. A 15% separation margin is commonly recommended [1] although a 20% margin is advisable in some specific applications; e.g., the special purpose gear unit in API Standard 613 [2]. An accurate reading of structural natural frequencies of a system with a bump test is a prerequisite to any code-compliant system design or design modification. Instrumentation for a Bump Test The following instrumentation is required to carry out a bump test. FFT (Fast Fourier Transform) vibration analyzer with cross-channel functions such as transfer function and coherence features [3]. Instrumented hammer (a hammer with a force sensor embedded inside) with multiple tips of different size and hardness. Vibration sensors; e.g. accelerometer. Careful selection of a suitable hammer and tip is important for a successful bump test. In general, a softer (often also larger) hammer tip provides higher amplitudes of exciting frequency components of the impact force, a narrower force spectrum, and a lower exciting frequency. Figure 1 contains a series of sample frequency response curves for an impact hammer with tips of different size and hardness. For a specific hammer, a detailed frequency response curve supplied by the manufacturer is needed to choose a suitable hammer and tip for the proposed impact test. Recommended Practices for a Bump Test: These practices for implementing a successful bump test result from extensive research and discussions with practicing vibration specialists. When the hammer is struck, avoid middle or end positions of the structure. They may be nodal points of the lower fundamental natural frequencies. Do not strike too hard; try to stay within the linear elastic regime of the structure. Strike gently at first, then gradually harder if necessary. Check the impact force time waveform; a double hit will appear as a double peak.")