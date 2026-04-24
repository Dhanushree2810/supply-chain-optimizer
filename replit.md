# Smart Supply Chain Optimizer

## Overview

A Streamlit web app that lets users upload shipment data (CSV), analyzes traffic and weather conditions, predicts delay risk (Low / Medium / High), and visualizes results in a dashboard with a risk-distribution bar chart.

## Stack

- **Language**: Python 3.11
- **Framework**: Streamlit
- **Data**: pandas
- **Charts**: Plotly Express

## Run

- Workflow `Start application` runs: `streamlit run app.py --server.port 5000`
- Streamlit config in `.streamlit/config.toml` (port 5000, headless, CORS off)

## CSV Format

Required columns: `traffic_level`, `weather`. Recommended: `shipment_id`, `origin`, `destination`.

Risk is derived from a simple rule-based score over normalized traffic and weather values.
