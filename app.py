# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from sklearn.decomposition import PCA
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import LabelEncoder

# # ── Page config ──────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="🦁 Zoo Animal Explorer",
#     page_icon="🦁",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ── Column metadata ───────────────────────────────────────────────────────────
# FEATURE_COLS = {
#     "1":  "Hair",
#     "2":  "Feathers",
#     "3":  "Eggs",
#     "4":  "Milk",
#     "5":  "Airborne",
#     "6":  "Aquatic",
#     "7":  "Predator",
#     "8":  "Toothed",
#     "9":  "Backbone",
#     "10": "Breathes",
#     "11": "Venomous",
#     "12": "Fins",
#     "13": "Legs",
#     "14": "Tail",
#     "15": "Domestic",
#     "16": "Catsize",
#     "17": "Class Type",
# }

# CLASS_NAMES = {
#     1: "Mammal", 2: "Bird", 3: "Reptile",
#     4: "Fish",   5: "Amphibian", 6: "Bug", 7: "Invertebrate",
# }

# CLASS_COLORS = {
#     "Mammal": "#e74c3c", "Bird": "#3498db", "Reptile": "#2ecc71",
#     "Fish": "#9b59b6", "Amphibian": "#f39c12", "Bug": "#1abc9c",
#     "Invertebrate": "#e67e22",
# }

# # ── Load data ─────────────────────────────────────────────────────────────────
# from pathlib import Path

# @st.cache_data
# def load_data(file=None):
#     if file is not None:
#         df = pd.read_csv(file)
#     else:
#         # Look for CSV next to this script (works locally & on Streamlit Cloud)
#         csv_path = Path(__file__).parent / "zoo_converted.csv"
#         df = pd.read_csv(csv_path)
#     df.columns = ["Animal"] + list(FEATURE_COLS.keys())
#     df.rename(columns=FEATURE_COLS, inplace=True)
#     df["Class Name"] = df["Class Type"].map(CLASS_NAMES)
#     df["Animal"] = df["Animal"].str.title()
#     return df

# # Try loading automatically; show uploader if file is missing
# csv_path = Path(__file__).parent / "zoo_converted.csv"
# if csv_path.exists():
#     df = load_data()
# else:
#     st.warning("⚠️ `zoo_converted.csv` not found. Please upload the file below.")
#     uploaded = st.file_uploader("Upload zoo_converted.csv", type="csv")
#     if uploaded is None:
#         st.stop()
#     df = load_data(uploaded)

# BINARY_FEATURES = [c for c in FEATURE_COLS.values() if c not in ("Legs", "Class Type")]

# # ── Sidebar ───────────────────────────────────────────────────────────────────
# st.sidebar.image("https://em-content.zobj.net/source/apple/391/lion_1f981.png", width=80)
# st.sidebar.title("🦁 Zoo Explorer")
# st.sidebar.markdown("---")

# page = st.sidebar.radio(
#     "Navigate",
#     ["📊 Overview", "🔍 Animal Lookup", "📈 Feature Analysis", "🗺️ PCA Explorer", "🤖 Cluster Finder"],
# )

# selected_classes = st.sidebar.multiselect(
#     "Filter by Class",
#     options=list(CLASS_NAMES.values()),
#     default=list(CLASS_NAMES.values()),
# )

# filtered_df = df[df["Class Name"].isin(selected_classes)]

# st.sidebar.markdown("---")
# st.sidebar.caption(f"Showing **{len(filtered_df)}** of **{len(df)}** animals")

# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE 1 – OVERVIEW
# # ═══════════════════════════════════════════════════════════════════════════════
# if page == "📊 Overview":
#     st.title("🦁 Zoo Animal Dataset Explorer")
#     st.markdown("Explore **101 animals** across **7 classes** with **16 biological features**.")

#     # KPI row
#     c1, c2, c3, c4 = st.columns(4)
#     c1.metric("Total Animals", len(filtered_df))
#     c2.metric("Animal Classes", filtered_df["Class Name"].nunique())
#     c3.metric("Predators", int(filtered_df["Predator"].sum()))
#     c4.metric("Domestic Animals", int(filtered_df["Domestic"].sum()))

