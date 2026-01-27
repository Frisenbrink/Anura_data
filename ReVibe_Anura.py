import streamlit as st

family = "Materials/anura.png"

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2025</p>
</div>"""

def main():
    st.image(family, width=800, caption="ANURA™ Remote Monitoring Kit")

    st.header("ANURA™ Monitoring Platform")
    st.markdown(
        """ANURA™ is an industrial monitoring platform for vibrating screens and feeders, combining wireless vibration sensors, supporting hardware, and software applications across field, on-premises, and remote monitoring environments. The platform enables continuous condition and process monitoring, with options ranging from self-powered sensing to battery-driven and integrated systems, delivering reliable insight wherever it is needed."""
    )
    video_path = "Materials/ReVibe_Anura_Orange_ver1.mp4"
    st.video(video_path, start_time=1)

    st.divider()
    video_path = "Materials/ReVibe_click_English.mov"
    st.video(video_path, start_time=1)

    st.divider()
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
