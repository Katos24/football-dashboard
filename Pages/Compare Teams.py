import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Compare NFL Teams", layout="wide")

# CSV URLs by year
csv_urls = {
    '2024': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=0&single=true&output=csv",
    '2023': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=891552912&single=true&output=csv",
    '2022': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=1500595878&single=true&output=csv",
    '2021': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=1119294445&single=true&output=csv",
    '2020': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=1068926879&single=true&output=csv",
}

team_conference = {
    'Detroit Lions': 'NFC', 'Tampa Bay Buccaneers': 'NFC', 'Baltimore Ravens': 'AFC',
    'Washington Commanders': 'NFC', 'Cincinnati Bengals': 'AFC', 'Buffalo Bills': 'AFC',
    'Philadelphia Eagles': 'NFC', 'Atlanta Falcons': 'NFC', 'Arizona Cardinals': 'NFC',
    'Minnesota Vikings': 'NFC', 'San Francisco 49ers': 'NFC', 'Kansas City Chiefs': 'AFC',
    'Miami Dolphins': 'AFC', 'Green Bay Packers': 'NFC', 'Los Angeles Rams': 'NFC',
    'Seattle Seahawks': 'NFC', 'Dallas Cowboys': 'NFC', 'Pittsburgh Steelers': 'AFC',
    'Los Angeles Chargers': 'AFC', 'Denver Broncos': 'AFC', 'Indianapolis Colts': 'AFC',
    'New York Jets': 'AFC', 'Las Vegas Raiders': 'AFC', 'Tennessee Titans': 'AFC',
    'Houston Texans': 'AFC', 'New Orleans Saints': 'NFC', 'Cleveland Browns': 'AFC',
    'New England Patriots': 'AFC', 'New York Giants': 'NFC', 'Jacksonville Jaguars': 'AFC',
    'Chicago Bears': 'NFC', 'Carolina Panthers': 'NFC',
}

st.title("🏈 Compare NFL Teams by First Downs")

# Year selection
year = st.selectbox("Select Season", options=sorted(csv_urls.keys(), reverse=True))

# Load data
df = pd.read_csv(csv_urls[year])
df['Conference'] = df['TEAM'].map(team_conference)

# Team selection
team_choices = df['TEAM'].sort_values().unique()
team1, team2 = st.columns(2)
with team1:
    selected_team_1 = st.selectbox("Choose First Team", team_choices, index=0)
with team2:
    selected_team_2 = st.selectbox("Choose Second Team", team_choices, index=1)

# Data subset
df_compare = df[df['TEAM'].isin([selected_team_1, selected_team_2])]
categories = ['TOTAL', 'PASS', 'RUSH', 'PEN']


# Vertical bar chart comparison with value labels
st.markdown(f"### {year} First Down Comparison: {selected_team_1} vs {selected_team_2}")

# Melt dataframe to long format for plotting
df_melted = df_compare.melt(
    id_vars=["TEAM"],
    value_vars=categories,
    var_name="Type",
    value_name="Count"
)

# Create vertical bar chart
fig_compare = px.bar(
    df_melted,
    x="Type",
    y="Count",
    color="TEAM",
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Set1,
    text="Count"  # Display count labels
)

# Set text position to show above bars
fig_compare.update_traces(textposition='outside')
fig_compare.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    yaxis_title="First Downs",
    xaxis_title="Type",
    legend_title="Team"
)

st.plotly_chart(fig_compare, use_container_width=True)

# Optional: pie charts side-by-side
st.markdown("### Distribution Breakdown (Rush vs Pass vs Penalty)")
col1, col2 = st.columns(2)

for i, team in enumerate([selected_team_1, selected_team_2]):
    team_row = df[df["TEAM"] == team].iloc[0]
    pie = px.pie(
        names=["Rush", "Pass", "Penalty"],
        values=[team_row["RUSH"], team_row["PASS"], team_row["PEN"]],
        title=team,
        color_discrete_map={'Rush': '#1f77b4', 'Pass': '#ff7f0e', 'Penalty': '#2ca02c'}
    )
    (col1 if i == 0 else col2).plotly_chart(pie, use_container_width=True)
