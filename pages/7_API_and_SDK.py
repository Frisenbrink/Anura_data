import streamlit as st

logo = "Materials/ReVibe.png"
family = "Materials/anura2_half.png"

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2025</p>
</div>"""

st.columns(3)[1].image(logo)

def main():
    st.header("Loqui REST API")
    #st.subheader("API")
    st.markdown('The Loqui API enables seamless communication with the ReVibe Anura vibration energy harvesting system, offering a robust interface for monitoring, managing, and controlling device operations. Through this RESTful API, users can access real-time data, configure system settings, and integrate Anura with various applications and platforms. Designed with flexibility and scalability in mind, the Loqui API simplifies integration for developers, allowing for efficient remote interaction with the Anura system. Explore the full API documentation to learn how to harness the power of Loqui for your energy harvesting solutions.')
    st.markdown('https://revibe-energy.github.io/loqui-api/prod/#/')

    #st.image(family, width=None, caption="ReVibe Anura™ system")

    st.divider()

    st.header("Anura™ Python SDK")

    st.markdown("""
    The Anura Python Software Development Kit (SDK) provides developers with a powerful and flexible toolset for integrating and interacting with the ReVibe Anura vibration energy harvesting system. With this SDK, you can seamlessly access and manage real-time data, customize system configurations, and develop tailored applications to maximize the performance of the Anura system. Designed for ease of use and versatility, the Anura Python SDK enables both rapid prototyping and advanced integration, making it an essential resource for optimizing your energy harvesting projects. Explore the documentation and resources to get started.
    
    Download the PyAnura SDK https://github.com/ReVibe-Energy/pyanura/tree/main
                
    # pyanura Package

    The pyanura package contains classes and command line utilities for interfacing
    the ReVibe Anura sensors and transceivers.

    ## Installing the package for programmatic use

    The package is installable using `pip3` by pointing to the top level directory (the one containing this README file).
    First you should set up and actiavte a suitable virtual environment for your project.
    After that you can install the pyanura package using `pip3`.

    Example (assuming the package is located in the Downloads directory):

        pip3 install ~/Downloads/pyanura

    Or with optional CLI dependencies included:

        pip3 install ~/Downloads/pyanura[cli]

    ## Installing command-line interface

    If you just want to install the `anura` command-line utility and make it available
    on your `PATH` the best option is likely to install `pipx` using your system's package
    manager and then install `pyanura` using `pipx`.

        pipx install ~/Downloads/pyanura[cli]

    Using this method you don't have to manually set up a virtual environment as `pipx`
    will create one for you. Additionally it will add a script to your `PATH` that will
    launch the command-line in the appropriate virtual environment.


    ## Development setup

    For development in the  `pyanura` repository you should setup a virtual environment in which you will install the dependencies of `pyanura` but not the `pyanura` package itself.

    Assuming you have activated a suitable a virtual environment, install the dendencies as follows:

        pip3 install -r requirements.txt

    (Optional) Install extra requirements needed to run the examples under `/examples`.

        pip3 install -r requirements-extras.txt

    After that you should be able to launch the `anura` command-line interface with the following command:

        python3 -m anura.cli


    ## Running an example

    Assuming you have activated a virtual environment with all the required
    dependencies you can launch the examples from the `pyanura` root directory
    as follows:

    python3 -m examples.forwarder --config examples/forwarder/example-config.json
    """)
    st.divider()
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()