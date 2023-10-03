#!/usr/bin/env python
# coding: utf-8

# # Streamlit Airline Data Dashboard

# **Objective:** Create an interactive web dashboard using Streamlit to explore and analyze the provided airline dataset, allowing users to gain insights into passenger demographics, flight routes, and flight statuses.

# In[1]:


# import all the packages
import pandas as pd
import numpy as np
import time
import streamlit as st
from datetime import datetime as dt
from matplotlib import pyplot as plt

#change location depeding on where i am whilst working on the project
location = st.selectbox('Choose file location',['Work (Local fle)','Git','Select a file'])
file = None


# define the file to be imported and replace the backslash with forwardslash
if location == 'Work (Local fle)':
    file = (r"C:\Users\PCHAPMAN\Documents\Paul - My Documents\Python\Airline Dataset Updated - v2.csv")
if location == 'Git':
    file = (r"https://raw.githubusercontent.com/QuerySavvy/TrainingFiles/main/Airline%20Dataset%20Updated%20-%20v2.csv")
if location == 'Select a file':
    if location not in ('Work (Local fle)', 'Git'):
        file = st.file_uploader("Choose a file")
        if file is None:
            st.write("No input file selected. Waiting for a file to be uploaded...")
            st.stop()

#if uploaded_file is not None:
#  df = pd.read_csv(uploaded_file)
#  st.subheader('DataFrame')
#  st.write(df)
#  st.subheader('Descriptive Statistics')
#  st.write(df.describe())
#else:
#  st.info('☝️ Upload a CSV file')
             
# read the file and convert ot a pandas DataFrame
data = pd.read_csv(file)
df = pd.DataFrame(data)
print(type(df))
print("Columns before adjusting dataset:\n",df.columns)

# Reformatting the date column
df['Departure Date'] = pd.to_datetime(df['Departure Date'],format='mixed)

# Reducing the dataset 
df = df[['Passenger ID', 'Gender', 'Age', 'Nationality', 'Airport Name',
'Country Name','Continents', 'Departure Date','Flight Status','Arrival Airport']]

#renaming columns
column_mapping = {'Airport Name': 'Departure Airport', 'Continents': 'Continent'}
df.rename(columns=column_mapping, inplace=True)
print("\nColumns after adjusting dataset:\n",df.columns)

# Making a reference list for the airports
lookup = df[['Departure Airport', 'Country Name', 'Continent']].drop_duplicates(subset='Departure Airport')


# **Passenger Demographics:**<br>
# 1. What is the distribution of passenger ages, and can we identify any age-related trends among passengers?
# 2. How does the gender distribution of passengers look, and is there any notable variation in travel preferences between genders?
# 3. Which nationalities are most commonly represented among passengers, and can we uncover any patterns related to nationality?

# In[2]:


#Passenger Demographics:
#Question 1
df['Age'].hist(bins = 15)
plt.suptitle('Distribution of age:', size = 14)
plt.title('This ficticious dataset does not follow the normal distribution',size = 10)
plt.show()


# In[3]:


#Passenger Demographics:
#Question 2

flights_by_sex = df.groupby("Gender")['Gender'].count()
flights_by_sex.plot(kind = 'bar')
plt.title('Gender split, male vs female')
plt.xlabel('Gender')
plt.ylabel('Count')

plt.show()


# In[4]:


#Passenger Demographics:
# Question 3

flights_by_nationality = df['Nationality'].value_counts().head(10)
flights_by_nationality = flights_by_nationality.sort_values()

flights_by_nationality.plot(kind = 'barh')
plt.title('Which nationality flies the most?')
plt.xlabel('Count')
plt.ylabel('Nationality')

plt.show()


# **Flight Routes and Airports:** <br>
# 1. What are the most frequently used airports in this dataset?
# 2. Which continents are the busiest in terms of flight departures, and are there seasonal variations in flight patterns?
# 3. Can we identify any trends or patterns in flight departures based on the departure date?

# In[5]:


#Flight Routes and Airports:
#Question 1
flights_by_airport = df.groupby(
    ['Departure Airport']).size().reset_index(name='count').sort_values(by='count', ascending=False)

airportjoin = flights_by_airport.merge(lookup, on='Departure Airport')
airportjoin = airportjoin.set_index('Departure Airport').head(10)

print("The top 10 airports are:\n\n",airportjoin)


# In[6]:


#Flight Routes and Airports:
#Question 2 and Question 3
#All flights
flight_counts = df.groupby(
    ['Continent', 'Departure Date']).size().reset_index(name='count').sort_values(by='count', ascending=True)
print("All Flights\n",flight_counts.head())

print("----------------------------------------------------------------------------------")

#filtered_df = df[df['Continent'] == 'inputvalue']

#All flights
flights_over_time = df.groupby(
    'Departure Date').size().reset_index(name='count').sort_values(by='count', ascending=False)
print("\nFlights_over_time\n",flights_over_time.head())
flights_over_time.plot(kind = "line", x='Departure Date',y='count', title = 'flights over time')
plt.show()

#Flights grouped by month
monthlyflights = flights_over_time.groupby(pd.Grouper(key='Departure Date', freq='M')).sum()
print("\nmonthlyflights\n",monthlyflights.head())
monthlyflights.plot(kind='line', y='count', title = 'flights grouped by month')
plt.show()


# **Flight Status Analysis:**
# 1. What is the percentage breakdown of flight statuses (on-time, delayed, canceled), and are there any factors associated with flight delays or cancellations?
# 

# In[7]:


#Flight Status Analysis:
#Question 1
flightstatus = df.groupby('Flight Status').size().reset_index(name='count').sort_values(by='count', ascending=False)
flightstatus.plot(kind = 'barh',x='Flight Status',y='count')


# In[8]:


print(df.head())


# **Visualization and Insights:**
# 1. How can we visually represent the age distribution, gender ratios, and nationality insights within the Streamlit dashboard?
# 2. Which airports and continents can be visualized as the busiest using interactive bar charts?
# 3. How can we create interactive time series plots to visualize flight departures over time and allow users to identify patterns or trends?

# In[9]:


#-------------------------------Streamlit variable setup
minage = df['Age'].min()
maxage = df['Age'].max()
age25 = np.percentile(df['Age'], 25)
age75 = np.percentile(df['Age'], 75)




# In[ ]:
#-------------------------------Sreamlit Design Testing
st.title("This is the title")
st.header("This is a header")
st.subheader("This is a subheader")
st.sidebar.header("This is the sidebar")
st.markdown("this is markdown")
st.caption("This is a caption")
st.text("This is text")






# In[ ]:
#-------------------------------Sreamlit Design Development
st.sidebar.subheader('Title')
values = st.sidebar.slider(
    'Select a range of values',
    value = [minage,maxage])
st.sidebar.write('Age range:', values)




# **Streamlit Dashboard:**
# 1. Create a Streamlit web application with interactive widgets and visualizations for each of the questions above.
# 2. Provide explanations and context for each section of the dashboard to guide users through the analysis.
# 3. Ensure a user-friendly and responsive design for a seamless exploration experience.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




