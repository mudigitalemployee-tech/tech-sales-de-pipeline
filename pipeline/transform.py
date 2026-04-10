import pandas as pd
import hashlib


def _to_float(x):
    try:
        return float(x)
    except Exception:
        return None


def transform(df):
    """Apply Silver layer transformations to tech_sales data."""
    df = df.copy()

    # Rule 1: Blank normalization
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].replace('', pd.NA)

    # Rule 5: Negative quantities -> abs
    if 'quantity' in df.columns:
        df['quantity_negative_flag'] = df['quantity'] < 0
        df['quantity'] = df['quantity'].abs()

    # Rule 7: Rating clamp 0-5
    if 'rating' in df.columns:
        df['rating_valid_flag'] = df['rating'].apply(
            lambda x: 0 <= (_to_float(x) or 0) <= 5
        )
        df['rating'] = df['rating'].clip(0, 5)

    # Rule 9: Text standardization
    for col in ['category', 'status', 'region']:
        if col in df.columns:
            df[col] = df[col].str.upper().str.strip()

    # Rule 11: PII masking
    for col in ['customer_name', 'customer_email', 'phone_number']:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: hashlib.sha256(
                    str(x).encode()
                ).hexdigest() if pd.notna(x) else x
            )

    return df
