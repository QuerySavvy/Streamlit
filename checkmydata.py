import streamlit as st
import pandas as pd
#import seaborn as sns
from matplotlib import pyplot as plt



# ---------------------------- ---------------------------- Title and intro
st.title("CheckMyData")
st.write("Welcome to CheckMyData!!!")
st.write("This platform, powered by Python and Streamlit, " 
         "is designed to help data analysts gather quick insights about their data before conducting more complex analysis.")

# ---------------------------- ---------------------------- File source selection
location = st.selectbox('Choose file source:',['Demo','Upload a csv file','Git URL'],)
file = None

# define the file to be imported
if location == 'Demo':
    file = "https://raw.githubusercontent.com/QuerySavvy/Streamlit/main/apartments_pl_2023_10.csv"
    with st.expander('Click to view dataset details'):
        st.write("A sample dataset has been loaded. "
                 "This dataset contains apartment offers from the 15 largest cities in Poland and comes "
                 "from https://www.kaggle.com/datasets/krzysztofjamroz/apartment-prices-in-poland")  
if location == 'Git URL':
    file = st.text_input("Paste your URL below:", "")    
    if len(file)<1:
        st.info('☝️ Please insert a URL')
        st.stop()
if location == 'Upload a csv file':
    file = st.file_uploader("Please choose a csv file to upload:")
    if file is None:
        st.info('☝️ Upload a file')
        st.stop()

# read the file and convert ot a pandas DataFrame
data = pd.read_csv(file)
df = pd.DataFrame(data)


# ---------------------------- ---------------------------- Data Preview 
st.subheader('Dataset preview:')
st.write(df.head())


# ---------------------------- ---------------------------- Data Summary 
# Print a summary of the number of rows and number of columns 
st.subheader('Data Summary:')

datashape = df.shape
st.write('The dataset contains ', datashape[1],' columns and ',datashape[0],' rows.')


# Group the data by data type and print a sentance for each data type
grouped_columns = df.columns.to_series().groupby(df.dtypes).groups
for data_type, columns in grouped_columns.items():
    st.markdown(f"- {len(columns)} columns with data type {data_type}.")

# ---------------------------- ---------------------------- Drop down section with data type
# Create a list of the different data types present in the file
st.subheader('Columns Details:')
unique_data_types = df.dtypes.unique()
# Pass the result to a select box, store the selecteted item to the variable 'datatypeselection'
form_datatypeselection = st.selectbox('Explore column(s) by data type and check for null values',unique_data_types)
# Create a table containing of all the columns containing the selected data type and check for null values
form_selectedcolumns = df.select_dtypes(include=[form_datatypeselection])
null_counts = form_selectedcolumns.isnull().sum()
data_types = form_selectedcolumns.dtypes
unique_values = form_selectedcolumns.nunique()
formatted_output = pd.DataFrame({ 'Data Type': data_types, 
                                  'Null Count': null_counts.values, 
                                  'Unique Values': unique_values.values})
st.table(formatted_output)

# ---------------------------- ---------------------------- Summary statistics
st.subheader('Summary statistics of numeric column(s)')
st.write(df.describe())

# ---------------------------- ---------------------------- Data Visualisation - Histogram
# Create a list of the different numeric columns present in the file
st.subheader('Data Visualisation:')
st.write("Inspect the distribution of numeric columns")
# Create a streamlit container to hold the paramaters for the histogram
col1, col2 = st.columns(2)
with col1:
    numeric_columns = df.select_dtypes(include=['number'])
    # Convert the variable to a list
    numeric_column_list = numeric_columns.columns.tolist()
    # Pass the result to a select box, store the selecteted item to the variable 'form_histcolumn'
    form_histcolumn = st.selectbox('Select a column to visualise',numeric_column_list)
with col2:
    histselection_unique_values = df[form_histcolumn].nunique()
    form_histbins = st.slider('Select the number of bins', 1, 50, min(20,histselection_unique_values))

# Create a histogram using the column selected paramaters
fig1 = plt.figure()
plt.hist(df[form_histcolumn],edgecolor = "black",bins=form_histbins)
# sns.histplot(df[form_histcolumn], kde=True, bins=form_histbins)
plt.title(f'Distribution of {form_histcolumn}')
st.pyplot(fig1)

# ---------------------------- ---------------------------- Data Visualisation - create your own chart
st.subheader('Explore relationships between variables:')

st.write('Select input variables for a bar chart:')
column_list = df.columns.tolist()
# Create a layout of three columns to choose the columns and aggregation types
col1, col2, col3 = st.columns(3)
with col1:
    x_axis = st.selectbox('Select an x axis value',column_list)
with col2:
    aggregation = st.selectbox('Select an aggregation method',['Sum','Average','Count'])   
with col3:
    y_axis = st.selectbox('Select a y axis value',column_list)
st.write("THIS IS A TEST")

if st.button('Display Bar Chart'):
    if aggregation == 'Sum': 
        df_agg = df.groupby(x_axis)[y_axis].sum()
    if aggregation == 'Average': 
        df_agg = df.groupby(x_axis)[y_axis].mean()
    if aggregation == 'Count': 
        df_agg = df.groupby(x_axis)[y_axis].count()
    st.bar_chart(df_agg)


st.write('Select input variables for a scatter chart:')
col1, col2 = st.columns(2)
with col1:
    x_axis2 = st.selectbox('Select an x axis value for your scatter chart',column_list)  
with col2:
    y_axis2 = st.selectbox('Select a y axis value for your scatter chart',column_list)

if st.button('Display Scatter Chart'):
    st.scatter_chart(df, x=x_axis2,y=y_axis2)
