# pages/Dataset.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px

# page configuration
st.set_page_config(page_title="Top 100 Sports Bets Analysis", layout="wide")



# title and description
st.title("📊 Top 100 Sports Bets Analysis")
st.markdown("""
This dashboard provides an in-depth analysis of the top 100 most bet sports matches. Explore various insights such as the popularity of competitions, betting trends over time, top teams involved in betting, and more.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("Top_100_Sports_Bets.csv", sep=';')
    # data cleaning (remove € symbol and spaces, then convert to float)
    df['mises'] = df['mises'].replace({'€': '', ' ': ''}, regex=True).astype(float)
    df['n_mises'] = df['n_mises'].replace({' ': ''}, regex=True).astype(int)
    df['n_joueurs'] = df['n_joueurs'].replace({' ': ''}, regex=True).astype(int)
    #'date_rencontre' to datetime
    df['date_rencontre'] = pd.to_datetime(df['date_rencontre'], format='%Y-%m-%d')

    return df

data = load_data()

# sidebar filters
st.sidebar.header("Filter Options")
# by sport
sports = data['sport'].unique()
selected_sport = st.sidebar.multiselect("Select Sport", options=sports, default=sports)
# by competition
competitions = data['competition'].unique()
selected_competition = st.sidebar.multiselect("Select Competition", options=competitions, default=competitions)
# by date range
min_date = data['date_rencontre'].min()
max_date = data['date_rencontre'].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])
# apply filters
filtered_data = data[
    (data['sport'].isin(selected_sport)) &
    (data['competition'].isin(selected_competition)) &
    (data['date_rencontre'] >= pd.to_datetime(start_date)) &
    (data['date_rencontre'] <= pd.to_datetime(end_date))
]

st.markdown("### Filtered Data Overview")
st.dataframe(filtered_data)

# section 1: Popularity of Competitions
competition_bets= filtered_data.groupby('competition')['n_mises'].sum().sort_values(ascending=False).head(10)
st.markdown("## 🏆 Popularity of Competitions")

fig1= px.bar(
    competition_bets.reset_index(),
    x='n_mises',
    y='competition',
    orientation='h',
    title="Top 10 Competitions by Number of Bets",
    labels={'n_mises': 'Number of Bets', 'competition': 'Competition'},
    color='n_mises',
    color_continuous_scale='Viridis'
)

st.plotly_chart(fig1, use_container_width=True)

# section 2 : Average Betting Amount per Match by Competition
st.markdown("## 📊 Average Betting Amount per Match by Competition")

avg_betting= filtered_data.groupby('competition')['mises'].mean().sort_values(ascending=False).reset_index()

fig9 = px.bar(avg_betting, x='competition', y='mises',
              title="Average Betting Amount (€) per Match by Competition",
              labels={'mises': 'Average Betting Amount (€)', 'competition': 'Competition'},
              hover_data=['mises'])

st.plotly_chart(fig9, use_container_width=True)

# section 3: Box Plots for Betting Amounts by Competition
st.markdown("## 📦 Distribution of Betting Amounts by Competition")

# select competitions
selected_competitions_box = st.multiselect(
    "Select Competitions for Box Plot",
    options=filtered_data['competition'].unique(),
    default=filtered_data['competition'].unique()
)

box_data = filtered_data[filtered_data['competition'].isin(selected_competitions_box)]

fig7 = px.box(box_data, x='competition', y='mises', 
             title="Betting Amounts Distribution by Competition",
             labels={'mises': 'Total Betting Amount (€)', 'competition': 'Competition'},
             points='outliers')  # outliers
st.plotly_chart(fig7, use_container_width=True)

# section 4:Betting Trends Over Time
# extract year and month
filtered_data['year'] = filtered_data['date_rencontre'].dt.year
filtered_data['month'] = filtered_data['date_rencontre'].dt.month

bets_over_time= filtered_data.groupby('year')['n_mises'].sum().reset_index()

st.markdown("## 📈 Betting Trends Over Time")
fig2= px.line(
    bets_over_time,
    x='year',
    y='n_mises',
    markers=True,
    title="Total Number of Bets Over Years",
    labels={'year': 'Year', 'n_mises': 'Number of Bets'},
    line_shape='linear',
    color_discrete_sequence=['orange']
)

st.plotly_chart(fig2, use_container_width=True)


#section 5 : Top Teams in Betting
st.markdown("## ⚽ Top Teams Involved in Betting")
#combine 'equipe_1' and 'equipe_2'
teams= pd.concat([filtered_data['equipe_1'], filtered_data['equipe_2']])
top_teams = teams.value_counts().head(10)

fig3, ax3 = plt.subplots(figsize=(10,6))
sns.barplot(x=top_teams.values, y=top_teams.index, ax=ax3, palette="magma")
ax3.set_xlabel("Number of Appearances")
ax3.set_ylabel("Team")
ax3.set_title("Top 10 Teams Involved in Bets")
st.pyplot(fig3)

#section 6: Betting Behavior Analysis
st.markdown("## 💰 Betting Behavior Analysis")
col1, col2= st.columns(2)

with col1:
    st.markdown("### Correlation Between Number of Bets and Total Amount")
    fig4, ax4= plt.subplots(figsize=(8,6))
    sns.scatterplot(data=filtered_data, x='n_mises', y='mises', hue='sport', palette="deep", ax=ax4)
    ax4.set_xlabel("Number of Bets")
    ax4.set_ylabel("Total Betting Amount (€)")
    ax4.set_title("Number of Bets vs Total Betting Amount")
    st.pyplot(fig4)

with col2:
    st.markdown("### Distribution of Betting Amounts")
    fig5, ax5= plt.subplots(figsize=(8,6))
    sns.histplot(filtered_data['mises'], bins=20, kde=True, ax=ax5, color='green')
    ax5.set_xlabel("Total Betting Amount (€)")
    ax5.set_ylabel("Frequency")
    ax5.set_title("Distribution of Betting Amounts")
    st.pyplot(fig5)


# section 7: Interactive Team Betting Analysis
st.markdown("## 🏅 Team Betting Analysis")
# select a team
all_teams = sorted(teams.unique())
selected_team = st.selectbox("Select a Team for Analysis", all_teams)
# filter data for the team
team_data = filtered_data[
    (filtered_data['equipe_1'] == selected_team) | 
    (filtered_data['equipe_2'] == selected_team)
]
# take betting data by competition
team_betting= team_data.groupby('competition').agg({
    'mises': 'sum',
    'n_mises': 'sum',
    'n_joueurs': 'sum'
}).reset_index()

fig8 = px.bar(team_betting, x='competition', y='mises',
              title=f"Total Betting Amount for {selected_team} by Competition",
              labels={'mises': 'Total Betting Amount (€)', 'competition': 'Competition'},
              hover_data=['n_mises', 'n_joueurs'])

st.plotly_chart(fig8, use_container_width=True)


# section 8: Detailed Match Analysis
st.markdown("## 🧐 Detailed Match Analysis")
st.markdown("""
Explore individual matches to understand specific betting behaviors and outcomes.
""")
# select a match
match = st.selectbox("Select a Match to View Details", filtered_data['equipe_1'] + " vs " + filtered_data['equipe_2'])
# take match details
match_details = filtered_data[filtered_data['equipe_1'] + " vs " + filtered_data['equipe_2'] == match].iloc[0]

st.markdown(f"### Match: {match}")
st.write(f"**Sport:** {match_details['sport']}")
st.write(f"**Competition:** {match_details['competition']}")
st.write(f"**Date:** {match_details['date_rencontre'].strftime('%Y-%m-%d')}")
st.write(f"**Total Betting Amount:** €{match_details['mises']:,}")
st.write(f"**Number of Bets:** {match_details['n_mises']:,}")
st.write(f"**Number of Players:** {match_details['n_joueurs']:,}")

# footer
st.markdown("""
---
*Data Source: ANJ (Autorité Nationale des Jeux)*
""")