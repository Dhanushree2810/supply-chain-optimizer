import io

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Smart Supply Chain Optimizer",
    page_icon=":truck:",
    layout="wide",
)

RISK_ORDER = ["Low", "Medium", "High"]
RISK_COLORS = {"Low": "#2ecc71", "Medium": "#f1c40f", "High": "#e74c3c"}

TRAFFIC_SCORES = {"low": 0, "light": 0, "medium": 1, "moderate": 1, "heavy": 2, "high": 2, "severe": 3}
WEATHER_SCORES = {
    "clear": 0,
    "sunny": 0,
    "cloudy": 1,
    "overcast": 1,
    "rain": 2,
    "rainy": 2,
    "snow": 3,
    "snowy": 3,
    "storm": 3,
    "stormy": 3,
    "fog": 2,
    "foggy": 2,
}


def normalize(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def score_traffic(value):
    return TRAFFIC_SCORES.get(normalize(value), 1)


def score_weather(value):
    return WEATHER_SCORES.get(normalize(value), 1)


def predict_risk(row):
    score = score_traffic(row.get("traffic_level")) + score_weather(row.get("weather"))
    if score <= 1:
        return "Low"
    if score <= 3:
        return "Medium"
    return "High"


def build_sample_csv() -> bytes:
    sample = pd.DataFrame(
        [
            {"shipment_id": "SHP-1001", "origin": "Seattle", "destination": "Portland", "traffic_level": "Low", "weather": "Clear"},
            {"shipment_id": "SHP-1002", "origin": "Chicago", "destination": "Detroit", "traffic_level": "Heavy", "weather": "Snow"},
            {"shipment_id": "SHP-1003", "origin": "Dallas", "destination": "Houston", "traffic_level": "Medium", "weather": "Rain"},
            {"shipment_id": "SHP-1004", "origin": "NYC", "destination": "Boston", "traffic_level": "Heavy", "weather": "Storm"},
            {"shipment_id": "SHP-1005", "origin": "LA", "destination": "San Diego", "traffic_level": "Low", "weather": "Sunny"},
            {"shipment_id": "SHP-1006", "origin": "Denver", "destination": "Salt Lake City", "traffic_level": "Medium", "weather": "Cloudy"},
            {"shipment_id": "SHP-1007", "origin": "Atlanta", "destination": "Miami", "traffic_level": "High", "weather": "Rain"},
            {"shipment_id": "SHP-1008", "origin": "Phoenix", "destination": "Las Vegas", "traffic_level": "Low", "weather": "Clear"},
        ]
    )
    return sample.to_csv(index=False).encode("utf-8")


def main():
    st.title("Smart Supply Chain Optimizer")
    st.caption("Upload shipment data to analyze traffic, weather, and predict delay risk.")

    with st.sidebar:
        st.header("Upload Shipment Data")
        st.write("Provide a CSV with the following columns:")
        st.code("shipment_id, origin, destination, traffic_level, weather", language="text")
        uploaded = st.file_uploader("CSV file", type=["csv"])
        st.download_button(
            label="Download sample CSV",
            data=build_sample_csv(),
            file_name="sample_shipments.csv",
            mime="text/csv",
        )

    if uploaded is None:
        st.info("Upload a CSV file from the sidebar to begin. You can download a sample to try it out.")
        return

    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")
        return

    required = {"traffic_level", "weather"}
    missing = required.difference(df.columns)
    if missing:
        st.error(f"Missing required columns: {', '.join(sorted(missing))}")
        return

    df["delay_risk"] = df.apply(predict_risk, axis=1)
    df["delay_risk"] = pd.Categorical(df["delay_risk"], categories=RISK_ORDER, ordered=True)

    total = len(df)
    counts = df["delay_risk"].value_counts().reindex(RISK_ORDER, fill_value=0)

    st.subheader("Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Shipments", total)
    c2.metric("Low Risk", int(counts["Low"]))
    c3.metric("Medium Risk", int(counts["Medium"]))
    c4.metric("High Risk", int(counts["High"]))

    st.subheader("Risk Distribution")
    chart_df = counts.reset_index()
    chart_df.columns = ["Delay Risk", "Shipments"]
    fig = px.bar(
        chart_df,
        x="Delay Risk",
        y="Shipments",
        color="Delay Risk",
        color_discrete_map=RISK_COLORS,
        text="Shipments",
    )
    fig.update_layout(showlegend=False, height=400, margin=dict(l=20, r=20, t=20, b=20))
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Shipment Details")
    risk_filter = st.multiselect(
        "Filter by risk level",
        options=RISK_ORDER,
        default=RISK_ORDER,
    )
    filtered = df[df["delay_risk"].isin(risk_filter)] if risk_filter else df
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    output = io.StringIO()
    filtered.to_csv(output, index=False)
    st.download_button(
        label="Download results as CSV",
        data=output.getvalue(),
        file_name="shipment_risk_results.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
