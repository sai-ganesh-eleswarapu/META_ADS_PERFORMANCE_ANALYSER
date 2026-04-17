import matplotlib.pyplot as plt
import streamlit as st
import joblib
import pandas as pd
import sys
import os

st.set_page_config(page_title="Meta Ads Analyzer", layout="wide")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from metrics import calculate_metrics
from insights import generate_insight

model = joblib.load("models/ads_model.pkl")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🔥 Meta Ads Performance Analyzer")
st.caption("Analyze your ad performance and detect issues instantly 🚀")

st.divider()

# SINGLE AD SECTION
st.header("📌 Analyze Single Ad")

colA, colB = st.columns(2)

with colA:
    impressions = st.number_input("Impressions", min_value=0, value=10000)
    clicks = st.number_input("Clicks", min_value=0, value=300)

with colB:
    spend = st.number_input("Ad Spend (₹)", min_value=0.0, value=1500.0)
    conversions = st.number_input("Conversions", min_value=0, value=10)

if st.button("🚀 Analyze Ad"):

    new_data = pd.DataFrame([{
        "impressions": impressions,
        "clicks": clicks,
        "spend": spend,
        "conversions": conversions
    }])

    prediction = model.predict(new_data)[0]

    ctr, cpc, cvr = calculate_metrics(impressions, clicks, spend, conversions)

    input_dict = new_data.iloc[0].to_dict()
    insight = generate_insight(input_dict, prediction)

    st.subheader("📊 Results")

    # -------- COLORED OUTPUT --------
    if prediction == "good":
        st.success(f"✅ Prediction: {prediction}")
    elif prediction == "conversion_issue":
        st.warning(f"⚠️ Prediction: {prediction}")
    else:
        st.error(f"❌ Prediction: {prediction}")

    st.info(f"💡 {insight}")

    # -------- METRICS CARDS --------
    st.subheader("📈 Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("CTR (%)", f"{ctr:.2f}")
    col2.metric("CPC (₹)", f"{cpc:.2f}")
    col3.metric("Conversion Rate (%)", f"{cvr:.2f}")

st.divider()

# CSV SECTION
st.header("📂 Upload CSV for Bulk Analysis")

uploaded_file = st.file_uploader("Upload your ads CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    required_cols = ["impressions", "clicks", "spend", "conversions"]

    if all(col in df.columns for col in required_cols):

        X = df[required_cols]
        predictions = model.predict(X)

        df["prediction"] = predictions

        # -------- INSIGHTS --------
        def get_insight(label):
            if label == "creative_issue":
                return "Ad creative may not be engaging."
            elif label == "audience_issue":
                return "Target audience may not be correct."
            elif label == "conversion_issue":
                return "Users are clicking but not converting."
            else:
                return "Campaign performing well."

        df["insight"] = df["prediction"].apply(get_insight)

        st.subheader("✅ Results")
        st.dataframe(df, use_container_width=True)

        st.divider()

        st.subheader("📊 Dashboard Insights")

        col1, col2 = st.columns(2, gap="large")

        # -------- LEFT GRAPH --------
        with col1:
            st.markdown("### 🔥 Issue Distribution")

            prediction_counts = df["prediction"].value_counts()

            fig1, ax1 = plt.subplots(figsize=(7,5))

            prediction_counts = df["prediction"].value_counts().sort_values(ascending=False)

            prediction_counts.plot(kind="bar", ax=ax1, width=0.5)

            for i, v in enumerate(prediction_counts):
                ax1.text(i, v + 0.5, str(v), ha='center')

            ax1.set_xlabel("Issue Type")
            ax1.set_ylabel("Count")
            ax1.set_title("Ad Performance Issues Breakdown")

            # Rotate labels slightly for spacing
            plt.xticks(rotation=20, ha='right')

            # Add spacing around plot
            plt.tight_layout()

            st.pyplot(fig1)

        # -------- RIGHT GRAPH --------
        with col2:
            st.markdown("### 📈 Clicks vs Conversions")

            fig2, ax2 = plt.subplots(figsize=(7,4.65))
            ax2.scatter(df["clicks"], df["conversions"])

            ax2.set_xlabel("Clicks")
            ax2.set_ylabel("Conversions")
            ax2.set_title("Clicks vs Conversions")

            st.pyplot(fig2)

    else:
        st.error("CSV must contain: impressions, clicks, spend, conversions")