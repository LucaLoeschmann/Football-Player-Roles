# Football-Player-Clustering

This project clusters professional football players based on their **playing styles**, not just positions or quality. It uses advanced statistical techniques to uncover **tactical roles** from performance data – similar to approaches used by StatsBomb, Smarterscout, and Liverpool FC's analytics department.

## 🔗 Streamlit App  
👉 [Click here to try the app](https://scouting25.streamlit.app/)

---

## 📚 Table of Contents

- [Overview](#overview)
- [Methodology](#methodology)
- [Project Goals](#project-goals)
- [Key Features](#key-features)
- [Future Improvements](#future-improvements)
- [Project Structure](#project-structure)
- [Inspiration](#inspiration)
- [Author](#author)

---

## 📖 Overview

This project explores unsupervised learning to identify **stylistic player roles** using match event data per 90 minutes. The goal is to uncover **underlying behavioral patterns**, such as:

- Inverted Fullbacks
- Deep-Lying Playmakers
- Press-Resistant Midfielders
- Wide Creators

All clusters are generated based on how players act on the pitch – not their nominal position.

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
