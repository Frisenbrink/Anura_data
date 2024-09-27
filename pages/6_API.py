import streamlit as st

logo = "Materials/ReVibe.png"
family = "Materials/anura2_half.png"

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2024</p>
</div>"""

st.columns(3)[1].image(logo)

st.cache()
def main():
    st.header("Loqui REST API")
    #st.subheader("API")
    st.markdown('The Loqui API enables seamless communication with the ReVibe Anura vibration energy harvesting system, offering a robust interface for monitoring, managing, and controlling device operations. Through this RESTful API, users can access real-time data, configure system settings, and integrate Anura with various applications and platforms. Designed with flexibility and scalability in mind, the Loqui API simplifies integration for developers, allowing for efficient remote interaction with the Anura system. Explore the full API documentation to learn how to harness the power of Loqui for your energy harvesting solutions.')
    st.markdown('https://revibe-energy.github.io/loqui-api/prod/#/')

    st.image(family, width=None, caption="ReVibe Anura™ system")

    st.divider()
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()