import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Load Data
all_df = pd.read_csv("https://raw.githubusercontent.com/MHendriF/bike-sharing-analysis/main/Submission/dashboard/main_data.csv")

st.set_page_config(page_title="Bike-Sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

# Helper function
def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby(["season", "year"]).agg({
        "total_users": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    seasonly_users_df = seasonly_users_df.sort_values('season')
    return seasonly_users_df

def create_weather_cond_users_df(df):
    weather_users_df = df.groupby(["weather_situation", "year"]).agg({
        "total_users": "sum"
    })
    weather_users_df = weather_users_df.reset_index()
    weather_users_df['weather_situation'] = pd.Categorical(weather_users_df['weather_situation'],
                                             categories=['good', 'moderate', 'bad', 'worse'])
    weather_users_df = weather_users_df.sort_values('weather_situation')
    return weather_users_df

def create_monthly_users_df(df):
    monthly_users_df = df.groupby(["month", "year"]).agg({
        "total_users": "sum"
    })
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df['month'] = pd.Categorical(monthly_users_df['month'],
                                             categories=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'])
    monthly_users_df = monthly_users_df.sort_values('month')
    return monthly_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby(["hour"]).agg({
        "total_users": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df['hour'] = pd.Categorical(hourly_users_df['hour'],
                                             categories=['12 am', '01 am', '02 am', '03 am', '04 am', 
                                                        '05 am', '06 am', '07 am', '08 am', '09 am', 
                                                        '10 am', '11 am', '12 pm', '01 pm', '02 pm',
                                                        '03 pm', '04 pm', '05 pm', '06 pm', '07 pm',
                                                        '08 pm', '09 pm', '10 pm', '11 pm'])
    hourly_users_df = hourly_users_df.sort_values('hour')
    return hourly_users_df

def create_composition_users_df(df):
    composition_users_df = df[['casual_users', 'registered_users']].sum()
    return composition_users_df

datetime_columns = ["date"]
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)
    
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Komponen Filter
min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/MHendriF/bike-sharing-analysis/main/Submission/assets/bycicle.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Filter Range Date',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]


# Menyiapkan berbagai dataframe
seasonly_users_df = create_seasonly_users_df(main_df)
weather_users_df = create_weather_cond_users_df(main_df)
monthly_users_df = create_monthly_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)
composition_users_df = create_composition_users_df(main_df)

st.title("Bike Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)
   
with col1:
    total_casual_rides = main_df['casual_users'].sum()
    st.metric("User Casual Rides", value=total_casual_rides)
with col2:
    total_registered_rides = main_df['registered_users'].sum()
    st.metric("User Registered Rides", value=total_registered_rides)
with col3:
    total_all_rides = main_df['total_users'].sum()
    st.metric("Total User Rides", value=total_all_rides)

st.markdown("---")


# Bagaimana tren penyewaan sepeda di tiap musimnya pada tahun 2011 dan 2012?
st.subheader('Season')

fig, ax = plt.subplots(figsize=(15, 7))
sns.barplot(data=seasonly_users_df, x="season", y="total_users", hue="year", palette="Set1", errorbar=None, ax=ax)

for i in ax.containers:
    ax.bar_label(i,fontsize=10)

ax.set_xlabel('Season',fontsize=15)
ax.set_ylabel('Total Rides',fontsize=15)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Bagaimana perbedaan tren penyewaan sepeda setiap bulannya pada tahun 2011 dengan 2012?
st.subheader('Wather Situation')

fig, ax = plt.subplots(figsize=(15, 7))
sns.barplot(data=weather_users_df, x="weather_situation", y="total_users", hue="year", palette="Set2", errorbar=None, ax=ax)

for i in ax.containers:
    ax.bar_label(i,fontsize=10)

ax.set_xlabel('Weather Situation',fontsize=15)
ax.set_ylabel('Total Rides',fontsize=15)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Bagaimana perbandingan pengguna tiap bulan di tahun 2011 dan 2012?
st.subheader('Monthly User')

fig, ax = plt.subplots(figsize=(15, 7))

sns.lineplot(x='month', y='total_users', hue='year', data=monthly_users_df, marker="o", palette="Set1", markersize=8, ax=ax)

# label points on the plot
for x, y in zip(monthly_users_df['month'], monthly_users_df['total_users']):
    plt.text(x = x, # x-coordinate position of data label
             y = y-150, # y-coordinate position of data label, adjusted to be 150 below the data point
             s = '{:.0f}'.format(y), # data label, formatted to ignore decimals
             color = 'grey') # set colour of line

ax.set_xlabel('Month',fontsize=15)
ax.set_ylabel('Total Rides',fontsize=15)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Kapan traffic tertinggi dan terendah penyewaan sepeda?
st.subheader('Traffic User')

fig, ax = plt.subplots(figsize=(15, 7))

sns.despine(fig)
sns.set(style="whitegrid")
sns.barplot(data=hourly_users_df, x='total_users', y='hour', orient='h', ax=ax)

for i in ax.containers:
    ax.bar_label(i,fontsize=10)
    
ax.set_xlabel('Total Rides',fontsize=15)
ax.set_ylabel('Time',fontsize=15)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Bagaimana komposisi pengguna Bike sharing?
st.subheader('User Composition')

fig, ax = plt.subplots(figsize=(6, 6))
sns.despine(fig)
sns.set_style("whitegrid")

plt.pie(
    x=composition_users_df,
    labels=('casual', 'registered'),
    colors=('#5F9EA0', '#7FFFD4'),
    autopct='%1.1f%%',
    wedgeprops = {'width':0.4}
)
st.pyplot(fig)