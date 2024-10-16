import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('fatalities.csv')


st.title("Incident tracker project")
st.sidebar.header("Upload data bro")
uploaded_file = st.sidebar.file_uploader("choose a csv", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    num_events = len(data)
    st.sidebar.write('mumber of events', num_events)
    weapons_used = data['ammunition'].value_counts()
    st.sidebar.write("weapons", weapons_used)

    col1 , col2 = st.sidebar.columns(2)
    col3 , col4 = st.sidebar.columns(2)

    citizenship_count = data['citizenship'].value_counts()
    event_location_count_region = data['event_location_region'].value_counts()
    hostilities_count = data[data['took_part_in_the_hostilities']=='YES']['citizenship'].value_counts()
    no_hostilities_counts = data[data['took_part_in_the_hostilities'] == 'No']['citizenship'].value_counts()

    with col1:
        st.subheader("Citizenship")
        st.write(citizenship_count)

    with col2:
        st.subheader("Event Location Region")
        st.write(event_location_count_region)

    with col3:
        st.subheader("hostilities")
        st.write(hostilities_count)
    with col4:
        st.subheader('no hostilities')
        st.write(no_hostilities_counts)


    st.header("Sample data")
    st.write(data.head())
#-----------------
    st.header("Data Analysis")
    col1 , col2 = st.columns(2)
    with col1:
        citizenship_count= data['citizenship'].value_counts()
        st.subheader("Incidents by citizenship")
        st.bar_chart(citizenship_count)

    with col2:
        citizenship_count = data['gender'].value_counts()
        st.subheader("Incidents by gender")
        st.bar_chart(citizenship_count)



    col1 , col2 = st.columns(2)
    with col1:
        st.subheader("Summary stats for age")
        citizenship_count = data['age'].describe()
        st.write(citizenship_count)

    with col2:
        citizenship_count = data['event_location_region'].value_counts()
        st.subheader("Incidents by region")
        st.bar_chart(citizenship_count)

    col1 , col2 = st.columns(2)
    
    with col1:
        st.subheader("Unique places for residence by region")
        citizenship_count = data.groupby('event_location_region')['event_location'].nunique()
        st.write(citizenship_count)

    with col2:
        st.subheader("Unique places for residence by age")
        citizenship_count = data.groupby('event_location_region')['age'].mean()
        st.write(citizenship_count)


    # Visualize the types of injuries using Matplotlib pi chart
    st.subheader('Types of injuries')
    injury_counts = data['type_of_injury'].value_counts()
    fig , ax = plt.subplots()
    ax.pie(injury_counts, labels=injury_counts.index, autopct='%1.1f%%')
    st.pyplot(fig)

    # Data filtering example: Incidents in a specific region with specific characteristics
    region = 'West Bank'
    filtered_data = data[(data['event_location_region']==region) & (data['type_of_injury']=='gunfire')]
    st.subheader(f"Incidents in {region} with Gunfire as Injury Type")
    st.write(filtered_data)

    #stones throwing average age
    avg_age = data[(data['citizenship']=='Palestinian') & (data['type_of_injury']=='stones throwing')].groupby('gender')['age'].mean()
    st.subheader("stones throwing avg age")
    st.write(avg_age)

    # Time-based analysis (events at specific times)
    data['date_of_event'] = pd.to_datetime(data['date_of_event'])
    data['year'] = data['date_of_event'].dt.year
    data['month'] = data['date_of_event'].dt.month_name()
    time_events = data.groupby(['year', 'month']).size().reset_index(name='incident_count')
    time_events['year_month'] = time_events['month'] + ' ' + time_events['year'].astype(str)
    st.subheader('Time Based Events')
    st.line_chart(time_events.set_index('year_month')['incident_count'])

    # Calculate average age for female (F) citizens
    female_age = pd.pivot_table(data[data['gender'] == 'F'], values='age', index=['citizenship'], aggfunc='mean')
    st.subheader('Average Age for Female Citizens')
    st.bar_chart(female_age)    

    # Calculate average age for male (M) citizens

    male_age = pd.pivot_table(data[data['gender'] == 'M'], values='age', index=['citizenship'], aggfunc='mean')
    st.subheader('Average Age for male Citizens')
    st.bar_chart(male_age)

    # filtering with multiple conditions
    filtered_data = data[(data['citizenship'] == 'Palestinian') & (data['gender'] == 'F') & (data['type_of_injury'] == 'gunfire')] [['citizenship','gender','type_of_injury']]
    st.subheader("Gender and Nationality Injury type")
    st.write(filtered_data)

st.sidebar.text("data analysis done by Mr. Chirayu")