#!/usr/bin/env python
# coding: utf-8

# # Streamlit Airline Data Dashboard

# **Objective:** Create an interactive web dashboard using Streamlit to explore and analyze the provided airline dataset, allowing users to gain insights into passenger demographics, flight routes, and flight statuses.

# import all the packages
import pandas as pd
import numpy as np
import time
import streamlit as st
from datetime import datetime as dt
from matplotlib import pyplot as plt

# read the file and convert ot a pandas DataFrame
file = (r"https://raw.githubusercontent.com/QuerySavvy/TrainingFiles/main/Airline%20Dataset%20Updated%20-%20v2.csv")
data = pd.read_csv(file)
df = pd.DataFrame(data)
print(type(df))
print("Columns before adjusting dataset:\n",df.columns)

# Reformatting the date column
df['Departure Date'] = pd.to_datetime(df['Departure Date'], format = 'mixed')

# Reducing the dataset 
df = df[['Passenger ID', 'Gender', 'Age', 'Nationality', 'Airport Name',
'Country Name','Continents', 'Departure Date','Flight Status','Arrival Airport']]

#renaming columns
column_mapping = {'Airport Name': 'Departure Airport', 'Continents': 'Continent'}
df.rename(columns=column_mapping, inplace=True)
print("\nColumns after adjusting dataset:\n",df.columns)

# Making a reference list for the airports
lookup = df[['Departure Airport', 'Country Name', 'Continent']].drop_duplicates(subset='Departure Airport')



#--------------------------------------------------------------Sreamlit Sidebar and Filters

st.sidebar.title('Settings and Filters')

minage = df['Age'].min()
maxage = df['Age'].max()
age25 = np.percentile(df['Age'], 25)
age75 = np.percentile(df['Age'], 75)

Mindate = df['Departure Date'].min()
Maxdate = df['Departure Date'].max()
Mindate = dt.date(Mindate)
Maxdate = dt.date(Maxdate)

date = st.sidebar.slider(
    'Select a date range',
    value = (Mindate, Maxdate))

age = st.sidebar.slider(
    'Select an age range',
    int(minage),int(maxage),(int(age25),int(age75)))

MinAgeSelected = age[0]
MaxAgeSelected = age[1]

MinDateSelected = pd.to_datetime(date[0])
MaxDateSelected = pd.to_datetime(date[1])

flights_by_nationality = df['Nationality'].value_counts().head(10)
flights_by_nationality = flights_by_nationality.sort_values()
countries = flights_by_nationality.index.tolist()

if st.sidebar.toggle('Filter by top 10 nationalities'):
    NationalitySelected = st.sidebar.selectbox('Selection a nationality',countries)
    df = df[(df['Nationality'] == NationalitySelected)]

# apply all the filters to the Dataframe
df = df[(df['Age'] >= MinAgeSelected) & (df['Age'] <= MaxAgeSelected)]
df = df[(df['Departure Date'] >= MinDateSelected) & (df['Departure Date'] <= MaxDateSelected)]

#-------------------------------------------------------------- Group and slice the data for analysis
flights_by_sex = df.groupby("Gender").size().reset_index(name='Count')

flights_by_nationality = df['Nationality'].value_counts().head(10)
flights_by_nationality = flights_by_nationality.sort_values()

flights_by_airport = df.groupby(
    ['Departure Airport']).size().reset_index(name='Count').sort_values(by='Count', ascending=False)
airportjoin = flights_by_airport.merge(lookup, on='Departure Airport')
airportjoin = airportjoin.set_index('Departure Airport').head(10)

#Flight Routes and Airports:
#Question 2 and Question 3
flights_over_time = df.groupby(
    'Departure Date').size().reset_index(name='count').sort_values(by='count', ascending=False)

#Flight Status Analysis:
#Question 1
flightstatus = df.groupby('Flight Status').size().reset_index(name='count').sort_values(by='count', ascending=False)
flightstatus.plot(kind = 'barh',x='Flight Status',y='count')


#-------------------------------Streamlit setup

# fig1 - Histogram of age distribution
fig1, ax = plt.subplots()
ax.hist(df['Age'],bins = 15)
plt.suptitle('Distribution of age:', size = 14)
plt.title('This ficticious dataset does not follow the normal distribution',size = 10)

#fig3
fig3, ax = plt.subplots()
flights_by_nationality.plot(kind = 'barh')
plt.title('Which nationality flies the most?')
plt.xlabel('Count')
plt.ylabel('Nationality')

#-------------------------------Sreamlit Design Testing
st.title("Explitory Data Analysis of the Airline Dataset")
st.write("Objective: Create an interactive web dashboard using Streamlit to explore and analyse the airline dataset, allowing users to gain insights into passenger demographics, flight routes, and flight statuses.")

st.header("Section 1: Customer demographics")
st.subheader("Question 1")
st.write("What is the distribution of passenger ages?")
st.pyplot(fig1)

st.subheader("Question 2")
st.write("How does the gender distribution of passengers look, and is there any notable variation in travel preferences between genders?")
st.bar_chart(flights_by_sex, x='Gender', y = 'Count')

st.subheader("Question 3")
st.write("Which nationalities are most commonly represented among passengers, and can we uncover any patterns related to nationality?")
st.pyplot(fig3)

st.header("Section 2: Flight Routes and Airports:")
st.subheader("Question 1")
st.write("What are the most frequently used airports in this dataset?")
st.write("The top 10 airports are:\n\n",airportjoin)

st.subheader("Question 2 ")
st.write("Are there seasonal variations in flight patterns?")
st.line_chart(flights_over_time, x='Departure Date',y='count')

st.header("Section 3: Flight Status Analysis:")
st.write("What is the percentage breakdown of flight statuses (on-time, delayed, canceled)")
st.bar_chart(flightstatus,x='Flight Status',y='count')
