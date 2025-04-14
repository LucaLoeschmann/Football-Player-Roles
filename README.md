# Football Player Role Explorer

This project clusters professional football players based on their **playing styles**, not just positions or performance level. It leverages statistical modeling and dimensionality reduction to uncover **stylistic player roles** – inspired by modern approaches from clubs like Liverpool FC and platforms like StatsBomb or Smarterscout.

## 🔗 Streamlit App
👉 [Click here to try the app](https://football-player-clustering.streamlit.app)

---

## 📚 Table of Contents

- [📖 Project Overview](#-project-overview)
- [🧪 Methodology](#-methodology)
- [🎯 Project Goals](#-project-goals)
- [✨ Key Features](#-key-features)
- [🧠 Role Logic & Feature Design](#-role-logic--feature-design)
- [📊 UMAP & Multi-Role Projection](#-umap--multi-role-projection)
- [🔧 Future Improvements](#-future-improvements)
- [📢 Disclaimer](#-disclaimer)

---

## 📖 Project Overview

The traditional classification of football players into Defenders, Midfielders, and Forwards has long been outdated. For years, football analysts have moved beyond these oversimplified categories. While positional labels may still provide a rough idea of a player’s function, they fall short in capturing the full complexity of individual playing styles.

The ongoing data revolution in elite football now makes it possible to identify **nuanced player roles** and to break them down further into specific profiles. What if players weren't defined solely by their position on paper — which is often static and fails to represent the fluid nature of a 90-minute match? What if we could instead track and quantify a player’s **true role on the pitch**, across different situations, tactical instructions, and phases of play?

Two players listed as full-backs might play entirely different roles:
- One may act as an attacking wide creator, overlapping like a winger,
- The other may stay deep and focus solely on defensive duties.

Likewise, a defensive midfielder (No. 6) might either:
- Dictate the game with his passing,
- Or function primarily as a destroyer, breaking up opposition attacks.

To explore these ideas and build a data-driven perspective on role interpretation, I created this clustering model that tries to answer: **How can we best group players based on what they do – not where they stand?**

---

## 🧪 Methodology

- **Data Source**: FBref.com (top European leagues)
- **Feature Engineering**:
  - Per-90 normalization for all performance metrics
  - Carefully selected features representing attacking, possession, and defensive behavior
  - Aggregated by player-season
- **Dimensionality Reduction**:
  - PCA with `n_components=0.93` (retaining ~93% explained variance)
- **Clustering Algorithms**:
  - Ward’s Hierarchical Clustering (primary)
  - Other methods (KMeans, PAM) tested during prototyping
- **Validation Metrics**:
  - Silhouette Score (internal cohesion)
  - Cross-validation with bootstrapped stability metrics
  - Composite role quality index used to choose optimal PCA depth and cluster count (n=12)

---

## 🎯 Project Goals

1. Identify **stylistic player archetypes** based on in-match behavior
2. Provide a **scouting and comparison tool** using role-based context
3. Visualize the high-dimensional structure of football styles in a **digestible format**
4. Build a foundation for **future supervised models** of role classification

---

## ✨ Key Features

- 🧩 **12 Clusters** based on tactical player function (not fixed position)
- 🎯 Interactive **Radar Chart**: Compare multiple players across percentile-normalized attributes
- 🌍 **UMAP Projection**: View stylistic neighborhoods of players in a compressed 2D landscape
- 📚 All metrics used are normalized per-90 and selected to reflect actual football usage:
  - **Possession & Build-up**: Passes, progressive passes, completions
  - **Chance Creation**: xAG, key passes, SCA, crosses
  - **Ball Progression**: Carries, progressive carries, final third involvement
  - **Defensive Profile**: Tackles, interceptions, blocks, aerial duels
  - **Attacking Output**: Shots, npxG, assists

---

## 🧠 Role Logic & Feature Design

The model is heavily inspired by the work of Ian Graham (Liverpool FC) and others who emphasize **behavior-based grouping** over label-driven categorization. Rather than predefining roles, the model identifies statistical similarities in how players contribute on the pitch.

Feature selection was driven by relevance to role detection, not performance rating. Metrics like "Miscontrols" or "Touches in Final Third" were included because they describe **how** a player engages with the game, not **how well**.

The final clusters were **manually interpreted** and assigned descriptive role labels like:
- "No.10 / Playmaker"
- "Inverted Fullback"
- "Target Man"

These are not fixed truths — just approximations to help explore a role landscape.

---

## 📊 UMAP & Multi-Role Projection

One of the key features of this project is the **UMAP-based 2D visualization**, which takes the 17-dimensional PCA output and reduces it to two dimensions.

Why? Because cluster numbers don't tell the whole story. Players in different clusters might still be very close in playstyle — and vice versa. The UMAP projection provides:
- A **bird’s-eye view** of how similar or dissimilar players are
- Context when players seem misclassified (e.g., creative fullbacks vs. inverted wingers)
- Insight into **stylistic overlap** between clusters

The map is designed as a **topological simplification** — a tool to aid intuition, not exact science. But it can help answer questions like:
- Who plays most similarly to a given player?
- Are there clusters that visibly overlap?
- Which roles are most distinct?

---

## 🔧 Future Improvements

- [ ] Integrate tracking data (heatmaps, zones)
- [ ] Include player-season dynamics (year-over-year role shift)
- [ ] Add feedback loop for expert review of roles

---

## 📢 Disclaimer

This project is intended **solely for educational and personal portfolio purposes**. It is not affiliated with or endorsed by FBref.com, StatsBomb, or any football clubs or data providers.

All data remains the property of its respective owners. The app does not recreate full datasets, and no commercial service is offered.

---
