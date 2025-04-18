import streamlit as st
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.stats import percentileofscore
from sklearn.metrics import silhouette_score
import umap
import plotly.express as px
import plotly.graph_objects as go

# --- Streamlit Setup ---
st.set_page_config(page_title="Player Role Clustering & Analysis", layout="wide")

# --- Load Data ---
data_dir = "data/"
outfield_df = pd.read_parquet(data_dir + "outfield_df.parquet")

# --- Initial Filter & Cleanup ---
outfield_df = outfield_df[outfield_df["90s"] > 3]

meta_columns = ["Player Name", "Nationality", "Position", "Team", "Competition", "Age"]
features_for_clustering = [
    "Goals-PK", "Shots", "xG", "npxG", "npxG+xAG", "xAG", "Assists", "Key Passes", "SCA", "GCA",
    "Passes Attempted", "Pass Completion Percentage", "Passes into Penalty Area", "Final Third Passes",
    "Through Balls", "Progressive Passes", "Switches", "Crosses",
    "Progressive Carries", "Carries", "Carries Into Final 3rd", "Carries Into Penalty Area",
    "Carries Progressive Distance", "Touches Midfield 3rd",
    "Touches Attacking 3rd", "Touches Attacking Penalty Area", "Progressive Passes Received", 
    "Tackles", "Interceptions", "Blocks", "Clearances", "Ball Recoveries", "Dribblers Tackled", 
    "Blocked Passes", "Challenges Lost", "Dribblers Challenged", "Dispossessed", "Miscontrols",
    "Fouls Committed", "Fouls Drawn", "Times Takled During Take-On",
    "Aerials Won", "Aerials Lost", "Aerials Win Percentage"
]
outfield_df = outfield_df[meta_columns + ["90s"] + features_for_clustering]

# --- Per-90 Normalization ---
performance_df = outfield_df.copy()
for col in features_for_clustering:
    performance_df[col] = performance_df[col] / performance_df["90s"]
performance_df = performance_df.drop(columns=meta_columns + ["90s"])

# --- Scale + PCA + Clustering ---
scaler = RobustScaler()
scaled = scaler.fit_transform(performance_df)
pca = PCA(n_components=0.93)
pca_df = pd.DataFrame(pca.fit_transform(scaled), index=outfield_df.index)

Z = linkage(pca_df, method="ward")
cluster_labels = fcluster(Z, 12, criterion='maxclust')
outfield_df['Cluster'] = cluster_labels

# --- Role Mapping ---
role_mapping = {
    1: "Centre Back (Defensive)",
    2: "Centre Back (Ball-Playing)",
    3: "All-Round Midfielder",
    4: "Inverted Fullback / Direct Passer",
    5: "Holding Midfielder / Destroyer",
    6: "Full Back (Attacking)",
    7: "Out-and-Out Goalscorer",
    8: "Target Man",
    9: "Hybrid Forward",
    10: "Wide Forward / Inside Forward",
    11: "No.10 / Playmaker",
    12: "Creative Wide Player"
}

outfield_df['Player_ID'] = outfield_df['Player Name'] + " | " + outfield_df['Team'] + " | " + outfield_df['Age'].astype(str)

# --- Radar Chart Feature Set ---
radar_columns_outfield = [
    "Goals-PK", "npxG", "Shots", "Assists", "xAG", "SCA",
    "Passes Attempted", "Pass Completion Percentage", "Progressive Passes",
    "Progressive Carries", 'Touches Attacking Penalty Area',
    "Progressive Passes Received", "Tackles", "Interceptions",
    "Blocks", "Clearances", "Aerials Won"
]

def calculate_per90_stats(df, radar_columns):
    df_per90 = df.copy()
    for column in radar_columns:
        df_per90[column + '_per90'] = df.apply(
            lambda row: row[column] / row['90s'] if row['90s'] > 0 else 0, axis=1
        )
    return df_per90

def calculate_percentiles(df, radar_columns):
    df_percentiles = pd.DataFrame()
    df_percentiles['Player Name'] = df['Player Name']
    df_percentiles['Position'] = df['Position']
    df_percentiles['Team'] = df['Team']
    for column in radar_columns:
        if df[column + '_per90'].nunique() > 1:
            df_percentiles[column] = df[column + '_per90'].apply(lambda x: percentileofscore(df[column + '_per90'], x))
        else:
            df_percentiles[column] = 50
    return df_percentiles

