import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import re


def plot_funding_trend(df):
    """Line chart for total funding by year."""
    g = df.dropna(subset=['amount_cr']).groupby('year')['amount_cr'].sum().reset_index()
    fig = px.line(
        g,
        x='year',
        y='amount_cr',
        markers=True,
        title="Total Funding by Year (₹ Cr)"
    )
    fig.update_layout(yaxis_title="Amount (₹ Cr)", xaxis_title="Year")
    return fig


def plot_top_categories(df, top_n=10):
    """Top sectors by total funding."""
    g = df.dropna(subset=['amount_cr']).groupby('industry_vertical')['amount_cr'].sum()
    g = g.sort_values(ascending=False).head(top_n).reset_index()
    fig = px.bar(g, x='amount_cr', y='industry_vertical', orientation='h',
                 title=f"Top Sectors by Funding (₹ Cr)")
    fig.update_layout(xaxis_title="Amount (₹ Cr)", yaxis_title="")
    return fig

def plot_top_cities(df, top_n=10):
    """Top cities by funding."""
    g = df.dropna(subset=['amount_cr']).groupby('city_location')['amount_cr'].sum()
    g = g.sort_values(ascending=False).head(top_n).reset_index()
    fig = px.bar(g, x='amount_cr', y='city_location', orientation='h',
                 title=f"Top {top_n} Cities by Funding (₹ Cr)")
    fig.update_layout(xaxis_title="Amount (₹ Cr)", yaxis_title="")
    return fig

def plot_top_investors(df, top_n=15):
    """Top investors by total funding."""
    df2 = df[['investors_name', 'amount_cr']].dropna(subset=['investors_name']).copy()
    
    rows = []
    for _, r in df2.iterrows():
        invs = [i.strip() for i in re.split(r',|;| and | & |/|\|', r['investors_name'])]
        amt = r['amount_cr'] if pd.notna(r['amount_cr']) else 0
        for inv in invs:
            if inv:
                rows.append({'Investor': inv, 'amount_cr': amt})
    
    if not rows:
        return px.bar(title="No investor data available")
    
    df_inv = pd.DataFrame(rows)
    g = df_inv.groupby('Investor')['amount_cr'].sum().sort_values(ascending=False).head(top_n).reset_index()
    fig = px.bar(g, x='amount_cr', y='Investor', orientation='h',
                 title=f"Top {top_n} Investors by Funding (₹ Cr)")
    fig.update_layout(xaxis_title="Amount (₹ Cr)", yaxis_title="")
    return fig

def pie_chart_overall_city_rounds(df):
    """Pie chart showing % of funding rounds by city."""
    city_counts = df["city_location"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        city_counts,
        labels=city_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Top Cities by Funding Rounds", fontsize=14)
    plt.tight_layout()
    return fig

def pie_chart_overall_city_amount(df):
    """Pie chart showing % of funding amount by city."""
    city_amounts = df.groupby("city_location")["amount_cr"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        city_amounts,
        labels=city_amounts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Top Cities by Funding Amount", fontsize=14)
    plt.tight_layout()
    return fig

import plotly.express as px
import pandas as pd

# ---------- Investor Funding Trend ----------
def plot_investor_funding_trend(df):
    if "date" in df.columns and not df.empty:
        df["year"] = pd.to_datetime(df["date"], errors="coerce").dt.year
        trend_df = df.groupby("year")["amount_cr"].sum().reset_index()
        if not trend_df.empty:
            fig = px.line(trend_df, x="year", y="amount_cr",
                          title="Funding Trend Over Time",
                          markers=True)
            fig.update_layout(yaxis_title="Funding Amount (Cr)", xaxis_title="Year")
            return fig

    # Empty figure fallback
    return px.scatter(title="No Data Available for Funding Trend")

# ---------- Investor Sector Distribution ----------
def plot_investor_sector_distribution(df):
    if "industry_vertical" in df.columns and not df.empty:
        sector_df = df["industry_vertical"].value_counts().reset_index()
        sector_df.columns = ["industry_vertical", "count"]
        if not sector_df.empty:
            fig = px.bar(sector_df, x="industry_vertical", y="count",
                         title="Sector Distribution of Investments")
            fig.update_layout(xaxis_title="Sector", yaxis_title="Number of Investments")
            return fig

    return px.scatter(title="No Data Available for Sector Distribution")


