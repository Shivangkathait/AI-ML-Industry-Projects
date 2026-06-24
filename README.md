# 🛒 SmartCart Customer Segmentation System

## Project Summary

Developed an AI-powered Customer Segmentation System for SmartCart, an e-commerce platform, using Machine Learning, FastAPI, Streamlit, and Docker.

The application analyzes customer demographics, purchasing behavior, website activity, and engagement metrics to automatically identify meaningful customer segments and generate actionable business insights through an interactive dashboard and REST API.

---

## Live Application

**Deployed Application:** https://smartcart-ai-shivang.streamlit.app

**API Documentation:** https://ai-ml-industry.onrender.com/docs

**GitHub Repository:** https://github.com/Shivangkathait/AI-ML-Industry-Projects

---

## Business Objective

The objective of this project is to help SmartCart:

* Understand customer purchasing patterns
* Identify high-value customers
* Detect low-engagement customers
* Improve customer retention
* Optimize marketing campaigns
* Support data-driven business decisions
* Enable targeted customer segmentation
* Improve overall business performance through analytics

---

## Dataset Information

**Total Records:** 2,240 Customers

**Features:** 22

### Data Categories

* Customer Demographics
* Income Information
* Spending Behavior
* Purchase Frequency
* Website Activity
* Campaign Response
* Customer Engagement

---

## Solution Architecture

Data Collection

↓

Data Cleaning

↓

Exploratory Data Analysis

↓

Feature Engineering

↓

Data Standardization

↓

Principal Component Analysis (PCA)

↓

Customer Clustering

↓

Cluster Evaluation

↓

Interactive Dashboard

↓

Business Insights

---

## Project Features

* Interactive Streamlit Dashboard
* Customer CSV Upload
* Automated Customer Segmentation
* K-Means Clustering
* Agglomerative Clustering
* PCA-based 3D Visualization
* Elbow Method Analysis
* Silhouette Score Evaluation
* Cluster Analytics Dashboard
* REST API using FastAPI
* Dockerized Deployment
* Cloud Deployment Support

---

## Machine Learning Techniques

### Principal Component Analysis (PCA)

Used to reduce dimensionality while preserving maximum information from customer features.

### K-Means Clustering

Used to discover hidden customer segments based on purchasing behavior and demographics.

### Agglomerative Clustering

Implemented hierarchical clustering as an alternative segmentation technique.

### Elbow Method

Used to determine the optimal number of customer clusters.

### Silhouette Analysis

Used to evaluate clustering quality and separation between customer groups.

---

## Skills Demonstrated

* Data Cleaning
* Feature Engineering
* Exploratory Data Analysis
* Data Visualization
* Customer Analytics
* Customer Segmentation
* Unsupervised Machine Learning
* Cluster Analysis
* Dimensionality Reduction
* Business Intelligence
* API Development
* Dashboard Development
* Cloud Deployment
* Docker Containerization

---

## Technologies

### Programming

* Python

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-Learn
* PCA
* K-Means
* Agglomerative Clustering
* Kneed

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit
* Plotly

### Deployment

* Docker
* Docker Compose
* Render
* Streamlit Community Cloud

### Version Control

* Git
* GitHub

---

## REST API Endpoints

### GET /

Returns API health status.

### POST /segment

Performs customer segmentation using uploaded customer data.

### POST /optimal-k

Finds the optimal number of clusters using Elbow Method and Silhouette Analysis.

---

## Project Structure

```
SmartCart/

├── app/
│   ├── main.py
│   └── streamlit_app.py
│
├── data/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── SmartCart_ecomm.ipynb
```

---

## Deployment

### Local Deployment

```
docker compose up --build
```

### Cloud Deployment

* FastAPI deployed on Render
* Streamlit Dashboard deployed on Streamlit Community Cloud

---

## Key Outcomes

* Segmented customers into meaningful behavioral groups
* Identified different spending patterns
* Improved customer targeting strategy
* Enabled personalized marketing recommendations
* Generated business-ready customer insights
* Built an interactive analytics dashboard
* Developed production-ready REST APIs
* Successfully deployed the application on cloud platforms

---

## Future Improvements

* RFM Customer Segmentation
* DBSCAN Clustering
* Gaussian Mixture Models
* Customer Lifetime Value Prediction
* Marketing Recommendation Engine
* Model Monitoring
* Authentication & User Management
* Database Integration
* Automated Model Retraining

---

## Author

**Shivang Kathait**

Machine Learning | Data Science | Artificial Intelligence
