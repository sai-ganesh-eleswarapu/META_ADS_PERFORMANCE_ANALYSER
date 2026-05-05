import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.set_page_config(page_title="Meta Ads Dashboard", layout="wide")

# CUSTOM STYLES
st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(145deg, #1f222b, #2a2e38);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.section-title {
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🔥 Meta Ads Performance Analyzer")
st.markdown("Analyze and diagnose your ad performance in real-time")

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Analyze Single Ad"])

model = joblib.load("models/ads_model.pkl")

# DASHBOARD

if page == "Dashboard":

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        required_cols = ["impressions", "clicks", "spend", "conversions"]

        if all(col in df.columns for col in required_cols):

            # Predictions & Insights
            X = df[required_cols]
            df["prediction"] = model.predict(X)

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

            # KPI Calculations
            total_impressions = df['impressions'].sum()
            total_clicks = df['clicks'].sum()
            total_spend = df['spend'].sum()
            total_conversions = df['conversions'].sum()

            ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
            cpc = total_spend / total_clicks if total_clicks > 0 else 0
            cvr = (total_conversions / total_clicks) * 100 if total_clicks > 0 else 0

            # KPI Cards
            st.markdown('<div class="section-title">📊 Dashboard Overview</div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Impressions", f"{total_impressions:,}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Clicks", f"{total_clicks:,}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Ad Spend", f"₹ {total_spend:,.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Conversions", f"{total_conversions:,}")
                st.markdown('</div>', unsafe_allow_html=True)

            col5, col6, col7 = st.columns(3)

            with col5:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Avg CTR", f"{ctr:.2f}%")
                st.markdown('</div>', unsafe_allow_html=True)

            with col6:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Avg CPC", f"₹ {cpc:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col7:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Conversion Rate", f"{cvr:.2f}%")
                st.markdown('</div>', unsafe_allow_html=True)

            # Visualisations and Insights
            colA, colB = st.columns(2)

            # DONUT
            with colA:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("🎯 Issue Distribution")

                fig = px.pie(
                    df,
                    names="prediction",
                    hole=0.6,
                    color="prediction",
                    color_discrete_map={
                        "good": "#00cc96",
                        "creative_issue": "#ffa600",
                        "audience_issue": "#636efa",
                        "conversion_issue": "#ef553b"
                    }
                )

                fig.update_traces(textinfo='percent+label')

                fig.update_layout(
                    paper_bgcolor="#1c1f26",
                    plot_bgcolor="#1c1f26",
                    font=dict(color="white"),
                    margin=dict(t=10, b=10)
                )

                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # SCATTER
            with colB:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("📈 Clicks vs Conversions")

                fig2 = px.scatter(
                    df,
                    x="clicks",
                    y="conversions",
                    color="prediction",
                    opacity=0.8,
                    color_discrete_map={
                        "good": "#00cc96",
                        "creative_issue": "#ffa600",
                        "audience_issue": "#636efa",
                        "conversion_issue": "#ef553b"
                    }
                )

                fig2.update_layout(
                    paper_bgcolor="#1c1f26",
                    plot_bgcolor="#1c1f26",
                    font=dict(color="white")
                )

                st.plotly_chart(fig2, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Data Table
            st.markdown('<div class="section-title">📋 Ad Performance Data</div>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)

            # Insights
            st.markdown('<div class="section-title">💡 Key Insights</div>', unsafe_allow_html=True)

            colX, colY = st.columns([2,1])

            with colY:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.error("🚨 Conversion issues detected")
                st.warning("🎨 Creative improvement needed")
                st.info("🎯 Audience refinement suggested")
                st.success("✅ Good campaigns performing well")
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error("CSV must contain: impressions, clicks, spend, conversions")

# Single AD Analysis

if page == "Analyze Single Ad":

    st.markdown('<div class="section-title">📌 Analyze Single Ad</div>', unsafe_allow_html=True)

    impressions = st.number_input("Impressions", min_value=0, value=10000)
    clicks = st.number_input("Clicks", min_value=0, value=300)
    spend = st.number_input("Ad Spend (₹)", min_value=0.0, value=1500.0)
    conversions = st.number_input("Conversions", min_value=0, value=10)

    if st.button("Analyze Ad 🚀"):

        new_data = pd.DataFrame([{
            "impressions": impressions,
            "clicks": clicks,
            "spend": spend,
            "conversions": conversions
        }])

        prediction = model.predict(new_data)[0]

        ctr = (clicks / impressions) * 100 if impressions > 0 else 0
        cpc = spend / clicks if clicks > 0 else 0
        cvr = (conversions / clicks) * 100 if clicks > 0 else 0

        st.markdown('<div class="section-title">📊 Results</div>', unsafe_allow_html=True)

        if prediction == "good":
            st.success(f"Prediction: {prediction}")
        else:
            st.error(f"Prediction: {prediction}")

        st.info("💡 " + prediction.replace("_", " ").title())

        st.markdown('<div class="section-title">📈 Metrics</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        col1.metric("CTR (%)", f"{ctr:.2f}")
        col2.metric("CPC (₹)", f"{cpc:.2f}")
        col3.metric("Conversion Rate (%)", f"{cvr:.2f}")