#     st.markdown("---")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Animals per Class")
#         class_counts = filtered_df["Class Name"].value_counts().reset_index()
#         class_counts.columns = ["Class", "Count"]
#         fig = px.bar(
#             class_counts, x="Class", y="Count", color="Class",
#             color_discrete_map=CLASS_COLORS, text="Count",
#         )
#         fig.update_traces(textposition="outside")
#         fig.update_layout(showlegend=False, height=380)
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.subheader("Class Distribution")
#         fig2 = px.pie(
#             class_counts, names="Class", values="Count",
#             color="Class", color_discrete_map=CLASS_COLORS,
#             hole=0.4,
#         )
#         fig2.update_layout(height=380)
#         st.plotly_chart(fig2, use_container_width=True)

#     st.subheader("📋 Raw Data Table")
#     st.dataframe(
#         filtered_df.drop(columns=["Class Type"]).style.background_gradient(
#             subset=BINARY_FEATURES, cmap="Blues"
#         ),
#         use_container_width=True,
#         height=400,
#     )

# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE 2 – ANIMAL LOOKUP
# # ═══════════════════════════════════════════════════════════════════════════════
# elif page == "🔍 Animal Lookup":
#     st.title("🔍 Animal Lookup")
#     st.markdown("Search for any animal and see its full feature profile.")

#     animal_list = sorted(filtered_df["Animal"].tolist())
#     selected_animal = st.selectbox("Choose an animal", animal_list)

#     row = filtered_df[filtered_df["Animal"] == selected_animal].iloc[0]

#     col1, col2 = st.columns([1, 2])
#     with col1:
#         cls = row["Class Name"]
#         st.markdown(f"### {selected_animal}")
#         st.markdown(f"**Class:** `{cls}`")
#         st.markdown(f"**Legs:** `{int(row['Legs'])}`")

#         tags = []
#         for feat in BINARY_FEATURES:
#             if row[feat] == 1:
#                 tags.append(f"`{feat}`")
#         st.markdown("**Traits:** " + "  ".join(tags) if tags else "_No binary traits_")

#     with col2:
#         feat_vals = {f: int(row[f]) for f in BINARY_FEATURES}
#         fig = go.Figure(go.Bar(
#             x=list(feat_vals.keys()),
#             y=list(feat_vals.values()),
#             marker_color=[CLASS_COLORS.get(cls, "#888") if v == 1 else "#ddd" for v in feat_vals.values()],
#         ))
#         fig.update_layout(
#             title=f"Feature Profile – {selected_animal}",
#             yaxis=dict(tickvals=[0, 1], ticktext=["No", "Yes"]),
#             height=350,
#         )
#         st.plotly_chart(fig, use_container_width=True)

#     st.markdown("---")
#     st.subheader("Similar Animals (same class)")
#     same_class = filtered_df[
#         (filtered_df["Class Name"] == row["Class Name"]) &
#         (filtered_df["Animal"] != selected_animal)
#     ][["Animal", "Legs"] + BINARY_FEATURES[:8]].reset_index(drop=True)
#     st.dataframe(same_class, use_container_width=True)

# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE 3 – FEATURE ANALYSIS
# # ═══════════════════════════════════════════════════════════════════════════════
# elif page == "📈 Feature Analysis":
#     st.title("📈 Feature Analysis")

#     tab1, tab2, tab3 = st.tabs(["Feature Prevalence", "Class vs Feature Heatmap", "Legs Distribution"])

#     with tab1:
#         st.subheader("How common is each feature?")
#         prevalence = filtered_df[BINARY_FEATURES].mean().sort_values(ascending=False).reset_index()
#         prevalence.columns = ["Feature", "Prevalence"]
#         prevalence["Prevalence %"] = (prevalence["Prevalence"] * 100).round(1)
#         fig = px.bar(
#             prevalence, x="Feature", y="Prevalence %", color="Prevalence %",
#             color_continuous_scale="teal", text="Prevalence %",
#         )
#         fig.update_traces(texttemplate="%{text}%", textposition="outside")
#         fig.update_layout(height=420, coloraxis_showscale=False)
#         st.plotly_chart(fig, use_container_width=True)

