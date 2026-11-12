
import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from backend.frequency_analysis import (
    calculate_keyword_frequency,
    calculate_query_frequency
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SearchLens | Analytics",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- ADVANCED CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080D1A;
    color: #F1F5F9;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding: 2rem 3rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10182B, #0B1220);
    border-right: 1px solid #24314A;
}

section[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

.brand {
    font-size: 27px;
    font-weight: 800;
    color: #A78BFA;
    letter-spacing: -1px;
    padding: 10px 0 5px 0;
}

.subtitle {
    color: #94A3B8;
    font-size: 13px;
    margin-bottom: 28px;
}

.main-title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #F8FAFC;
}

.description {
    color: #94A3B8;
    font-size: 14px;
    margin-bottom: 25px;
}

.metric-card {
    background: linear-gradient(135deg, #17233D, #111B30);
    border: 1px solid #293B5C;
    border-radius: 16px;
    padding: 22px;
    min-height: 125px;
    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: #8B5CF6;
    box-shadow: 0 10px 30px #00000040;
}

.metric-label {
    color: #A5B4CC;
    font-size: 13px;
}

.metric-value {
    color: #F8FAFC;
    font-size: 30px;
    font-weight: 800;
    margin-top: 12px;
}

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #F8FAFC;
    margin: 20px 0 12px 0;
}

div[data-testid="stFileUploader"] {
    background: #111B30;
    border: 1px dashed #7C6BE8;
    border-radius: 15px;
    padding: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #7C3AED, #4F46E5);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    box-shadow: 0 5px 20px #7C3AED60;
    border: none;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #293B5C;
    border-radius: 12px;
}

.stCaption {
    color: #94A3B8;
}

</style>
""", unsafe_allow_html=True)


# ---------------- DATA LOADING ----------------

DATA_PATH = ROOT / "dataset" / "search_queries.csv"

@st.cache_data
def load_sample_data():
    return pd.read_csv(DATA_PATH)

if "data" not in st.session_state:
    st.session_state.data = load_sample_data()

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown(
        '<div class="brand">⌕ SearchLens</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">BIG DATA ANALYTICS PLATFORM</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Keyword Analysis",
            "Query Analysis",
            "Dataset Management"
        ]
    )

    st.markdown("---")
    st.caption("SearchLens Analytics")
    st.caption("Powered by Python & PySpark")


# ---------------- GET DATA ----------------

df = st.session_state.data.copy()

required_columns = {"search_query", "search_date"}

if not required_columns.issubset(df.columns):
    st.error("Dataset must contain search_query and search_date columns.")
    st.stop()

df["search_query"] = df["search_query"].fillna("").astype(str)
df = df[df["search_query"].str.strip() != ""]

keywords = calculate_keyword_frequency(df)
keyword_df = pd.DataFrame(keywords)

query_df = calculate_query_frequency(df)

total_searches = len(df)
unique_queries = df["search_query"].str.lower().nunique()
total_keywords = int(keyword_df["Frequency"].sum()) if not keyword_df.empty else 0
unique_keywords = len(keyword_df)

if not keyword_df.empty:
    top_keyword = keyword_df.iloc[0]["Keyword"]
    top_frequency = int(keyword_df.iloc[0]["Frequency"])
else:
    top_keyword = "N/A"
    top_frequency = 0


# ---------------- OVERVIEW ----------------

if page == "Overview":

    st.markdown(
        '<div class="main-title">Analytics Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">Monitor search activity and discover popular keywords from your dataset.</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "TOTAL SEARCHES", total_searches),
        (c2, "UNIQUE QUERIES", unique_queries),
        (c3, "TOTAL KEYWORDS", total_keywords),
        (c4, "UNIQUE KEYWORDS", unique_keywords)
    ]

    for col, label, value in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value:,}</div>
            </div>
            """, unsafe_allow_html=True)

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown(
            '<div class="section-title">Top 10 Search Keywords</div>',
            unsafe_allow_html=True
        )

        if not keyword_df.empty:
            chart_data = keyword_df.head(10).sort_values("Frequency")

            fig = px.bar(
                chart_data,
                x="Frequency",
                y="Keyword",
                orientation="h",
                color="Frequency",
                color_continuous_scale=["#4F46E5", "#A78BFA"],
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=20, b=10),
                height=380
            )

            st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown(
            '<div class="section-title">Top Keyword</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">MOST FREQUENT KEYWORD</div>
            <div class="metric-value">{top_keyword}</div>
            <p style="color:#A78BFA;">
                Appeared {top_frequency} times
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">Recent Search Queries</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df.tail(5).iloc[::-1],
            use_container_width=True,
            hide_index=True
        )


# ---------------- KEYWORD ANALYSIS ----------------

elif page == "Keyword Analysis":

    st.markdown(
        '<div class="main-title">Keyword Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">Explore individual keyword frequency and ranking.</div>',
        unsafe_allow_html=True
    )

    if not keyword_df.empty:

        limit = st.selectbox(
            "Select keyword ranking",
            [10, 20, 50, 100]
        )

        st.dataframe(
            keyword_df.head(limit),
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            keyword_df.head(limit),
            x="Keyword",
            y="Frequency",
            color="Frequency",
            color_continuous_scale="Purples",
            template="plotly_dark"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            "Download Keyword Results",
            keyword_df.to_csv(index=False),
            "keyword_frequency.csv",
            "text/csv"
        )


# ---------------- QUERY ANALYSIS ----------------

elif page == "Query Analysis":

    st.markdown(
        '<div class="main-title">Search Query Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">Analyze complete search phrases and their frequency.</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        query_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Query Results",
        query_df.to_csv(index=False),
        "query_frequency.csv",
        "text/csv"
    )


# ---------------- DATASET MANAGEMENT ----------------

elif page == "Dataset Management":

    st.markdown(
        '<div class="main-title">Dataset Management</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">Upload your own search query dataset.</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            uploaded_df = pd.read_csv(uploaded_file)

            if not required_columns.issubset(uploaded_df.columns):
                st.error(
                    "CSV must contain search_query and search_date columns."
                )
            else:
                if st.button("Process Uploaded Dataset"):

                    st.session_state.data = uploaded_df
                    st.success("Dataset uploaded successfully!")

                    st.rerun()

        except Exception as error:
            st.error(f"Unable to read dataset: {error}")

    st.markdown('<div class="section-title">Current Dataset</div>',
                unsafe_allow_html=True)

    st.write(f"Total records: {len(df)}")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
