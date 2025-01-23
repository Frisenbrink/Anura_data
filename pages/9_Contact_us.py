import streamlit as st

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2025</p>
</div>"""

logo = "Materials/ReVibe.png"

st.columns(3)[1].image(logo)

def main():
    st.header("Contact us")
    
    st.markdown('We’d love to get in touch with you to answer any questions you may have.')
    st.write("Tel: +46 (0) 31 24 23 22")
    st.write("Email: contact@revibeenergy.com")

    st.divider()
    
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()