import streamlit as st
import pandas as pd


location = st.selectbox('Choose file type:',['Git URL','Upload a file'],)
file = None

# define the file to be imported and replace the backslash with forwardslash
if location == 'Git URL':
    file = st.text_input("Enter your URL below:", "https://raw.githubusercontent.com/QuerySavvy/TrainingFiles/main/Airline%20Dataset%20Updated%20-%20v2.csv")    
    if len(file)<1:
        st.info('☝️ Please insert a URL')
        st.stop()
if location == 'Upload a file':
    file = st.file_uploader("Please choose a file to upload:")
    if file is None:
        st.info('☝️ Upload a file')
        st.stop()
    st.balloons()
# read the file and convert ot a pandas DataFrame
data = pd.read_csv(file)

st.write("Data preview:")
st.write(data.head())
