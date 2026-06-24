import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

API_URL = "http://fastapi:8000"

st.set_page_config(page_title="SmartCart Segmentation", page_icon="🛒", layout="wide")

st.title("🛒 SmartCart — Customer Segmentation Dashboard")
st.caption("Upload your customer CSV, choose clustering settings, and explore segments.")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    method = st.selectbox("Clustering Method", ["agglomerative", "kmeans"])
    n_clusters = st.slider("Number of Clusters", 2, 8, 4)
    st.markdown("---")
    st.info("Required CSV columns listed below")

uploaded = st.file_uploader("Upload Customer CSV", type=["csv"])

if uploaded:
    df_preview = pd.read_csv(uploaded)
    uploaded.seek(0)

    with st.expander("📄 Raw Data Preview", expanded=False):
        st.dataframe(df_preview.head(10), use_container_width=True)
        st.caption(f"{df_preview.shape[0]} rows × {df_preview.shape[1]} columns")

    col1, col2 = st.columns(2)

    # ---------------- OPTIMAL K ----------------
    with col1:
        if st.button("🔍 Find Optimal K", use_container_width=True):
            with st.spinner("Analyzing elbow & silhouette scores..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/optimal-k",
                        files={"file": ("data.csv", uploaded, "text/csv")}
                    )
                    uploaded.seek(0)

                    if resp.status_code != 200:
                        st.error(resp.text)
                        st.stop()

                    try:
                        data = resp.json()
                    except:
                        st.error("API JSON नहीं दे रहा है")
                        st.write(resp.text)
                        st.stop()

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=data["k_range"],
                        y=data["wcss"],
                        name="WCSS",
                        mode="lines+markers",
                        yaxis="y1"
                    ))

                    fig.add_trace(go.Scatter(
                        x=data["k_range"],
                        y=data["silhouette_scores"],
                        name="Silhouette",
                        mode="lines+markers",
                        yaxis="y2",
                        line=dict(dash="dash", color="red")
                    ))

                    fig.update_layout(
                        title="Elbow & Silhouette Analysis",
                        yaxis=dict(title="WCSS"),
                        yaxis2=dict(title="Silhouette Score", overlaying="y", side="right"),
                        xaxis_title="K",
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.success(
                        f"Recommended K: {data['optimal_k_elbow']} (elbow) · "
                        f"{data['optimal_k_silhouette']} (silhouette)"
                    )

                except Exception as e:
                    st.error(f"API error: {e}")

    # ---------------- SEGMENTATION ----------------
    with col2:
        if st.button("🚀 Run Segmentation", use_container_width=True):
            with st.spinner("Clustering customers..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/segment",
                        files={"file": ("data.csv", uploaded, "text/csv")},
                        params={"n_clusters": n_clusters, "method": method},
                    )

                    uploaded.seek(0)

                    if resp.status_code != 200:
                        st.error(resp.text)
                        st.stop()

                    try:
                        result = resp.json()
                    except:
                        st.error("API JSON नहीं दे रहा है")
                        st.write(resp.text)
                        st.stop()

                    st.session_state["result"] = result

                except Exception as e:
                    st.error(f"API error: {e}")

    # ---------------- RESULTS ----------------
    if "result" in st.session_state:
        result = st.session_state["result"]

        st.markdown("---")

        m1, m2, m3, m4 = st.columns(4)

        st.write(result)

        m1.metric("Customers", result["n_customers"])
        m2.metric("Clusters", result["n_clusters"])
        m3.metric("Method", result["method"].capitalize())
        m4.metric("Silhouette Score", result["silhouette_score"])

        # 3D scatter
        pca_df = pd.DataFrame(result["pca_points"])
        pca_df["cluster"] = pca_df["cluster"].astype(str)

        fig3d = px.scatter_3d(
            pca_df,
            x="x",
            y="y",
            z="z",
            color="cluster",
            title="3D PCA Cluster Visualization",
            labels={"x": "PC1", "y": "PC2", "z": "PC3"},
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        st.plotly_chart(fig3d, use_container_width=True)

        col_a, col_b = st.columns(2)

        with col_a:
            counts = result["cluster_counts"]

            fig_bar = px.bar(
                x=list(counts.keys()),
                y=list(counts.values()),
                labels={"x": "Cluster", "y": "Count"},
                title="Customer Count per Cluster",
                color=list(counts.keys()),
                color_discrete_sequence=px.colors.qualitative.Bold
            )

            st.plotly_chart(fig_bar, use_container_width=True)

        with col_b:
            summary = result["cluster_summary"]

            if "Income" in summary and "Total_Spending" in summary:
                clusters = list(summary["Income"].keys())
                incomes = [summary["Income"][k] for k in clusters]
                spendings = [summary["Total_Spending"][k] for k in clusters]

                fig_sc = px.scatter(
                    x=spendings,
                    y=incomes,
                    text=[f"Cluster {c}" for c in clusters],
                    labels={"x": "Avg Spending", "y": "Avg Income"},
                    title="Income vs Spending by Cluster",
                    color=[str(c) for c in clusters],
                    color_discrete_sequence=px.colors.qualitative.Bold
                )

                fig_sc.update_traces(textposition="top center", marker_size=14)
                st.plotly_chart(fig_sc, use_container_width=True)

        with st.expander("📊 Cluster Summary Table"):
            for metric, vals in result["cluster_summary"].items():
                st.write(f"**{metric}**")
                st.dataframe(pd.DataFrame(vals, index=["value"]).T, use_container_width=True)

else:
    st.info("👆 Upload a CSV file to get started.")