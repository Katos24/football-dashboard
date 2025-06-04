import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
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


# Year selector in sidebar
year = st.sidebar.selectbox("Select Year", options=sorted(csv_urls.keys(), reverse=True))

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



# --- Top 5 in 1D with Blue First Downs Text ---
top_5 = df.sort_values('1D', ascending=False).head(5).reset_index(drop=True)

st.markdown("### 🏆 Top 5 QB by First Downs (1D)")

# Add CSS for hover effect and spacing
st.markdown("""
<style>
.top5-card {
    background: linear-gradient(135deg, #4a90e2, #357ABD);
    color: white;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(53, 122, 189, 0.5);
    text-align: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    user-select: none;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin: 0 0.3rem;
}
.top5-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(53, 122, 189, 0.7);
}
@media (max-width: 768px) {
    .top5-card {
        margin: 0.5rem 0;
    }
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(5)
for i, row in top_5.iterrows():
    with cols[i]:
        st.markdown(f"""
            <div class="top5-card">
                <div style="font-size: 1.4rem; font-weight: 700; margin-bottom: 0.4rem;">#{i+1}</div>
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.8rem;">{row['Player']}</div>
                <div style="font-size: 1rem;">
                    1D: <strong style="color: #a9d1ff;">{int(row['1D'])}</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- Data Preview ---
df_sorted = df.sort_values('1D', ascending=False).reset_index(drop=True)
df_sorted.index = df_sorted.index + 1

st.write(f"### Data Preview ({year} Season)")
st.dataframe(df_sorted)

# --- Top 10 QBs – Passing First Downs ---
st.write("### 📊 Top 10 Players – Passing First Downs")

top_qbs = df.sort_values('1D', ascending=False).head(10)

fig_qb_1d = px.bar(
    top_qbs,
    x='Player',
    y='1D',
    color='1D',
    color_continuous_scale='Blues',
    hover_data={'Team': True, 'Att': True, 'Cmp': True, '1D': True},
    text='1D',
)

fig_qb_1d.update_traces(
    marker_line_color='black',
    marker_line_width=1,
    textposition='outside',
    textfont=dict(color='black', size=12)
)

fig_qb_1d.update_layout(
    plot_bgcolor='#f5f5f5',
    paper_bgcolor='#f5f5f5',
    showlegend=False,
    margin=dict(t=20, b=50, l=20, r=20),
    xaxis=dict(
        tickangle=-45,
        tickfont=dict(size=12, color='black'),
        title_text=None,
        showgrid=False,
        zeroline=False,
    ),
    yaxis=dict(
        tickfont=dict(size=12, color='black'),
        title_text=None,
        showgrid=False,
        zeroline=False,
    ),
    font=dict(color='black', size=14)
)

st.plotly_chart(fig_qb_1d, use_container_width=True)

# --- Top 10 by First Down Rate ---
top_10 = df.sort_values('First Down Rate', ascending=False).head(10)
st.write("### Top 10 Players by First Down Rate (%)")
st.table(top_10[['Player', 'First Down Rate']].reset_index(drop=True))


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
st.write("### Compare Two Players")
players = df['Player'].unique()
player1 = st.selectbox("Player 1", players, key='player1')
player2 = st.selectbox("Player 2", players, key='player2')

if player1 and player2:
    stats1 = df[df['Player'] == player1].iloc[0]
    stats2 = df[df['Player'] == player2].iloc[0]
    comparison_df = pd.DataFrame({player1: stats1, player2: stats2})
    st.dataframe(comparison_df)
