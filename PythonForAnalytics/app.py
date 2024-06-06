import streamlit as st

st.set_page_config(page_title="Python For Analytics", page_icon="📊",)

# -------------------------------------------------------------------
# Defenition of functions to be used as individual pages
# -------------------------------------------------------------------

def home():
    st.title("Welcome to Python For Analytics!")
    st.write("""
Python For Analytics is your go-to resource for common to complex Python code.

Whether you're a seasoned data analyst or just starting out, this collection of code examples will provide you with the tools and knowledge you need to excel in Python-based data analysis.

Happy coding!
            """)
    
# -------------------------------------------------------------------
# Python Basics
def python_basics():
    st.header("Python Basics")
    st.write("PLACEHOLDER")
    st.code("""

""") 
    
# -------------------------------------------------------------------
# Data Manipulation
def data_manipulation_1():
    st.header("Data Manipulation")
    st.markdown(
"""
- Reading and Writing Files
- Slicing and Filtering DataFrames
"""
)
    st.subheader("Importing and Exporting data with Pandas")
    st.code("""
import pandas as pd

file = str(input("Please enter a file"))
file = file.replace("\\\\","/")
#OR
file = (r"your_file_path")    
            
# Reading a CSV file:
df = pd.read_csv(file)

#Reading an Excel file
df = pd.read_excel(file)
            
# Check to see if the file has a header
import csv
with open(file, 'r') as csvfile:
    has_header = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0)
if has_header:
    header = True
    df_raw = pd.read_csv(file)
else:
    header = False
    df_raw = pd.read_csv(file_path, header=None)            

# Writing to a CSV file
df.to_csv('output.csv', index=False)

#Writing to an Excel file
df.to_excel('output.xlsx', index=False)
    """)


    st.subheader("Slicing and Filtering")
    st.code("""
import pandas as pd
            
# Selecting rows based on boolean condition
filtered_df = df[df['column'] > 10]

# Select specific columns
selected_columns = filtered_df[['column1', 'column2']]
            
# Selecting rows and columns based on boolean condition
selected_data = df[df['column'] > 10][['column1', 'column2']]

# Selecting specific rows and columns using loc
selected_data = df.loc[df['column'] > 10, ['column1', 'column2']]
            
# Using iloc (Integer-location based indexing)
df.iloc[1:3, 0:2])  # Rows 1 to 2, columns 0 to 1
        
    """)

    st.subheader("Filtering with .isin()")
    st.code("""
import pandas as pd
            
# List of names to filter
names_to_include = ['Alice', 'David']

# Filter DataFrame to include only specified names
filtered_df = df[df['Name'].isin(names_to_include)]
            
# List of names to exclude
names_to_exclude = ['Alice', 'David']

# Filter DataFrame to exclude specified names. 
# Notice this symbol ( ~ ) negates .isin() to make it "is NOT in"
filtered_df = df[~df['Name'].isin(names_to_exclude)]
        
    """)

# -------------------------------------------------------------------
# Data Manipulation
def data_manipulation_2():
    st.header("Data Manipulation")
    st.markdown(
"""
- Coming Soon
- Coming Soon

"""
)
    st.code(
"""

""")
  
# -------------------------------------------------------------------
# Data Cleaning
def data_cleaning():
    st.header("Data Cleaning")
    st.markdown(
"""
- Coming Soon
- Coming Soon

""")
    st.code(
"""

""")

def data_visualization():
    st.header("Data Visualization")
    st.markdown(
"""
- Coming Soon
- Coming Soon

""")
    st.code(
"""

""")

def eda():
    st.header("Exploratory Data Analysis")
    st.markdown(
"""
- Coming Soon
- Coming Soon

""")
    st.code(
"""

""")


def statistical_analysis():
    st.header("Statistical Analysis")
    st.markdown(
"""
- Coming Soon
- Coming Soon

""")
    st.code(
"""

""")


def automation_scripting():
    st.header("Automation and Scripting")
    st.markdown(
"""
- Coming Soon
- Coming Soon

""")
    st.code(
"""

""")

def apis_web_scraping():
    st.header("APIs and Web Scraping")
    st.write("Using Requests and BeautifulSoup for web scraping.")
    st.code("""

    """)

def advanced_topics():
    st.header("Advanced Topics")
    st.write("Time series analysis and big data.")
    st.code("""

    """)

def useful_code():
    st.header("Other Useful Code")
    st.markdown(
"""
- Coming Soon
- Coming Soon

""")
    st.code(
"""

""")

# -------------------------------------------------------------------
# Streamlit Application
# -------------------------------------------------------------------

home() # Display the welcome information

tab1, tab2 = st.tabs(["📈 Code Examples", "🐍 Python Playground"])

with tab1:
    topic = st.selectbox("Select a topic:",
                        [#"Python Basics 🐍",
                        "Data Manipulation 101 🐼",
                        "Data Manipulation 102 🐼",
                        "Data Cleaning 🧹",
                        "Data Visualization 📊",
                        "Exploratory Data Analysis 🔍",
                        #"Statistical Analysis 📈",
                        "Automation and Scripting 🤖",
                        #"APIs and Web Scraping 🌐",
                        #"Advanced Topics 🚀",
                        "Other Useful Code 💡"])

    if topic == "Python Basics 🐍":
        python_basics()
    elif topic == "Data Manipulation 101 🐼":
        data_manipulation_1()
    elif topic == "Data Manipulation 102 🐼":
        data_manipulation_2()
    elif topic == "Data Cleaning 🧹":
        data_cleaning()
    elif topic == "Data Visualization 📊":
        data_visualization()
    elif topic == "Exploratory Data Analysis 🔍":
        eda()
    elif topic == "Statistical Analysis 📈":
        statistical_analysis()
    elif topic == "Automation and Scripting 🤖":
        automation_scripting()
    elif topic == "APIs and Web Scraping 🌐":
        apis_web_scraping()
    elif topic == "Advanced Topics 🚀":
        advanced_topics()
    elif topic == "Other Useful Code 💡":
        useful_code()

with tab2:
    with st.form("coder",border=False):
        with st.expander("About this coding engine"): 
            st.write("""Note: This Python coding engine is executed in Streamlit, therefore your code must comply with Streamlit syntax. For example, print("Hello world") becomes st.write("Hello world").""")
        st.header("Python coding engine")
        code = st.text_area("Enter your (Streamlit) Python code here",height = 200)
        if st.form_submit_button("Run Code"):
            try:
                st.divider()
                exec(code)
            except Exception as e:
                st.error(f"Error: {e}")

