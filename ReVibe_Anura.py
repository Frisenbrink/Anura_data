import streamlit as st
import os

logo = "Materials/ReVibe.png"
zip = "Anura_data.zip"

st.columns(3)[1].image(logo, width=250)

def plot_csv_file():
    st.title("Plot CSV File with Matplotlib")

    # Allow user to upload a CSV file
    file = st.file_uploader("Choose a CSV file", type="csv")

    if file is not None:
        # Read the CSV file into a pandas dataframe
        df = pd.read_csv(file, skiprows=2, usecols=[0,1,2])

        # Plot the dataframe using Matplotlib
        fig, ax = plt.subplots()
        ax.plot(df)

        # Add axis labels and a title
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")
        ax.set_title("CSV Plot")

        # Display the plot using Streamlit
        st.pyplot(fig)



    root_dir = 'data'
    files = []
    for filename in os.listdir(root_dir):
        if filename.endswith(".csv"):
            files.append(os.path.join(root_dir, filename))
            continue
        else:
            continue
    # create a list of the dataframes
    dataframes = [pd.read_csv(f) for f in files]
    # create list of variables for each dataframe dynamically
    for i, df in enumerate(dataframes):
        globals()['data%s' % (i+1)] = df
    y_axis1 = []
    y_axis2 = []
    y_axis3 = []
    y_axis4 = []

    axis = 'Y'
    data1_timestamp = data1['X'][0]
    data2_timestamp = data2['X'][0]
    data3_timestamp = data3['X'][0]
    data4_timestamp = data4['X'][0]

    sample_rate1 = data1['Z'][0] / 10
    sample_rate2 = data2['Z'][0] / 10
    sample_rate3 = data3['Z'][0] / 10
    sample_rate4 = data4['Z'][0] / 10

    print("samplerate of data1:",sample_rate1)
    print("samplerate of data2:",sample_rate2)
    print("samplerate of data3:",sample_rate3)
    print("samplerate of data4:",sample_rate4)

    biggest_value = data1_timestamp
    if(data2_timestamp > biggest_value):
        biggest_value = data2_timestamp
    if(data3_timestamp > biggest_value):
        biggest_value = data3_timestamp
    if(data4_timestamp > biggest_value):
        biggest_value = data4_timestamp

    print(biggest_value)
    one_step_of_sample1 = 1000000 / sample_rate1
    one_step_of_sample2 = 1000000 / sample_rate2
    one_step_of_sample3 = 1000000 / sample_rate3
    one_step_of_sample4 = 1000000 / sample_rate4

    data1_start_from = int(round((biggest_value - data1_timestamp) / one_step_of_sample1))
    print("data1 starts from:",data1_start_from)
    data2_start_from = int(round((biggest_value - data2_timestamp) / one_step_of_sample2))
    print("data2 starts from:",data2_start_from)
    data3_start_from = int(round((biggest_value - data3_timestamp) / one_step_of_sample3))
    print("data3 starts from:",data3_start_from)
    data4_start_from = int(round((biggest_value - data4_timestamp) / one_step_of_sample4))
    print("data4 starts from:",data4_start_from)

    for i in range(0,data1['X'].size-data1_start_from-1):
        y_axis1.append(i*(1/sample_rate1))
    for i in range(0,data2['X'].size-data2_start_from-1):
        y_axis2.append(i*(1/sample_rate2))
    for i in range(0,data3['X'].size-data3_start_from-1):
        y_axis3.append(i*(1/sample_rate3))
    for i in range(0,data4['X'].size-data4_start_from-1):
        y_axis4.append(i*(1/sample_rate4))

    x_axis1 = []
    for i in range(1+data1_start_from,data1[axis].size):
        x_axis1.append(data1[axis][i])
    x_axis2 = []
    for i in range(1+data2_start_from,data2[axis].size):
        x_axis2.append(data2[axis][i])
    x_axis3 = []
    for i in range(1+data3_start_from,data3[axis].size):
        x_axis3.append(data3[axis][i])
    x_axis4 = []
    for i in range(1+data4_start_from,data4[axis].size):
        x_axis4.append(data4[axis][i])

    fig = plt.figure()
    plt.plot(y_axis1,x_axis1)
    plt.plot(y_axis2,x_axis2)
    plt.plot(y_axis3,x_axis3)
    plt.plot(y_axis4,x_axis4)
    plt.legend(files)
    #plt.show()
    #st.pyplot(fig)
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, width=1280, height=600)

st.cache()
def main():
    st.header("ReVibe Anura™ data")
    st.subheader("Introduction")
    st.markdown('This repository contains data and information that can be used as a reference or for in-depth analysis of the Anura sensoring system. It includes vibration data collected from both a circular motion rig and a linear shaker, as well as tips for software analysis. The vibration data was collected under controlled conditions and provides insights into the performance of the Anura sensoring system in response to different types of motion. The circular motion rig generated data for circular motion, while the linear shaker generated data for linear motion. This dataset can be used to compare and contrast the performance of the system under different types of motion. Additionally, the repository provides helpful tips for software analysis, including guidelines for data preprocessing, feature extraction, and modeling. These tips are aimed at helping users to effectively analyze the data and extract meaningful insights. Overall, this repository is a valuable resource for anyone interested in the Anura sensoring system, and can be used for a range of purposes, including research, testing, and development.')
    st.markdown("""---""")
    st.markdown("We are pleased to offer you access to a set of data that has been procured through our proprietary technology, Anura™. The files, which are available for download below, contain a series of detailed measurements that have been collected using advanced measurement techniques. To ensure that you can make the most of this data, we recommend that you use Vibinspect or your preferred software package to analyze the files. With the help of these powerful tools, you will be able to gain a deeper understanding of the data and identify important trends, patterns, and insights that can inform your decision-making. We understand that analyzing large amounts of data can be a daunting task, but we are confident that the quality and accuracy of our measurements will make the process as smooth and efficient as possible. Whether you are an experienced analyst or a novice user, we believe that you will find these files to be a valuable resource that can help you unlock new insights and opportunities in your work. Thank you for your interest in our data, and we look forward to hearing about your analysis and findings. If you have any questions or feedback, please do not hesitate to contact us.")
    with open("Materials/Anura_data.zip", "rb") as fp:
        btn = st.download_button(
            label="Download Anura™ example data files",
            data=fp,
            file_name="Anura_data.zip",
            mime="application/zip"
        )
    st.markdown("""---""")
    st.columns(3)[1].write("ReVibe Energy AB 2023")

if __name__ == '__main__':
    main()