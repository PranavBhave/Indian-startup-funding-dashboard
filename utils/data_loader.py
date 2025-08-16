import pandas as pd
import numpy as np
import re

def parse_amount(x):
    """
    Convert funding amounts like '152.38 Cr', '1,234.5 Cr', 'Undisclosed' → float
    Returns np.nan for invalid entries.
    """
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    if s.lower() in ['undisclosed', '—', '-', 'na', 'n/a', 'nan', '']:
        return np.nan
    s = re.sub(r'[^\d\.\-eE]', '', s)  # Keep digits, dot, minus, exponent
    try:
        return float(s)
    except ValueError:
        return np.nan

def standardize_city(city):
    """Standardize common city names."""
    if pd.isna(city):
        return city
    c = str(city).strip().title()
    mapping = {
        "Bangalore": "Bengaluru",
        "Bombay": "Mumbai",
        "New Delhi": "Delhi",
        "Ncr": "Delhi",
    }
    return mapping.get(c, c)

def load_and_prepare_data(path):
    """Load CSV, clean columns, parse dates, and standardize fields."""
    df = pd.read_csv(path)
    df = df.copy()

    # Normalize column names → lowercase, snake_case
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Convert date
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

    # Clean text columns
    text_cols = ['startup_name', 'industry_vertical', 'sub_vertical',
                 'city_location', 'investors_name', 'investment_type']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({'nan': None})

    # Convert funding amount to numeric
    if 'amount_cr' in df.columns:
        df['amount_cr'] = df['amount_cr'].apply(parse_amount)

    # Standardize city names
    if 'city_location' in df.columns:
        df['city_location'] = df['city_location'].apply(standardize_city)

    # Add year & month columns
    if 'date' in df.columns:
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.to_period('M').astype(str)

    return df
