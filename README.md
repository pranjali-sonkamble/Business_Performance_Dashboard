# Business Performance Dashboard

An end-to-end retail sales performance dashboard built on the UCI Online Retail dataset — covering revenue trends, product performance, and geographic sales concentration for a UK-based online retailer.

---

## Table of Contents
- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Dashboard Preview](#dashboard-preview)
- [Key Findings](#key-findings)
- [Business Recommendations](#business-recommendations)
- [How to Reproduce](#how-to-reproduce)
- [Limitations & Future Work](#limitations--future-work)
- [Tools & Technologies](#tools--technologies)

---

## Problem Statement

A retail business needs a single view of sales performance to answer the questions that actually drive decisions: what's the revenue trend, which products are carrying the business, and where is the customer base concentrated geographically. This dashboard consolidates raw transaction-level data into a decision-ready view for that purpose.

---

## Dataset

This project uses the **UCI Online Retail dataset** — real transaction-level data from a UK-based online retailer selling mostly unique all-occasion gifts, covering **December 2010 to December 2011**. Each row is a single line item within an invoice, with fields for invoice number, product code/description, quantity, unit price, invoice date, customer ID, and country. It was chosen because it's a genuine (not synthetic) e-commerce dataset, which surfaces real messiness — like non-product entries mixed into the product list (see [Limitations](#limitations--future-work)) — that a synthetic dataset wouldn't show.

---

## Methodology

- **Data cleaning (Excel):** initial feature creation and cleanup before modeling — e.g. deriving `Month` / `Month_Sort` fields for correctly-ordered time trend charts (a common necessity since raw month names sort alphabetically, not chronologically, by default).
- **Data modeling (Power BI):** core measures built with DAX — `Total Sales`, `Total Orders`, `Average Order Value`, and `Products Sold` — driving the four headline KPI cards.
- **Geographic view:** sales by country, with the UK deliberately excluded from that specific chart — the UK is the retailer's home market and dominates volume so heavily that including it flattens every other country's bar to near-invisible. Excluding it is what makes the *secondary* international markets actually readable.

---

## Dashboard Preview

### Full Dashboard View
![Dashboard Overview](images/dashboard_overview.png)

### KPI and Sales Trend View
![KPI and Trend](images/dashboard_kpi_trend.png)

---

## Key Findings

- **10.67M total sales** across **21K orders**, for an average order value of **£514.65**, with **4,063 unique products sold**.
- Monthly sales show a clear upward trend across the year — starting around £0.5M–0.7M in the earlier months and climbing to **£1.5M in the final two months**, roughly a **2x increase** from trough to peak.
- The product performance table reveals a data quality nuance worth calling out directly: the top revenue lines include **"DOTCOM POSTAGE" (£206,248.77)**, **"Manual" (£78,112.82)**, and **"POSTAGE" (£78,101.88)** — these are shipping/manual-adjustment charges, not actual products. The genuine top-selling *product* is **REGENCY CAKESTAND 3 TIER at £174,484.74 across 1,989 orders**, followed by **WHITE HANGING HEART T-LIGHT HOLDER (£106,292.77, 2,260 orders)** — notably the highest *order count* of any line item, suggesting a lower-price, high-frequency bestseller rather than a high-ticket item.
- Excluding the UK (the dominant home market), **Netherlands and EIRE (Ireland)** are the top two international markets by sales, followed by **Germany and France** — a meaningful concentration in just four countries before the drop-off to Australia, Spain, Switzerland, Belgium, Sweden, and Japan.

## Business Recommendations

- Treat "DOTCOM POSTAGE," "Manual," and "POSTAGE" as non-product transaction types and exclude them from product-performance analysis and reporting — as-is, they're inflating the apparent rank of a "top seller" that isn't actually a product.
- Netherlands and Ireland are the clearest candidates for deeper international investment (marketing spend, localized promotions) given they already lead all non-UK markets without dedicated attention.
- WHITE HANGING HEART T-LIGHT HOLDER's combination of high order count and mid-tier revenue suggests it functions as a reliable volume driver — a good candidate for bundling or cross-sell promotions rather than a product to discontinue based on revenue rank alone.

---

## How to Reproduce

1. Download the UCI Online Retail dataset (`Online Retail.xlsx`, UCI Machine Learning Repository).
2. Open the provided `.pbix` file in `powerbi/Business_Performance_Dashboard.pbix` in Power BI Desktop.
3. Point the data source at your local copy of the dataset and refresh.
4. The `Month` / `Month_Sort` fields and core DAX measures (Total Sales, Total Orders, Average Order Value, Products Sold) will recalculate automatically.

*(Raw data isn't included in this repo due to size — the `.pbix` file and dashboard screenshots are provided so the build is reproducible from the public dataset directly.)*

---

## Limitations & Future Work

- **Non-product entries skew "top product" rankings**, as shown above. A cleaner version of this dashboard would filter out postage/manual/adjustment line items at the data-modeling stage rather than leaving them in the product table.
- **Month field doesn't distinguish year.** Since the dataset spans Dec 2010–Dec 2011 (13 months), a chart grouped by calendar month name alone may combine December 2010 and December 2011 into a single bucket. Worth verifying, and switching to a proper year-month axis if so.
- **No customer-level segmentation yet** — the dataset includes `CustomerID`, which would support repeat-vs-one-time customer analysis, cohort retention, or CLV estimation as a strong next iteration.
- **No profitability view** — this dashboard covers revenue and order volume, not margin. Without cost data, "top product by revenue" isn't the same as "most profitable product."

---

## Tools & Technologies

- **Excel** — data cleaning and feature creation
- **Power BI** — data modeling, DAX measures, dashboard visualization
- **Dataset:** UCI Online Retail dataset (UK-based online retailer, Dec 2010–Dec 2011)

---

## Author

Pranjali Sonkamble
