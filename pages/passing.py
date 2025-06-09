import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64

st.set_page_config(layout="centered")  # or leave as wide if you want
st.sidebar.markdown("""
### 🔍 About This Page
Dive deep into NFL passing first downs. Track performance by year, player, and key efficiency metrics.
""")

# URLs for each year's data CSV
csv_urls = {
    '2024': "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_MsjqbDCt5ffmLWWZ0c-pPjkFwoUT6TmQdSo1m4peXEO42c9wTs3V4C5lw9VyRXaeexUB7nFJCZLe/pub?gid=1348857990&single=true&output=csv",
    '2023': "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_MsjqbDCt5ffmLWWZ0c-pPjkFwoUT6TmQdSo1m4peXEO42c9wTs3V4C5lw9VyRXaeexUB7nFJCZLe/pub?gid=1490524640&single=true&output=csv",
    '2022': "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_MsjqbDCt5ffmLWWZ0c-pPjkFwoUT6TmQdSo1m4peXEO42c9wTs3V4C5lw9VyRXaeexUB7nFJCZLe/pub?gid=1282758623&single=true&output=csv",
    '2021': "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_MsjqbDCt5ffmLWWZ0c-pPjkFwoUT6TmQdSo1m4peXEO42c9wTs3V4C5lw9VyRXaeexUB7nFJCZLe/pub?gid=498746140&single=true&output=csv",
    '2020': "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_MsjqbDCt5ffmLWWZ0c-pPjkFwoUT6TmQdSo1m4peXEO42c9wTs3V4C5lw9VyRXaeexUB7nFJCZLe/pub?gid=2108600758&single=true&output=csv",
}

st.title("🏈 QB First Down Kings | NFL Passing Breakdown")
st.markdown("Get seamless and interactive visualizations of NFL quarterbacks' first down passing stats across seasons.")

# Move year selector here, not sidebar
year = st.selectbox("Select Year", options=sorted(csv_urls.keys(), reverse=True))

@st.cache_data
def load_data(year):
    url = csv_urls[year]
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    # Clean percentage columns
    pct_cols = ['First Down Rate', 'Succ%']
    for col in pct_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.rstrip('%').replace('nan', None)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert numeric columns
    numeric_cols = ['G', 'Age', 'Cmp', 'Att', 'Yds', 'TD', 'Int', '1D',
                    'Yards per First Down', 'First Down Rate per Game', 'Rate', 'QBR']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

df = load_data(year)


# top 5 cards
top_5 = df.sort_values('1D', ascending=False).head(5).reset_index(drop=True)

st.markdown("### 🏆 Top 5 QB by First Downs (1D)")

medals = {
    0: "🥇",  # Gold
    1: "🥈",  # Silver
    2: "🥉",  # Bronze
}

max_1d = top_5['1D'].max()

