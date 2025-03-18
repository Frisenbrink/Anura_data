import streamlit as st
import requests
import re

def find_latest_version(base_url, base_version="0_19_0"):
    major, minor, patch = map(int, base_version.split("_"))
    latest_version = base_version
    
    while True:
        next_patch = f"{major}_{minor}_{patch + 1}"
        test_url = f"{base_url}vibreshark-{next_patch}.msi"
        response = requests.head(test_url)
        
        if response.status_code == 200:
            latest_version = next_patch
            patch += 1
        else:
            break
    
    return latest_version

# Streamlit UI
st.title("Vibreshark Latest Release")
base_url = "https://vibreshark-releases-eu-central-1-115273158856.s3.eu-central-1.amazonaws.com/"
base_version = "0_19_0"

latest_version = find_latest_version(base_url, base_version)
download_link = f"{base_url}vibreshark-{latest_version}.msi"

st.success(f"Latest version: {latest_version}")
st.markdown(f"[Download Here]({download_link})")
