# Football-Player-Clustering

This project clusters professional football players based on their **playing styles**, not just positions or quality. It uses advanced statistical techniques to uncover **tactical roles** from performance data – similar to approaches used by StatsBomb, Smarterscout, and Liverpool FC's analytics department.

## 🔗 Streamlit App  
👉 [Click here to try the app]([https://scouting25.streamlit.app/](https://football-player-clustering.streamlit.app))

---

## 📚 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [🧪 Methodology](#-methodolodgy)
- [🎯 Project Goals](#-project-goals)
- [✨ Key Features](#-key-features)
- [🔧 Future Improvements](#-future-improvements)
- [📢 Disclaimer](#-disclaimer)

---

## 📖 Project Overview

The traditional classification of football players into Defenders, Midfielders, and Forwards has long been outdated. For years, football analysts have moved beyond these oversimplified categories. While positional labels may still provide a rough idea of a player’s function, they fall short in capturing the full complexity of individual playing styles.

The ongoing data revolution in elite football now makes it possible to identify **nuanced player roles** and to break them down further into specific profiles. What if players weren't defined solely by their position on paper — which is often static and fails to represent the fluid nature of a 90-minute match?  
What if we could instead track and quantify a player’s **true role on the pitch**, across different situations, tactical instructions, and phases of play?

Beyond basic position groups, even more specific roles can vary significantly depending on:
- tactical system
- formation
- and individual player traits
- a players individual interpretation of a role  

Two players listed as full-backs might play entirely different roles:
- One may act as an attacking wide creator, overlapping like a winger,
- the other may stay deep and focus solely on defensive duties.

Likewise, a defensive midfielder (No. 6) might either:
- dictate the game with his passing,
- primarily function as a destroyer, breaking up opposition attacks.

---

To explore these ideas and expand my understanding of modern football, I began studying the concept of **stylistic player role clustering**. My goal was to develop a system that could help identify and interpret player functions beyond traditional positions.

This project draws on insights from various academic papers, blog articles, and football analytics literature.  
A special inspiration came from the book *"How to Win the Premier League"* by Ian Graham, former Director of Research at Liverpool FC — which sparked the initial motivation to build this system.

---

## 🧪 Methodology

- **Data Source**: Match events from top European leagues
- **Feature Engineering**:
  - Per-90 normalization
  - Success rates & zone distributions
  - Contextual play types (e.g. progressive passes, key passes, dribbles)
- **Dimensionality Reduction**:
  - PCA (90–95% variance retained)
- **Clustering Algorithms**:
  - KMeans
  - Ward’s Hierarchical Clustering
  - PAM (Partitioning Around Medoids)
- **Validation Metrics**:
  - Silhouette Score
  - Entropy (cluster balance)
  - Bootstrap Stability
  - Aggregated index with custom weights (composite quality score)

---

## 🎯 Project Goals

1. Identify **tactical player archetypes** based on behavior
2. Provide a **stylistic scouting tool** to find similar profiles
3. Enable **player comparison** based on roles
4. Visualize role landscapes with **UMAP** and interactive plots

---

## ✨ Key Features

- 🧩 Two-layer clustering logic:
  - **Macro clusters** (5–10 groups) for high-level role segmentation
  - **Micro clusters** (100–150 groups) for finding near-identical profiles
- 🎨 Visual role maps with UMAP
- 🧠 Expert-inspired feature design (proportions, success rates, play types)
- 🔁 Bootstrap-based **cluster stability analysis**
- 🤖 Ready for supervised extension: role classification via Random Forest or XGBoost

---

## 🔧 Future Improvements

- [ ] Integration of tracking data (heatmaps, movement profiles)
- [ ] Expert feedback on cluster labels (via survey)
- [ ] Streamlit dashboard optimization
- [ ] Full model pipeline for new player classification

---

## 📢 Disclaimer

This project is intended **solely for educational and personal portfolio use**.  
It is **not affiliated with or endorsed by FBref.com, Sports Reference LLC, or their data providers**.

Player data used in this app was sourced from publicly available web pages on FBref.com and is presented for analysis and research purposes.  
The app does **not reproduce a complete database**, does **not offer any form of commercial service**, and is **not intended to compete with FBref or any related platform**.

All data remains the intellectual property of its respective owners.