#     with tab2:
#         st.subheader("Average feature value per class")
#         heatmap_data = (
#             filtered_df.groupby("Class Name")[BINARY_FEATURES].mean().round(2)
#         )
#         fig = px.imshow(
#             heatmap_data, text_auto=True, aspect="auto",
#             color_continuous_scale="RdYlGn", zmin=0, zmax=1,
#         )
#         fig.update_layout(height=420)
#         st.plotly_chart(fig, use_container_width=True)

#     with tab3:
#         st.subheader("Leg count distribution across classes")
#         fig = px.histogram(
#             filtered_df, x="Legs", color="Class Name",
#             color_discrete_map=CLASS_COLORS, barmode="group",
#             nbins=10,
#         )
#         fig.update_layout(height=400)
#         st.plotly_chart(fig, use_container_width=True)

#         st.subheader("Legs by Class (Box Plot)")
#         fig2 = px.box(
#             filtered_df, x="Class Name", y="Legs", color="Class Name",
#             color_discrete_map=CLASS_COLORS, points="all",
#         )
#         fig2.update_layout(height=400, showlegend=False)
#         st.plotly_chart(fig2, use_container_width=True)

# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE 4 – PCA EXPLORER
# # ═══════════════════════════════════════════════════════════════════════════════
# elif page == "🗺️ PCA Explorer":
#     st.title("🗺️ PCA Explorer")
#     st.markdown("Reduce 16 features to 2D/3D to visualise animal groupings.")

#     mode = st.radio("Dimensions", ["2D", "3D"], horizontal=True)

#     features_for_pca = BINARY_FEATURES + ["Legs"]
#     X = filtered_df[features_for_pca].values

#     n_components = 3 if mode == "3D" else 2
#     pca = PCA(n_components=n_components)
#     components = pca.fit_transform(X)
#     var_explained = (pca.explained_variance_ratio_ * 100).round(1)

#     pca_df = filtered_df[["Animal", "Class Name"]].copy()
#     pca_df["PC1"] = components[:, 0]
#     pca_df["PC2"] = components[:, 1]
#     if mode == "3D":
#         pca_df["PC3"] = components[:, 2]

#     if mode == "2D":
#         fig = px.scatter(
#             pca_df, x="PC1", y="PC2", color="Class Name",
#             hover_data=["Animal"],
#             color_discrete_map=CLASS_COLORS,
#             labels={"PC1": f"PC1 ({var_explained[0]}%)", "PC2": f"PC2 ({var_explained[1]}%)"},
#         )
#     else:
#         fig = px.scatter_3d(
#             pca_df, x="PC1", y="PC2", z="PC3", color="Class Name",
#             hover_data=["Animal"],
#             color_discrete_map=CLASS_COLORS,
#             labels={
#                 "PC1": f"PC1 ({var_explained[0]}%)",
#                 "PC2": f"PC2 ({var_explained[1]}%)",
#                 "PC3": f"PC3 ({var_explained[2]}%)",
#             },
#         )

#     fig.update_traces(marker=dict(size=8, opacity=0.85))
#     fig.update_layout(height=550, legend_title="Class")
#     st.plotly_chart(fig, use_container_width=True)

#     total_var = sum(var_explained)
#     st.info(f"**Variance explained:** PC1={var_explained[0]}%  |  PC2={var_explained[1]}%"
#             + (f"  |  PC3={var_explained[2]}%" if mode == "3D" else "")
#             + f"  →  **Total {total_var:.1f}%**")

# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE 5 – CLUSTER FINDER
# # ═══════════════════════════════════════════════════════════════════════════════
# elif page == "🤖 Cluster Finder":
#     st.title("🤖 K-Means Cluster Finder")
#     st.markdown("Group animals using K-Means clustering on their biological features.")

#     n_clusters = st.slider("Number of clusters (k)", min_value=2, max_value=10, value=7)

#     features_km = BINARY_FEATURES + ["Legs"]
#     X = filtered_df[features_km].values

#     km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
#     labels = km.fit_predict(X)

