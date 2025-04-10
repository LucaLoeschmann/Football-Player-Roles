import streamlit as st
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.stats import percentileofscore
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go

# --- Streamlit Setup ---
st.set_page_config(page_title="Player Clustering", layout="wide")

# --- Load Data ---
data_dir = "data/"
outfield_df = pd.read_parquet(data_dir + "outfield_df.parquet")

# --- Initial Filter & Cleanup ---
outfield_df = outfield_df[outfield_df["90s"] > 3].fillna(0)

meta_columns = ["Player Name", "Nationality", "Position", "Team", "Competition", "Age"]  # Removed Year Born

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

# --- Final Role Mapping  ---
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

# --- Radar Chart Feature Set ---
radar_columns_outfield = [
    "Goals-PK", "npxG", "Shots", "Assists", "xAG", "npxG+xAG", "SCA",
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

outfield_df_per90 = calculate_per90_stats(outfield_df, radar_columns_outfield)

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

outfield_df_percentiles = calculate_percentiles(outfield_df_per90, radar_columns_outfield)

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

# --- Streamlit UI ---
st.title("Player Clustering")
st.sidebar.header("Spielerauswahl")

selected_player = st.sidebar.selectbox("Wähle einen Spieler", outfield_df['Player Name'].unique())
player_cluster = outfield_df[outfield_df['Player Name'] == selected_player]['Cluster'].values[0]
role_name = role_mapping.get(player_cluster, "")
st.sidebar.markdown(f"**{selected_player}** ist in Cluster {player_cluster} → {role_name}")

st.write(f"### Spieler in Cluster {player_cluster} – {role_name}")
cluster_data = outfield_df[outfield_df['Cluster'] == player_cluster]
st.dataframe(cluster_data[meta_columns])

st.sidebar.subheader("Vergleich: Radar Chart")
player_options = outfield_df['Player Name'].unique()
selected_players = st.sidebar.multiselect("Spieler zum Vergleichen auswählen", options=player_options, default=[selected_player])

if selected_players:
    radar_chart = create_radar_plot(outfield_df_percentiles, selected_players, radar_columns_outfield)
    st.plotly_chart(radar_chart)
else:
    st.info("Bitte wähle mindestens einen Spieler für den Vergleich.")

st.sidebar.subheader("Cluster manuell auswählen")
manual_cluster = st.sidebar.selectbox("Cluster wählen", sorted(outfield_df['Cluster'].unique()))
manual_cluster_data = outfield_df[outfield_df['Cluster'] == manual_cluster]
st.write(f"### Alle Spieler in Cluster {manual_cluster} – {role_mapping.get(manual_cluster, '')}")
st.dataframe(manual_cluster_data[meta_columns])
