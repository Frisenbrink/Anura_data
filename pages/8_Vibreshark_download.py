import streamlit as st
import requests
import re

logo = "Materials/ReVibe.png"

st.columns(3)[1].image(logo)

vibreshark = "Materials/Vibreshark_laptop_tablet.png"

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2025</p>
</div>"""

INDEX_URL = "https://vibreshark-releases-eu-central-1-115273158856.s3.eu-central-1.amazonaws.com/index.json"
BASE_URL = "https://vibreshark-releases-eu-central-1-115273158856.s3.eu-central-1.amazonaws.com/"
CHANGELOG_URL = f"{BASE_URL}stable/CHANGELOG.md"

def get_latest_version():
    """Fetch index.json, filter out RC versions, and return the latest version."""
    response = requests.get(INDEX_URL)
    if response.status_code == 200:
        versions = response.json().get("versions", [])

        # Ta bort RC
        stable_versions = [v for v in versions if not re.search(r"-rc\d*", v)]

        if stable_versions:
            stable_versions.sort(key=lambda v: list(map(int, re.findall(r"\d+", v))))
            return stable_versions[-1]
    return None

st.header("Vibreshark")
st.image(vibreshark, caption="Vibreshark application")

st.markdown('Capture vibration data and transform it into actionable insights with Vibreshark’s powerful visualization capabilities.')

latest_version = get_latest_version()
if latest_version:
    download_link = f"{BASE_URL}{latest_version}"
    st.success(f"Latest version: {latest_version.replace('vibreshark-', '').replace('.msi', '')}")
    st.markdown(f"[Download Vibreshark Installer]({download_link})", unsafe_allow_html=True)
else:
    st.error("No stable versions found. Please check back later.")

# changelog.md
try:
    changelog_response = requests.get(CHANGELOG_URL)
    if changelog_response.status_code == 200:
        changelog_text = changelog_response.text
        st.markdown(f"[Download changelog.md]({CHANGELOG_URL})", unsafe_allow_html=True)
        st.markdown(changelog_text)
    else:
        st.warning("Changelog not available at the moment.")
except Exception as e:
    st.error(f"Failed to fetch changelog: {e}")

st.divider()

st.markdown(footer_html, unsafe_allow_html=True)
