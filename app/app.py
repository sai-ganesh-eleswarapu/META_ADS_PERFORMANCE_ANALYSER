import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import sys
import os

st.set_page_config(
    page_title="Meta Ads Performance Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from metrics import calculate_metrics
from insights import generate_insight
from model_compare import compare_models

model = joblib.load("models/ads_model.pkl")

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color: #060b1a;
    color: white;
}

[data-testid="stSidebar"]{
    background-color: #0d1326;
    border-right: 1px solid #1f2937;
}

[data-testid="stHeader"]{
    background: transparent;
}

.block-container{
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.main-title{
    font-size:42px;
    font-weight:700;
    color:white;
    margin-bottom:0px;
}

.sub-title{
    color:#9ca3af;
    margin-top:-10px;
    margin-bottom:25px;
}

.metric-card{
    background: linear-gradient(145deg,#101827,#0f172a);
    padding:20px;
    border-radius:18px;
    border:1px solid #1f2937;
    box-shadow: 0 0 20px rgba(0,0,0,0.35);
}

.metric-label{
    color:#9ca3af;
    font-size:15px;
    margin-bottom:10px;
}

.metric-value{
    color:white;
    font-size:34px;
    font-weight:700;
}

.section-card{
    background: linear-gradient(145deg,#101827,#0b1220);
    padding:20px;
    border-radius:20px;
    border:1px solid #1f2937;
    margin-top:15px;
}

.insight-good{
    background: rgba(34,197,94,0.15);
    border-left:5px solid #22c55e;
    padding:16px;
    border-radius:12px;
    margin-bottom:12px;
}

.insight-warning{
    background: rgba(251,191,36,0.15);
    border-left:5px solid #fbbf24;
    padding:16px;
    border-radius:12px;
    margin-bottom:12px;
}

.insight-danger{
    background: rgba(239,68,68,0.15);
    border-left:5px solid #ef4444;
    padding:16px;
    border-radius:12px;
    margin-bottom:12px;
}

.insight-info{
    background: rgba(59,130,246,0.15);
    border-left:5px solid #3b82f6;
    padding:16px;
    border-radius:12px;
    margin-bottom:12px;
}

.table-card{
    background: linear-gradient(145deg,#101827,#0b1220);
    padding:20px;
    border-radius:20px;
    border:1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 🔥 Meta Ads")
st.sidebar.markdown("### Performance Analyzer")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Analyze Single Ad",
        "Bulk Analysis",
        "Model Comparison"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Quick Summary")
st.sidebar.info("""
✔ Random Forest ML Model  
✔ KPI Tracking  
✔ CSV Bulk Analysis  
✔ Interactive Charts  
✔ Insight Generation  
""")

# ---------------- HEADER ----------------

st.markdown('<div class="main-title">🔥 Meta Ads Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Analyze and diagnose advertisement performance using Machine Learning</div>',
    unsafe_allow_html=True
)

# ---------------- SINGLE AD ----------------

if menu == "Analyze Single Ad":

    st.markdown("## 📌 Analyze Single Ad")

    c1, c2 = st.columns(2)

    with c1:
        impressions = st.number_input("Impressions", 0, value=15000)
        clicks = st.number_input("Clicks", 0, value=450)

    with c2:
        spend = st.number_input("Ad Spend (₹)", 0.0, value=27000.0)
        conversions = st.number_input("Conversions", 0, value=18)

    if st.button("🚀 Analyze Advertisement"):

        new_data = pd.DataFrame([{
            "impressions": impressions,
            "clicks": clicks,
            "spend": spend,
            "conversions": conversions
        }])

        prediction = model.predict(new_data)[0]

        ctr, cpc, cvr = calculate_metrics(
            impressions,
            clicks,
            spend,
            conversions
        )

        input_dict = new_data.iloc[0].to_dict()
        insight = generate_insight(input_dict, prediction)

        st.markdown("## 📊 Analysis Result")

        if prediction == "good":
            st.success(f"✅ Prediction: {prediction}")

        elif prediction == "creative_issue":
            st.warning(f"🎨 Prediction: {prediction}")

        elif prediction == "audience_issue":
            st.info(f"🎯 Prediction: {prediction}")

        else:
            st.error(f"🚨 Prediction: {prediction}")

        st.info(insight)

        st.markdown("## 📈 Performance Metrics")

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CTR (%)</div>
                <div class="metric-value">{ctr:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CPC (₹)</div>
                <div class="metric-value">{cpc:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Conversion Rate (%)</div>
                <div class="metric-value">{cvr:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

# ---------------- BULK ANALYSIS ----------------

elif menu == "Bulk Analysis":

    st.markdown("## 📂 Upload CSV Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        required_cols = [
            "impressions",
            "clicks",
            "spend",
            "conversions"
        ]

        if all(col in df.columns for col in required_cols):

            X = df[required_cols]

            predictions = model.predict(X)

            df["prediction"] = predictions

            total_impressions = int(df["impressions"].sum())
            total_clicks = int(df["clicks"].sum())
            total_spend = float(df["spend"].sum())
            total_conversions = int(df["conversions"].sum())

            ctr = (total_clicks / total_impressions) * 100
            cpc = total_spend / total_clicks
            cvr = (total_conversions / total_clicks) * 100

            # ---------------- KPI SECTION ----------------

            st.markdown("## 📊 Dashboard Overview")

            k1, k2, k3, k4 = st.columns(4)

            with k1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">👁 Impressions</div>
                    <div class="metric-value">{total_impressions:,}</div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🖱 Clicks</div>
                    <div class="metric-value">{total_clicks:,}</div>
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">💰 Ad Spend</div>
                    <div class="metric-value">₹ {total_spend:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)

            with k4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 Conversions</div>
                    <div class="metric-value">{total_conversions:,}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            k5, k6, k7 = st.columns(3)

            with k5:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📈 Avg CTR</div>
                    <div class="metric-value">{ctr:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

            with k6:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">💵 Avg CPC</div>
                    <div class="metric-value">₹ {cpc:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

            with k7:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">⚡ Conversion Rate</div>
                    <div class="metric-value">{cvr:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

            # ---------------- CHARTS ----------------

            st.markdown("## 📊 Visual Analytics")

            left, right = st.columns([1, 1])

            with left:

                st.markdown('<div class="section-card">', unsafe_allow_html=True)

                st.markdown("### 🎯 Performance Issue Distribution")

                issue_counts = df["prediction"].value_counts()

                fig1 = px.pie(
                    names=issue_counts.index,
                    values=issue_counts.values,
                    hole=0.55,
                    color=issue_counts.index,
                    color_discrete_map={
                        "good": "#22c55e",
                        "creative_issue": "#f59e0b",
                        "audience_issue": "#3b82f6",
                        "conversion_issue": "#ef4444"
                    }
                )

                fig1.update_layout(
                    paper_bgcolor="#101827",
                    plot_bgcolor="#101827",
                    font_color="white",
                    height=450
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

                st.markdown('</div>', unsafe_allow_html=True)

            with right:

                st.markdown('<div class="section-card">', unsafe_allow_html=True)

                st.markdown("### 📈 Clicks vs Conversions")

                fig2 = px.scatter(
                    df,
                    x="clicks",
                    y="conversions",
                    color="prediction",
                    size="spend",
                    hover_data=["impressions"],
                    color_discrete_map={
                        "good": "#22c55e",
                        "creative_issue": "#f59e0b",
                        "audience_issue": "#3b82f6",
                        "conversion_issue": "#ef4444"
                    }
                )

                fig2.update_layout(
                    paper_bgcolor="#101827",
                    plot_bgcolor="#101827",
                    font_color="white",
                    height=450
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

                st.markdown('</div>', unsafe_allow_html=True)

            # ---------------- TABLE + INSIGHTS ----------------

            table_col, insight_col = st.columns([2, 1])

            with table_col:

                st.markdown('<div class="table-card">', unsafe_allow_html=True)

                st.markdown("## 🏆 Top Performing Ads")

                df["CTR"] = (
                    df["clicks"] / df["impressions"]
                ) * 100

                df["CPC"] = (
                    df["spend"] / df["clicks"]
                )

                df["Conversion Rate"] = (
                    df["conversions"] / df["clicks"]
                ) * 100

                display_df = df[
                    [
                        "impressions",
                        "clicks",
                        "spend",
                        "CTR",
                        "CPC",
                        "Conversion Rate",
                        "prediction"
                    ]
                ]

                st.dataframe(
                    display_df,
                    use_container_width=True
                )

                st.markdown('</div>', unsafe_allow_html=True)

            with insight_col:

                st.markdown("## 💡 Key Insights")

                conversion_issues = len(
                    df[df["prediction"] == "conversion_issue"]
                )

                creative_issues = len(
                    df[df["prediction"] == "creative_issue"]
                )

                audience_issues = len(
                    df[df["prediction"] == "audience_issue"]
                )

                good_ads = len(
                    df[df["prediction"] == "good"]
                )

                st.markdown(f"""
                <div class="insight-danger">
                🚨 <b>{conversion_issues} conversion issues detected</b><br>
                Landing pages may need optimization.
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="insight-warning">
                🎨 <b>{creative_issues} creative issues found</b><br>
                Try improving visuals and ad copy.
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="insight-info">
                🎯 <b>{audience_issues} audience issues detected</b><br>
                Audience targeting may need refinement.
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="insight-good">
                ✅ <b>{good_ads} campaigns performing well</b><br>
                These ads show healthy engagement.
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error(
                "CSV must contain impressions, clicks, spend and conversions columns."
            )

# ---------------- MODEL COMPARISON ----------------

elif menu == "Model Comparison":

    st.markdown("## 🤖 Machine Learning Model Comparison")

    results = compare_models("data/ads_data1.csv")

    model_names = list(results.keys())
    accuracies = list(results.values())

    fig = px.bar(
        x=model_names,
        y=accuracies,
        color=model_names,
        text=accuracies
    )

    fig.update_layout(
        paper_bgcolor="#101827",
        plot_bgcolor="#101827",
        font_color="white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    best_model = max(results, key=results.get)

    st.success(f"🏆 Best Performing Model: {best_model}")

    for model_name, acc in results.items():

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{model_name}</div>
            <div class="metric-value">{acc:.2f}</div>
        </div>
        <br>
        """, unsafe_allow_html=True)

# ---------------- DASHBOARD PAGE ----------------

else:

    st.markdown("""
    ## 🚀 Meta Ads Intelligence Dashboard

    This system analyzes advertisement performance using Machine Learning.

    ### Features
    - KPI Tracking
    - Bulk CSV Analysis
    - Interactive Charts
    - Prediction Engine
    - Model Comparison
    - Insight Generation

    ### Technologies Used
    - Python
    - Streamlit
    - Plotly
    - Scikit-learn
    - Pandas
    """)