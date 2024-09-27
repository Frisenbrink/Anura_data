import os
import re
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2024</p>
</div>"""

def extract_version(filename):
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', filename)
    if match:
        return tuple(map(int, match.groups()))
    return (0, 0, 0)

def filter_latest_versions(filenames):
    latest_versions = {}
    
    for filename in filenames:
        base_name = re.sub(r'\d+\.\d+\.\d+', '', filename).strip('_-.')
        version = extract_version(filename)
        
        if base_name not in latest_versions or version > latest_versions[base_name][1]:
            latest_versions[base_name] = (filename, version)
    
    return [filename for filename, version in latest_versions.values()]

def list_pdfs(folder_path='./pdf'):
    filenames = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')],
        key=sort_key
    )
    
    return filter_latest_versions(filenames)

def sort_key(filename):
    parts = re.split(r'(\d+)', filename)
    return [int(part) if part.isdigit() else part for part in parts]

def main():

    st.columns(3)[1].image("Materials/ReVibe.png")

    st.header("Anura™ documentation")
    st.markdown(
        """
This section provides access to all relevant manuals and datasheets for the Anura vibration energy harvesting system, available for download in PDF format. These documents offer comprehensive guidance on system installation, configuration, and performance optimization, as well as detailed technical specifications. To ensure proper integration and operation of the Anura system, please refer to the latest manuals and datasheets provided below."""
    )

    folder_path = './pdf'
    pdf_files = list_pdfs(folder_path)
    
    cols = st.columns(3)
    for i, pdf_file in enumerate(pdf_files):
        with cols[i % 3]:
            filename = os.path.join(folder_path, pdf_file)
            
            pdf_viewer(filename, pages_to_render=[1])
            
            with open(filename, "rb") as fp:
                st.download_button(
                    label=f"Download {pdf_file}",
                    data=fp,
                    file_name=pdf_file,
                    mime="application/pdf"
                )
        
        if (i + 1) % 3 == 0:
            cols = st.columns(3)
    
    st.divider()
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