st.markdown("""
<style>
.top-list-item {
    padding: 0.3rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.3rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
    font-size: 0.9rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
}
.gold {
    background: linear-gradient(90deg, #FFD700, #FFC107);
}
.silver {
    background: linear-gradient(90deg, #C0C0C0, #A9A9A9);
}
.bronze {
    background: linear-gradient(90deg, #CD7F32, #B87333);
}
.others {
    background: linear-gradient(90deg, #4a90e2, #357ABD);
}
/* Bar behind the 1D number */
.bar {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 0;
    opacity: 0.3;
    border-radius: 6px;
}
/* Text container above the bar */
.text-content {
    position: relative;
    z-index: 1;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

for i, row in top_5.iterrows():
    medal = medals.get(i, f"{i+1}.")
    if i == 0:
        css_class = "top-list-item gold"
        bar_color = "rgba(255, 215, 0, 0.7)"  # gold
    elif i == 1:
        css_class = "top-list-item silver"
        bar_color = "rgba(192, 192, 192, 0.7)"  # silver
    elif i == 2:
        css_class = "top-list-item bronze"
        bar_color = "rgba(205, 127, 50, 0.7)"  # bronze
    else:
        css_class = "top-list-item others"
        bar_color = "rgba(74, 144, 226, 0.7)"  # blue

    # Calculate bar width as percentage of max 1D, min width for visibility
    bar_width_pct = max(10, (row['1D'] / max_1d) * 100)

    st.markdown(f"""
        <div class="{css_class}">
            <div class="bar" style="width: {bar_width_pct}%; background-color: {bar_color};"></div>
            <div class="text-content">
                <span><strong>{medal} {row['Player']}</strong></span>
                <span>1D: <strong>{int(row['1D'])}</strong></span>
            </div>
        </div>
    """, unsafe_allow_html=True)




# --- Data Preview ---
df_sorted = df.sort_values('1D', ascending=False).reset_index(drop=True)
df_sorted.index = df_sorted.index + 1

st.write(f"### Data Preview ({year} Season)")
st.dataframe(df_sorted)



# --- Top 10 QBs – Passing First Downs ---
top_qbs = df.sort_values('1D', ascending=True).tail(10)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=top_qbs['1D'],
    y=top_qbs['Player'],
    orientation='h',
    marker=dict(
        color=top_qbs['1D'],
        colorscale='blues',
        line=dict(color='rgba(255,255,255,0.7)', width=1.5)
    ),
    text=top_qbs['1D'],
    textposition='outside',
    insidetextanchor='start',
    textfont=dict(color='white'),
    hovertemplate=(
        "<b>%{y}</b><br>" +
        "Team: %{customdata[0]}<br>" +
        "Completions: %{customdata[1]}<br>" +
        "Attempts: %{customdata[2]}<br>" +
        "1D: %{x}<extra></extra>"
    ),
    customdata=top_qbs[['Team', 'Cmp', 'Att']]
))

fig.update_layout(
    title="🏈 Top 10 QBs – Passing First Downs",
    title_font=dict(color='white', size=22),
    xaxis=dict(title=None, showgrid=False, color='white'),
    yaxis=dict(title=None, tickfont=dict(size=13, color='white')),
    plot_bgcolor='#111111',
    paper_bgcolor='#111111',
    margin=dict(l=60, r=30, t=50, b=40),
    height=450,
    font=dict(color='white')
)

st.plotly_chart(fig, use_container_width=True)



# --- Interactive Scatter Plot ---
st.write("### Yards per First Down vs. First Down Rate")
selected_players = st.multiselect("Highlight Players", options=df['Player'].unique())

fig = px.scatter(
    df,
    x='First Down Rate',
    y='Yards per First Down',
    hover_data=['Player'],
    title='Yards per First Down vs. First Down Rate',
    labels={'First Down Rate': 'First Down Rate (%)', 'Yards per First Down': 'Yards per First Down'}
)

if selected_players:
    highlighted = df[df['Player'].isin(selected_players)]
    fig.add_scatter(
        x=highlighted['First Down Rate'],
        y=highlighted['Yards per First Down'],
        mode='markers+text',
        text=highlighted['Player'],
        textposition='top center',
        marker=dict(color='red', size=12),
        name='Selected Players'
    )

st.plotly_chart(fig, use_container_width=True)






# --- Compare Two Players ---
st.write("### 🆚 Compare Two Players")

col1, col2 = st.columns(2)
players = df['Player'].unique()
with col1:
    player1 = st.selectbox("Player 1", players, key='player1')
with col2:
    player2 = st.selectbox("Player 2", players, key='player2')

if player1 and player2 and player1 != player2:
    stats1 = df[df['Player'] == player1].iloc[0]
    stats2 = df[df['Player'] == player2].iloc[0]

    # Choose relevant stats to compare
    stat_cols = ['1D', 'Cmp', 'Att', 'Yds', 'TD', 'Int', 'Rate', 'QBR']
    comparison_df = pd.DataFrame({
        'Stat': stat_cols,
        player1: [stats1[stat] for stat in stat_cols],
        player2: [stats2[stat] for stat in stat_cols]
    })

    st.write("#### 📊 Stat Comparison")
    st.dataframe(comparison_df.set_index('Stat'), use_container_width=True)

    # Optional: Visual chart
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=comparison_df[player1],
        y=comparison_df['Stat'],
        orientation='h',
        name=player1,
        marker_color='steelblue'
    ))
    fig.add_trace(go.Bar(
        x=comparison_df[player2],
        y=comparison_df['Stat'],
        orientation='h',
        name=player2,
        marker_color='orange'
    ))

    fig.update_layout(
        barmode='group',
        title_text='Side-by-Side Player Comparison',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        height=400,
        margin=dict(t=30, b=30, l=30, r=30),
    )

    st.plotly_chart(fig, use_container_width=True)




