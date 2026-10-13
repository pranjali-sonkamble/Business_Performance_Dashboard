"""Audit UCI Online Retail data before using it in the Power BI dashboard.

Usage:
    python analysis/audit_online_retail.py path/to/Online_Retail.xlsx
    python analysis/audit_online_retail.py path/to/Online_Retail.xlsx --output-dir outputs

The script does not modify the input file. It prints cancellation coverage, the
PAPER CRAFT, LITTLE BIRDIE order-line details, and product rankings with/without
non-merchandise descriptions. Outputs are optional CSVs in the chosen folder.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

NON_MERCHANDISE = {
    "DOTCOM POSTAGE", "MANUAL", "POSTAGE", "BANK CHARGES",
    "CARRIAGE", "DISCOUNT", "AMAZON FEE", "CRUK COMMISSION",
    "POSTAGE CHARGES", "SAMPLES",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path, help="UCI Online Retail .xlsx or .csv")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    if args.input_file.suffix.lower() == ".csv":
        df = pd.read_csv(args.input_file, low_memory=False)
    else:
        df = pd.read_excel(args.input_file)

    required = {"InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing expected UCI columns: {', '.join(sorted(missing))}")

    df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
    df["Description"] = df["Description"].astype("string").str.strip()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["LineSales"] = df["Quantity"] * df["UnitPrice"]
    df["IsCancellationInvoice"] = df["InvoiceNo"].str.upper().str.startswith("C", na=False)
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype("string")

    cancellation_rows = df["IsCancellationInvoice"]
    positive_sales = df["Quantity"].gt(0) & df["UnitPrice"].ge(0)
    excluded_desc = df["Description"].str.upper().isin(NON_MERCHANDISE)
    birdie = df["Description"].str.upper().eq("PAPER CRAFT, LITTLE BIRDIE")

    print("=== Dataset audit ===")
    print(f"Rows: {len(df):,}")
    print(f"Invoice date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
    print(f"Rows with cancellation invoice (InvoiceNo starts C): {int(cancellation_rows.sum()):,}")
    print(f"Cancellation-invoice line sales (signed): £{df.loc[cancellation_rows, 'LineSales'].sum():,.2f}")
    print(f"All line sales (signed): £{df['LineSales'].sum():,.2f}")
    print(f"Positive-quantity, nonnegative-price line sales: £{df.loc[positive_sales, 'LineSales'].sum():,.2f}")
    print(f"Sales from named non-merchandise descriptions (before cancellation filter): £{df.loc[excluded_desc, 'LineSales'].sum():,.2f}")
    print(f"PAPER CRAFT, LITTLE BIRDIE rows: {int(birdie.sum()):,}")
    print(f"PAPER CRAFT, LITTLE BIRDIE line sales (signed): £{df.loc[birdie, 'LineSales'].sum():,.2f}")
    if birdie.any():
        print("PAPER CRAFT, LITTLE BIRDIE invoice details:")
        print(df.loc[birdie, ["InvoiceNo", "InvoiceDate", "Quantity", "UnitPrice", "LineSales"]]
              .sort_values("LineSales", ascending=False).head(20).to_string(index=False))

    # Common exploratory views. They are explicit variants, not an assertion that
    # one cleaning policy is correct for every business question.
    base = df.loc[~cancellation_rows & positive_sales].copy()
    product_all = (base.groupby("Description", dropna=False)["LineSales"]
                   .sum().sort_values(ascending=False).rename("Sales").reset_index())
    product_merch = (base.loc[~excluded_desc]
                     .groupby("Description", dropna=False)["LineSales"]
                     .sum().sort_values(ascending=False).rename("Sales").reset_index())
    monthly = (base.groupby("YearMonth", dropna=False)["LineSales"]
               .sum().rename("Sales").reset_index().sort_values("YearMonth"))

    print("\nTop 15 descriptions after excluding cancellation invoices and nonpositive lines:")
    print(product_all.head(15).to_string(index=False))
    print("\nTop 15 after also excluding named non-merchandise descriptions:")
    print(product_merch.head(15).to_string(index=False))
    print("\nMonthly sales using Year-Month key:")
    print(monthly.to_string(index=False))

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        product_all.to_csv(args.output_dir / "product_sales_including_adjustment_descriptions.csv", index=False)
        product_merch.to_csv(args.output_dir / "product_sales_excluding_adjustment_descriptions.csv", index=False)
        monthly.to_csv(args.output_dir / "monthly_sales_year_month.csv", index=False)
        df.loc[birdie].to_csv(args.output_dir / "paper_craft_little_birdie_rows.csv", index=False)
        print(f"\nAudit CSVs written to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
