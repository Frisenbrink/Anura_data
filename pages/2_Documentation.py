import os
import re
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2026</p>
</div>"""

def main():

    st.markdown('The documentation is available at https://docs.revibeenergy.com/index.html')

    st.divider()
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
