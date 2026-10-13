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
        birdie_rows = df.loc[birdie, [
            "InvoiceNo", "InvoiceDate", "Quantity", "UnitPrice", "LineSales",
            "IsCancellationInvoice",
        ]].copy()
        print("PAPER CRAFT, LITTLE BIRDIE invoice details (C-prefixed invoices are cancellation invoices):")
        print(birdie_rows.sort_values("LineSales", ascending=False).head(20).to_string(index=False))
        print("PAPER CRAFT, LITTLE BIRDIE grouped by invoice:")
        print(birdie_rows.groupby(
            ["InvoiceNo", "IsCancellationInvoice"], dropna=False
        ).agg(
            rows=("LineSales", "size"),
            quantity=("Quantity", "sum"),
            line_sales=("LineSales", "sum"),
        ).sort_values("line_sales", ascending=False).head(20).to_string())

    # Surface extreme lines for review rather than silently deleting them.
    # A high-value row is not automatically erroneous.
    extreme_lines = df.loc[
        df["Quantity"].abs().ge(10_000) | df["LineSales"].abs().ge(10_000),
        ["InvoiceNo", "InvoiceDate", "StockCode", "Description", "Quantity",
         "UnitPrice", "LineSales", "IsCancellationInvoice"],
    ].copy().sort_values("LineSales", key=lambda values: values.abs(), ascending=False)
    print(f"\nExtreme lines requiring review (|quantity| >= 10,000 or |line sales| >= £10,000): {len(extreme_lines):,}")
    if not extreme_lines.empty:
        print(extreme_lines.head(30).to_string(index=False))

    # Gross sales excludes cancellation invoices and nonpositive lines.
    # Net sales retains signed cancellation lines so they can offset original sales.
    # These are different business definitions; neither should be silently labelled
    # simply "Sales" without documenting the selected policy.
    gross_base = df.loc[~cancellation_rows & positive_sales].copy()
    net_base = df.loc[~excluded_desc].copy()

    product_gross_all = (gross_base.groupby("Description", dropna=False)["LineSales"]
                         .sum().sort_values(ascending=False).rename("GrossSales").reset_index())
    product_gross_merch = (gross_base.loc[~excluded_desc]
                           .groupby("Description", dropna=False)["LineSales"]
                           .sum().sort_values(ascending=False).rename("GrossSales").reset_index())
    product_net_merch = (net_base.groupby("Description", dropna=False)["LineSales"]
                         .sum().sort_values(ascending=False).rename("NetSales").reset_index())
    monthly_gross = (gross_base.groupby("YearMonth", dropna=False)["LineSales"]
                     .sum().rename("GrossSales").reset_index().sort_values("YearMonth"))
    monthly_net = (net_base.groupby("YearMonth", dropna=False)["LineSales"]
                   .sum().rename("NetMerchandiseSales").reset_index().sort_values("YearMonth"))

    print("\nTop 15 descriptions by gross sales (cancellation invoices/nonpositive lines excluded):")
    print(product_gross_all.head(15).to_string(index=False))
    print("\nTop 15 merchandise descriptions by gross sales (named adjustments excluded):")
    print(product_gross_merch.head(15).to_string(index=False))
    print("\nTop 15 merchandise descriptions by signed net sales (cancellation rows retained):")
    print(product_net_merch.head(15).to_string(index=False))
    print("\nMonthly gross sales using Year-Month key:")
    print(monthly_gross.to_string(index=False))
    print("\nMonthly signed net merchandise sales using Year-Month key:")
    print(monthly_net.to_string(index=False))

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        product_gross_all.to_csv(args.output_dir / "product_gross_sales_including_adjustment_descriptions.csv", index=False)
        product_gross_merch.to_csv(args.output_dir / "product_gross_sales_merchandise_only.csv", index=False)
        product_net_merch.to_csv(args.output_dir / "product_net_sales_merchandise_only.csv", index=False)
        monthly_gross.to_csv(args.output_dir / "monthly_gross_sales_year_month.csv", index=False)
        monthly_net.to_csv(args.output_dir / "monthly_net_merchandise_sales_year_month.csv", index=False)
        df.loc[birdie].to_csv(args.output_dir / "paper_craft_little_birdie_rows.csv", index=False)
        extreme_lines.to_csv(args.output_dir / "extreme_lines_for_review.csv", index=False)
        df.loc[cancellation_rows].to_csv(args.output_dir / "cancellation_invoice_rows.csv", index=False)
        print(f"\nAudit CSVs written to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
