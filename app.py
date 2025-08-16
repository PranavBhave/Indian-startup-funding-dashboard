import streamlit as st
import pandas as pd
from utils.data_loader import load_and_prepare_data
from utils.charts import  pie_chart_overall_city_rounds,pie_chart_overall_city_amount,plot_funding_trend, plot_top_categories, plot_top_cities, plot_top_investors,plot_investor_funding_trend,plot_investor_sector_distribution


# Page Config & Styling

st.set_page_config(layout="wide", page_title="Startup Funding Analysis")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { background-color: #dad7cd; }
    div[data-testid="metric-container"] > div { color: white; }
    </style>
    """,
    unsafe_allow_html=True
)


# Load Data

@st.cache_data
def get_data():
    return load_and_prepare_data("data/indian_startup_funding_cleaned.csv")

df = get_data()


# Sidebar Menu

st.sidebar.title("Startup Funding Dashboard")
menu_option = st.sidebar.selectbox(
    "Select Analysis Type",
    ["Company POV", "Investor POV", "General Analysis"]
)


# COMPANY POV
# =========================
if menu_option == "Company POV":
    st.subheader("📊 Company Point of View")

    # Clean the startup name column
    df["startup_name_clean"] = (
        df["startup_name"].astype(str).str.lower()
        .str.strip()
        .str.replace(r'[\'"]+', '', regex=True)
        .str.replace(r'\s+', ' ', regex=True)
        .str.replace(r'[^\w\s]', '', regex=True)
    )

    # Create sorted list of startup names
    startup_list = sorted(df["startup_name_clean"].dropna().unique())

    # Let user select a startup from sidebar
    selected_startup = st.sidebar.selectbox("Select a Startup", startup_list)

    # Filter DataFrame for selected startup
    startup_df = df[df["startup_name_clean"] == selected_startup].copy()

    
    # Show the selected startup in the main app
    st.subheader(f"{selected_startup}")

    if not startup_df.empty:
        # Basic Metrics
        total_funding = startup_df["amount_cr"].sum()
        funding_rounds = startup_df.shape[0]

        col1, col2 = st.columns(2)
        col1.metric("Total Funding (Cr)", f"{total_funding:,.2f}")
        col2.metric("Number of Funding Rounds", funding_rounds)

        # Information about Table
        st.subheader("📄 Startup Details")
        details_columns = [
            col for col in ["startup_name", "city_location", "industry_vertical", "sub_vertical", "investors_name", "date"]
            if col in startup_df.columns
        ]
        if details_columns:
            st.dataframe(startup_df[details_columns].reset_index(drop=True))
        else:
            st.info("No extra details available for this startup.")

        # Charts
        st.subheader("📈 Funding Trend")
        st.plotly_chart(plot_funding_trend(startup_df), use_container_width=True)

    else:
        st.warning("No data available for this startup.")




# INVESTOR POV

elif menu_option == "Investor POV":
    st.subheader("💼 Investor POV")

    # Clean investor name
    df["investor_clean"] = (
        df["investors_name"].astype(str)
        .str.lower()
        .str.strip()
        .str.replace(r'[\'"]+', '', regex=True)
    )

    investor_list = sorted(df["investor_clean"].dropna().unique())
    selected_investor = st.sidebar.selectbox("Select an Investor", investor_list)

    investor_df = df[df["investor_clean"] == selected_investor].copy()

    if not investor_df.empty:
        # Metrics
        total_investment = investor_df["amount_cr"].sum()
        total_startups = investor_df["startup_name"].nunique()
        total_rounds = investor_df.shape[0]
        avg_investment = total_investment / total_rounds if total_rounds > 0 else 0
        last_investment = investor_df["date"].max()

        # Format the date as DD MMM YYYY
        formatted_date = pd.to_datetime(last_investment).strftime("%d %b %Y")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Invested (Cr)", f"{total_investment:,.2f}")
        col2.metric("Startups Funded", total_startups)
        col3.metric("Funding Rounds", total_rounds)
        col4.metric("Avg per Round", f"{avg_investment:,.2f}")

        # Custom HTML for Last Investment (smaller font, no truncation)
        col5.markdown(
            f"""
            <div style="font-size:14px; line-height:1.1-1.2;">
              <div style="color:var(--text-color); font-weight:400; margin-bottom:2px;">Last Investment</div>
              <div style="font-size:16px; color:var(--text-color);">{formatted_date}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Top startups table
        st.subheader("🚀 Top Startups Funded")
        top_startups_df = (
            investor_df.groupby("startup_name")["amount_cr"]
            .sum()
            .reset_index()
            .sort_values(by="amount_cr", ascending=False)
            .head(10)
        )
        st.dataframe(top_startups_df)

        # Charts
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.plotly_chart(plot_investor_funding_trend(investor_df), use_container_width=True)
        with chart_col2:
            st.plotly_chart(plot_investor_sector_distribution(investor_df), use_container_width=True)

    else:
        st.warning("No data available for this investor.")




# GENERAL ANALYSIS

else:
    
    st.subheader("📊 General Analysis")
    st.plotly_chart(plot_funding_trend(df), use_container_width=True)
    st.plotly_chart(plot_top_categories(df), use_container_width=True)
    st.plotly_chart(plot_top_cities(df), use_container_width=True)
    st.plotly_chart(plot_top_investors(df), use_container_width=True)
    col1, col2 = st.columns(2)

    with col1:
        fig_rounds = pie_chart_overall_city_rounds(df)
        st.pyplot(fig_rounds)

    with col2:
        fig_amount = pie_chart_overall_city_amount(df)
        st.pyplot(fig_amount)