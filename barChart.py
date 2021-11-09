import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# sns.set_theme(style="whitegrid")
# ax2 = sns.barplot(x="", y="", data="")

def create_graph():
    plt.figure(figsize=(2, 2))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(data=df)
    # ax.set(xlim=(0, 1))
    plt.xticks(rotation = 90)
    st.pyplot(plt)

def imagedownload(plt, filename):
    s = io.BytesIO()
    plt.savefig(s, format='pdf', bbox_inches='tight')
    plt.close()
    b64 = base64.b64encode(s.getvalue()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

# Side bar
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
st.sidebar.header("1. Upload your CSV data")
uploader = st.sidebar.file_uploader("Upload your input CSV file", help="Upload your dataset file here", type=['csv','xlsx'])
with st.sidebar.header('2. Set Parameters'):
    split_size = st.sidebar.slider('Data split ratio (% for Training Set)', 10, 90, 80, 5)
    seed_number = st.sidebar.slider('Set the random seed number', 1, 100, 42, 1)
# /Sidebar

# Main page
st.title("Millennium Square AutoML")
last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)
# /Main page

# Progress bar
# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)
#
# progress_bar.empty()
# /Progress bar

# Dataset
if uploader is not None:
    st.header(uploader.name, ' upload successfully')
    df = pd.read_csv(uploader, index_col=False)
    st.write(df.head())
    if len(df.index) > 5:
        st.caption("The input only show the first 5 rows of data")
    create_graph()
else:
    st.info('Awaiting for dataset to be uploaded')

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
