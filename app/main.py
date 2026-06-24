from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
from kneed import KneeLocator
import io

app = FastAPI(title="SmartCart Customer Segmentation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- PREPROCESS ----------------
def preprocess(df: pd.DataFrame):
    df = df.copy()

    df["Income"] = df["Income"].fillna(df["Income"].median())

    df["Age"] = 2026 - df["Year_Birth"]

    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Dt_Customer"])

    reference_date = df["Dt_Customer"].max()
    df["Customer_Tenure_Days"] = (reference_date - df["Dt_Customer"]).dt.days

    spending_raw = [
        "MntFishProducts", "MntFruits", "MntMeatProducts",
        "MntSweetProducts", "MntWines"
    ]
    df["Total_Spending"] = df[spending_raw].sum(axis=1)
    df["Total_Children"] = df["Kidhome"] + df["Teenhome"]

    df["Education"] = df["Education"].replace({
        "Basic": "Undergraduate",
        "2n Cycle": "Undergraduate",
        "Graduation": "Graduate",
        "Master": "Postgraduate",
        "PhD": "Postgraduate"
    })

    df["Living_With"] = df["Marital_Status"].replace({
        "Married": "Partner",
        "Together": "Partner",
        "Single": "Alone",
        "Divorced": "Alone",
        "Widow": "Alone",
        "Absurd": "Alone",
        "YOLO": "Alone"
    })

    drop_cols = [
        "ID", "Year_Birth", "Marital_Status",
        "Kidhome", "Teenhome", "Dt_Customer",
        "MntWines", "MntFruits", "MntMeatProducts",
        "MntFishProducts", "MntSweetProducts", "MntGoldProds"
    ]

    df_cleaned = df.drop(columns=[c for c in drop_cols if c in df.columns])

    df_cleaned = df_cleaned[
        (df_cleaned["Age"] < 90) &
        (df_cleaned["Income"] < 600000)
    ]

    cat_cols = ["Education", "Living_With"]

    ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    enc_arr = ohe.fit_transform(df_cleaned[cat_cols])

    enc_df = pd.DataFrame(
        enc_arr,
        columns=ohe.get_feature_names_out(cat_cols),
        index=df_cleaned.index
    )

    df_encoded = pd.concat(
        [df_cleaned.drop(columns=cat_cols), enc_df],
        axis=1
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_encoded)

    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_scaled)

    return df_encoded, X_pca, pca.explained_variance_ratio_.tolist()


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "SmartCart Segmentation API is running"}


# ---------------- SEGMENT ----------------
@app.post("/segment")
async def segment_customers(
    file: UploadFile = File(...),
    n_clusters: int = 4,
    method: str = "agglomerative"
):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    try:
        df_encoded, X_pca, variance_ratio = preprocess(df)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    if method == "kmeans":
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    else:
        model = AgglomerativeClustering(n_clusters=n_clusters)

    labels = model.fit_predict(X_pca)
    df_encoded["cluster"] = labels

    # SAFE silhouette (IMPORTANT FIX)
    sil = None
    if len(set(labels)) > 1:
        sil = silhouette_score(X_pca, labels)
    else:
        sil = 0.0

    cluster_summary = df_encoded.groupby("cluster").mean().round(2).to_dict()

    pca_points = [
        {
            "x": float(X_pca[i, 0]),
            "y": float(X_pca[i, 1]),
            "z": float(X_pca[i, 2]),
            "cluster": int(labels[i])
        }
        for i in range(len(labels))
    ]

    return {
        "n_customers": int(len(df_encoded)),
        "n_clusters": int(n_clusters),
        "method": method,
        "silhouette_score": float(round(sil, 4)),
        "explained_variance_ratio": variance_ratio,
        "cluster_summary": cluster_summary,
        "pca_points": pca_points,
        "cluster_counts": df_encoded["cluster"].value_counts().to_dict(),
    }


# ---------------- OPTIMAL K ----------------
@app.post("/optimal-k")
async def find_optimal_k(file: UploadFile = File(...)):

    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    try:
        _, X_pca, _ = preprocess(df)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    wcss = []
    sil_scores = []

    for k in range(2, 11):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        lbl = km.fit_predict(X_pca)

        wcss.append(float(km.inertia_))
        sil_scores.append(float(silhouette_score(X_pca, lbl)))

    knee = KneeLocator(range(2, 11), wcss, curve="convex", direction="decreasing")

    return {
        "k_range": list(range(2, 11)),
        "wcss": wcss,
        "silhouette_scores": sil_scores,
        "optimal_k_elbow": int(knee.elbow) if knee.elbow else 4,
        "optimal_k_silhouette": int(np.argmax(sil_scores) + 2),
    }