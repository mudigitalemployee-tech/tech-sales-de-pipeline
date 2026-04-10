import pandas as pd
import sys


def _to_float(x):
    try:
        return float(x)
    except Exception:
        return None


def check_numeric_range(series, min_val, max_val):
    """Check if numeric values are within range. Non-numeric = FAIL."""
    results = []
    for x in series:
        f = _to_float(x)
        if f is None:
            results.append(False)
        else:
            results.append(min_val <= f <= max_val)
    return results


def run_dq_checks(df):
    results = []

    # Completeness
    null_pct = df.isnull().mean().mean() * 100
    results.append({
        'check': 'Completeness',
        'score': round(100 - null_pct, 1),
        'status': 'PASS' if null_pct < 20 else 'WARN'
    })

    # Rating validity (0-5)
    if 'rating' in df.columns:
        valid = check_numeric_range(df['rating'], 0, 5)
        score = sum(valid) / len(valid) * 100
        results.append({
            'check': 'Rating validity (0-5)',
            'score': round(score, 1),
            'status': 'PASS' if score >= 80 else 'WARN'
        })

    # Quantity positivity
    if 'quantity' in df.columns:
        valid = [(_to_float(x) or 0) > 0 for x in df['quantity']]
        score = sum(valid) / len(valid) * 100
        results.append({
            'check': 'Quantity > 0',
            'score': round(score, 1),
            'status': 'PASS' if score >= 80 else 'WARN'
        })

    for r in results:
        print(f"  {r['check']}: {r['score']}% [{r['status']}]")

    return results


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/transformed_data.csv'
    df = pd.read_csv(path)
    print(f"Rows: {len(df)} | Columns: {len(df.columns)}")
    run_dq_checks(df)
    print("DQ checks complete.")
