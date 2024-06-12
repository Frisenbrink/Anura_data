import base64
import streamlit as st


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
family = "Materials/anura.png"
screen = "Materials/Screen2.png"
video = "Materials/ReVibe_tease.mp4"
video2 = "Materials/ReVibe_Anura_Orange_ver1.mp4"

st.columns(3)[1].image(logo)

#st.cache()
def main():

    config = {'displaylogo': False}

    st.header("ReVibe test installation")
    st.write("Schaktmassor får nytt liv. Vid byggnation av hus och vägar uppstår ofta ett överskott av schaktmassor. Dessa massor består inte sällan av brukbar jord. Vi sorterar den och erbjuder ett antal jordprodukter som anpassas utifrån det specifika ändamålet. Återvinning av betong och asfalt. Genom att ta emot och krossa betong eller asfalt från anläggningsprojekt i samhället, och blanda med bergkrossprodukter, går det att minska samhällets deponivolymer, minska uttaget av jungfruligt material och samtidigt spara pengar. Betong och asfalt återvinns bland annat vid rivning av gamla byggnader och i samband med att gamla vägar bryts upp eller repareras. Ofta hamnar materialet på deponi. Att istället återvinna materialet gynnar både miljön och samhället.")

    st.image(screen, caption="Vibrating screen with ReVibe Anura™ sensor fitted.")
    st.write("Sed vel porttitor nisl, sit amet malesuada leo. Integer tempus, diam accumsan ultricies gravida, massa dolor vestibulum felis, eget condimentum leo odio eu nulla. Morbi commodo pellentesque massa lobortis placerat. Nam tincidunt nisi nec ipsum sollicitudin auctor. Nam fringilla dictum massa et congue. Nam imperdiet, nulla non tempus pharetra, massa leo congue enim, nec porttitor lectus nisi vel nunc. Etiam at mauris sit amet ipsum elementum consectetur ac in augue. Maecenas dolor nibh, viverra in scelerisque vitae, mollis at risus.")

    st.video(video)
    st.columns(3)[1].caption("Anura installation")

    st.markdown("""---""")

    st.columns(3)[1].write("ReVibe Energy AB 2024")

if __name__ == '__main__':
    main()
