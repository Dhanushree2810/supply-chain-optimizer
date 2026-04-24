# 🚚 Smart Supply Chain Optimizer

A web application that predicts shipment delay risks using traffic and weather data, built for the Google Solution Challenge 2026.

## 🌍 UN SDG Alignment
**SDG 9 — Industry, Innovation and Infrastructure**
Helps logistics companies reduce delays and improve supply chain efficiency.

## 🔗 Live Demo
https://supply-chain-optimizer-pamh.onrender.com

## 🚀 Features
- Upload shipment CSV data
- Predicts delay risk (Low / Medium / High) based on traffic and weather
- Interactive dashboard with risk distribution chart
- Filter and view shipment details
- Download scored results as CSV

## 🛠️ Tech Stack
- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly

## 📋 How to Use
1. Open the live demo link
2. Upload a CSV file with columns: `shipment_id`, `origin`, `destination`, `traffic_level`, `weather`
3. View the risk predictions on the dashboard
4. Download the results

## 📊 Sample CSV Format
| shipment_id | origin | destination | traffic_level | weather |
|-------------|--------|-------------|---------------|---------|
| S001 | Chennai | Mumbai | High | Rainy |
| S002 | Delhi | Bangalore | Low | Clear |

## 💡 Problem It Solves
Supply chain delays cost businesses billions every year. This tool helps logistics managers identify high-risk shipments early so they can take preventive action.

## 👩‍💻 Developer
Dhanushree2810
