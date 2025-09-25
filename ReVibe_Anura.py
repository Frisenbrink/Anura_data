import streamlit as st

family = "Materials/anura.png"

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2025</p>
</div>"""

def main():
    st.image(family, width=800, caption="ReVibe Anura™ system")

    st.header("Anura™ monitoring system")
    st.markdown(
        """A self-powered, fit-and-forget industrial monitoring system designed to track the status of vibrating screens. 
        The system transmits data wirelessly to cloud services, allowing users to access real-time information, 
        assess screen conditions, and take action to prevent potential breakdowns, enabling maintenance planning well in advance. 
        Combined with advanced analysis tools for optimizing performance and flow rates, 
        the ReVibe Anura™ is the preferred solution for operators. 
        This repository contains data and resources that serve as a reference or for in-depth analysis of the ReVibe Anura™ 
        monitoring system for vibrating screens."""
    )
    video_path = "Materials/ReVibe_Anura_Orange_ver1.mp4"
    #st.video(video_path, start_time=1)

    st.divider()
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