#     pca2 = PCA(n_components=2)
#     coords = pca2.fit_transform(X)
#     var2 = (pca2.explained_variance_ratio_ * 100).round(1)

#     cluster_df = filtered_df[["Animal", "Class Name"]].copy()
#     cluster_df["Cluster"] = labels.astype(str)
#     cluster_df["PC1"] = coords[:, 0]
#     cluster_df["PC2"] = coords[:, 1]

#     fig = px.scatter(
#         cluster_df, x="PC1", y="PC2", color="Cluster",
#         hover_data=["Animal", "Class Name"],
#         symbol="Class Name",
#         labels={"PC1": f"PC1 ({var2[0]}%)", "PC2": f"PC2 ({var2[1]}%)"},
#         title=f"K-Means with k={n_clusters} (PCA 2D projection)",
#     )
#     fig.update_traces(marker=dict(size=9, opacity=0.85))
#     fig.update_layout(height=500)
#     st.plotly_chart(fig, use_container_width=True)

#     st.subheader("Cluster Composition")
#     comp = (
#         cluster_df.groupby(["Cluster", "Class Name"])
#         .size()
#         .reset_index(name="Count")
#     )
#     fig2 = px.bar(
#         comp, x="Cluster", y="Count", color="Class Name",
#         color_discrete_map=CLASS_COLORS, barmode="stack",
#     )
#     fig2.update_layout(height=380)
#     st.plotly_chart(fig2, use_container_width=True)

#     st.subheader("Animals in each Cluster")
#     for c in sorted(cluster_df["Cluster"].unique(), key=int):
#         animals = cluster_df[cluster_df["Cluster"] == c]["Animal"].tolist()
#         with st.expander(f"Cluster {c}  ({len(animals)} animals)"):
#             st.write(", ".join(sorted(animals)))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🦁 Zoo Animal Explorer",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Column metadata ───────────────────────────────────────────────────────────
FEATURE_COLS = {
    "1":  "Hair",
    "2":  "Feathers",
    "3":  "Eggs",
    "4":  "Milk",
    "5":  "Airborne",
    "6":  "Aquatic",
    "7":  "Predator",
    "8":  "Toothed",
    "9":  "Backbone",
    "10": "Breathes",
    "11": "Venomous",
    "12": "Fins",
    "13": "Legs",
    "14": "Tail",
    "15": "Domestic",
    "16": "Catsize",
    "17": "Class Type",
}

CLASS_NAMES = {
    1: "Mammal", 2: "Bird", 3: "Reptile",
    4: "Fish",   5: "Amphibian", 6: "Bug", 7: "Invertebrate",
}

CLASS_COLORS = {
    "Mammal": "#e74c3c", "Bird": "#3498db", "Reptile": "#2ecc71",
    "Fish": "#9b59b6", "Amphibian": "#f39c12", "Bug": "#1abc9c",
    "Invertebrate": "#e67e22",
}

# ── Load data ─────────────────────────────────────────────────────────────────
from pathlib import Path

@st.cache_data
def load_data():
    csv_path = Path(__file__).parent / "zoo_converted.csv"
    df = pd.read_csv(csv_path)
    df.columns = ["Animal"] + list(FEATURE_COLS.keys())
    df.rename(columns=FEATURE_COLS, inplace=True)
    df["Class Name"] = df["Class Type"].map(CLASS_NAMES)
    df["Animal"] = df["Animal"].str.title()
    return df

df = load_data()

BINARY_FEATURES = [c for c in FEATURE_COLS.values() if c not in ("Legs", "Class Type")]

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://em-content.zobj.net/source/apple/391/lion_1f981.png", width=80)
st.sidebar.title("🦁 Zoo Explorer")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "🔍 Animal Lookup", "📈 Feature Analysis", "🗺️ PCA Explorer", "🤖 Cluster Finder"],
)

selected_classes = st.sidebar.multiselect(
    "Filter by Class",
    options=list(CLASS_NAMES.values()),
    default=list(CLASS_NAMES.values()),
)