def create_radar_plot(df_percentiles, selected_players, radar_columns):
    fig = go.Figure()
    colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ]
    for idx, player_name in enumerate(selected_players):
        player_data = df_percentiles[df_percentiles['Player Name'] == player_name].iloc[0]
        player_values = player_data[radar_columns].values

        fig.add_trace(go.Scatterpolar(
            r=player_values,
            theta=radar_columns,
            fill='toself',
            name=f"{player_data['Player Name']} ({player_data['Position']}, {player_data['Team']})",
            line=dict(color=colors[idx % len(colors)])
        ))

    fig.update_layout(
        title="Radar Chart Comparison",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100]),
                   angularaxis=dict(rotation=90)),
        showlegend=True
    )
    return fig

outfield_df_per90 = calculate_per90_stats(outfield_df, radar_columns_outfield)
outfield_df_percentiles = calculate_percentiles(outfield_df_per90, radar_columns_outfield)

# --- Streamlit UI ---
st.title("Football Player Role Explorer")
st.sidebar.header("Navigation")
menu_option = st.sidebar.radio("Select section", ["Player Selection", "Player Roles", "Radar Chart", "UMAP Visualization"])

if menu_option == "Player Selection":
    st.subheader("Player Cluster Overview")
    selected_player = st.sidebar.selectbox("Select a player", outfield_df['Player_ID'].unique())
    player_cluster = outfield_df[outfield_df['Player_ID'] == selected_player]['Cluster'].values[0]
    role_name = role_mapping.get(player_cluster, "")
    st.markdown(f"**{selected_player}** plays the role: {role_name}")
    cluster_data = outfield_df[outfield_df['Cluster'] == player_cluster]
    st.write(f"### Players in Role: {role_name}")
    st.dataframe(cluster_data[meta_columns])

elif menu_option == "Player Roles":
    st.subheader("View all players within a selected role")
    role_name_options = {v: k for k, v in role_mapping.items()}
    selected_role_name = st.sidebar.selectbox("Select Player Role", [
        "Centre Back (Defensive)",
        "Centre Back (Ball-Playing)",
        "Inverted Fullback / Direct Passer",
        "Full Back (Attacking)",
        "Holding Midfielder / Destroyer",
        "All-Round Midfielder",
        "No.10 / Playmaker",
        "Creative Wide Player",
        "Wide Forward / Inside Forward",
        "Hybrid Forward",
        "Out-and-Out Goalscorer",
        "Target Man"
    ])
    manual_cluster = role_name_options[selected_role_name]
    st.markdown(f"### Players in Role: {role_mapping.get(manual_cluster, '')}")
    manual_cluster_data = outfield_df[outfield_df['Cluster'] == manual_cluster]
    st.dataframe(manual_cluster_data[meta_columns])

elif menu_option == "Radar Chart":
    st.subheader("Radar Chart Comparison")
    player_options = outfield_df['Player_ID'].unique()
    selected_players = st.sidebar.multiselect("Select players to compare", options=player_options)
    if selected_players:
        radar_chart = create_radar_plot(outfield_df_percentiles, [p.split(" | ")[0] for p in selected_players], radar_columns_outfield)
        st.plotly_chart(radar_chart)
    else:
        st.info("Please select at least one player to generate the radar chart.")

elif menu_option == "UMAP Visualization":
    st.subheader("UMAP Role Landscape")

    # UMAP projection (only done once here for speed)
    umap_model = umap.UMAP(n_components=2, random_state=42)
    umap_coords = umap_model.fit_transform(pca_df)
    umap_df = pd.DataFrame(umap_coords, columns=['UMAP1', 'UMAP2'], index=outfield_df.index)
    outfield_df = pd.concat([outfield_df, umap_df], axis=1)

    # Multiselect for players to highlight
    highlight_players = st.sidebar.multiselect("Highlight players", outfield_df['Player_ID'].unique())

    outfield_df['Highlight'] = outfield_df['Player_ID'].isin(highlight_players)

    # Base UMAP scatter
    fig = px.scatter(
        outfield_df,
        x="UMAP1",
        y="UMAP2",
        color=outfield_df['Cluster'].map(role_mapping),
        hover_data=["Player Name", "Team", "Position", "Cluster"],
        labels={"color": "Player Role"}
    )

    # Highlight selected players
    highlight_df = outfield_df[outfield_df['Highlight']]
    fig.add_trace(go.Scatter(
        x=highlight_df['UMAP1'],
        y=highlight_df['UMAP2'],
        mode='markers+text',
        marker=dict(size=16, color='red', symbol='star'),
        text=highlight_df['Player Name'],
        textfont=dict(size=14, color='black', family="Arial Black"),
        hovertext=highlight_df.apply(
            lambda row: f"{row['Player Name']} ({row['Position']}, {row['Team']}, {row['Age']} y/o) – Role: {role_mapping.get(row['Cluster'], '')}",
            axis=1
        ),
        hoverinfo='text',
        name="Highlighted Players",
        textposition='top center'
    ))

    fig.update_layout(legend_title="Player Role", showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