filtered_df = df[df["Class Name"].isin(selected_classes)]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(filtered_df)}** of **{len(df)}** animals")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 – OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📊 Overview":
    st.title("🦁 Zoo Animal Dataset Explorer")
    st.markdown("Explore **101 animals** across **7 classes** with **16 biological features**.")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Animals", len(filtered_df))
    c2.metric("Animal Classes", filtered_df["Class Name"].nunique())
    c3.metric("Predators", int(filtered_df["Predator"].sum()))
    c4.metric("Domestic Animals", int(filtered_df["Domestic"].sum()))

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Animals per Class")
        class_counts = filtered_df["Class Name"].value_counts().reset_index()
        class_counts.columns = ["Class", "Count"]
        fig = px.bar(
            class_counts, x="Class", y="Count", color="Class",
            color_discrete_map=CLASS_COLORS, text="Count",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Class Distribution")
        fig2 = px.pie(
            class_counts, names="Class", values="Count",
            color="Class", color_discrete_map=CLASS_COLORS,
            hole=0.4,
        )
        fig2.update_layout(height=380)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Raw Data Table")
    st.dataframe(
        filtered_df.drop(columns=["Class Type"]),
        use_container_width=True,
        height=400,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – ANIMAL LOOKUP
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Animal Lookup":
    st.title("🔍 Animal Lookup")
    st.markdown("Search for any animal and see its full feature profile.")

    animal_list = sorted(filtered_df["Animal"].tolist())
    selected_animal = st.selectbox("Choose an animal", animal_list)

    row = filtered_df[filtered_df["Animal"] == selected_animal].iloc[0]

    col1, col2 = st.columns([1, 2])
    with col1:
        cls = row["Class Name"]
        st.markdown(f"### {selected_animal}")
        st.markdown(f"**Class:** `{cls}`")
        st.markdown(f"**Legs:** `{int(row['Legs'])}`")

        tags = []
        for feat in BINARY_FEATURES:
            if row[feat] == 1:
                tags.append(f"`{feat}`")
        st.markdown("**Traits:** " + "  ".join(tags) if tags else "_No binary traits_")

    with col2:
        feat_vals = {f: int(row[f]) for f in BINARY_FEATURES}
        fig = go.Figure(go.Bar(
            x=list(feat_vals.keys()),
            y=list(feat_vals.values()),
            marker_color=[CLASS_COLORS.get(cls, "#888") if v == 1 else "#ddd" for v in feat_vals.values()],
        ))
        fig.update_layout(
            title=f"Feature Profile – {selected_animal}",
            yaxis=dict(tickvals=[0, 1], ticktext=["No", "Yes"]),
            height=350,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Similar Animals (same class)")
    same_class = filtered_df[
        (filtered_df["Class Name"] == row["Class Name"]) &
        (filtered_df["Animal"] != selected_animal)
    ][["Animal", "Legs"] + BINARY_FEATURES[:8]].reset_index(drop=True)
    st.dataframe(same_class, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – FEATURE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Feature Analysis":
    st.title("📈 Feature Analysis")

    tab1, tab2, tab3 = st.tabs(["Feature Prevalence", "Class vs Feature Heatmap", "Legs Distribution"])

    with tab1:
        st.subheader("How common is each feature?")
        prevalence = filtered_df[BINARY_FEATURES].mean().sort_values(ascending=False).reset_index()
        prevalence.columns = ["Feature", "Prevalence"]
        prevalence["Prevalence %"] = (prevalence["Prevalence"] * 100).round(1)
        fig = px.bar(
            prevalence, x="Feature", y="Prevalence %", color="Prevalence %",
            color_continuous_scale="teal", text="Prevalence %",
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(height=420, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Average feature value per class")
        heatmap_data = (
            filtered_df.groupby("Class Name")[BINARY_FEATURES].mean().round(2)
        )
        fig = px.imshow(
            heatmap_data, text_auto=True, aspect="auto",
            color_continuous_scale="RdYlGn", zmin=0, zmax=1,
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Leg count distribution across classes")
        fig = px.histogram(
            filtered_df, x="Legs", color="Class Name",
            color_discrete_map=CLASS_COLORS, barmode="group",
            nbins=10,
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Legs by Class (Box Plot)")
        fig2 = px.box(
            filtered_df, x="Class Name", y="Legs", color="Class Name",
            color_discrete_map=CLASS_COLORS, points="all",
        )
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 – PCA EXPLORER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ PCA Explorer":
    st.title("🗺️ PCA Explorer")
    st.markdown("Reduce 16 features to 2D/3D to visualise animal groupings.")

    mode = st.radio("Dimensions", ["2D", "3D"], horizontal=True)

    features_for_pca = BINARY_FEATURES + ["Legs"]
    X = filtered_df[features_for_pca].values

    n_components = 3 if mode == "3D" else 2
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(X)
    var_explained = (pca.explained_variance_ratio_ * 100).round(1)

    pca_df = filtered_df[["Animal", "Class Name"]].copy()
    pca_df["PC1"] = components[:, 0]
    pca_df["PC2"] = components[:, 1]
    if mode == "3D":
        pca_df["PC3"] = components[:, 2]

    if mode == "2D":
        fig = px.scatter(
            pca_df, x="PC1", y="PC2", color="Class Name",
            hover_data=["Animal"],
            color_discrete_map=CLASS_COLORS,
            labels={"PC1": f"PC1 ({var_explained[0]}%)", "PC2": f"PC2 ({var_explained[1]}%)"},
        )
    else:
        fig = px.scatter_3d(
            pca_df, x="PC1", y="PC2", z="PC3", color="Class Name",
            hover_data=["Animal"],
            color_discrete_map=CLASS_COLORS,
            labels={
                "PC1": f"PC1 ({var_explained[0]}%)",
                "PC2": f"PC2 ({var_explained[1]}%)",
                "PC3": f"PC3 ({var_explained[2]}%)",
            },
        )

    fig.update_traces(marker=dict(size=8, opacity=0.85))
    fig.update_layout(height=550, legend_title="Class")
    st.plotly_chart(fig, use_container_width=True)

    total_var = sum(var_explained)
    st.info(f"**Variance explained:** PC1={var_explained[0]}%  |  PC2={var_explained[1]}%"
            + (f"  |  PC3={var_explained[2]}%" if mode == "3D" else "")
            + f"  →  **Total {total_var:.1f}%**")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 – CLUSTER FINDER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 Cluster Finder":
    st.title("🤖 K-Means Cluster Finder")
    st.markdown("Group animals using K-Means clustering on their biological features.")

    n_clusters = st.slider("Number of clusters (k)", min_value=2, max_value=10, value=7)

    features_km = BINARY_FEATURES + ["Legs"]
    X = filtered_df[features_km].values

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(X)

    pca2 = PCA(n_components=2)
    coords = pca2.fit_transform(X)
    var2 = (pca2.explained_variance_ratio_ * 100).round(1)

    cluster_df = filtered_df[["Animal", "Class Name"]].copy()
    cluster_df["Cluster"] = labels.astype(str)
    cluster_df["PC1"] = coords[:, 0]
    cluster_df["PC2"] = coords[:, 1]

    fig = px.scatter(
        cluster_df, x="PC1", y="PC2", color="Cluster",
        hover_data=["Animal", "Class Name"],
        symbol="Class Name",
        labels={"PC1": f"PC1 ({var2[0]}%)", "PC2": f"PC2 ({var2[1]}%)"},
        title=f"K-Means with k={n_clusters} (PCA 2D projection)",
    )
    fig.update_traces(marker=dict(size=9, opacity=0.85))
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cluster Composition")
    comp = (
        cluster_df.groupby(["Cluster", "Class Name"])
        .size()
        .reset_index(name="Count")
    )
    fig2 = px.bar(
        comp, x="Cluster", y="Count", color="Class Name",
        color_discrete_map=CLASS_COLORS, barmode="stack",
    )
    fig2.update_layout(height=380)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Animals in each Cluster")
    for c in sorted(cluster_df["Cluster"].unique(), key=int):
        animals = cluster_df[cluster_df["Cluster"] == c]["Animal"].tolist()
        with st.expander(f"Cluster {c}  ({len(animals)} animals)"):
            st.write(", ".join(sorted(animals)))

