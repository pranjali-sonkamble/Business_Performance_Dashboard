# Business Performance Dashboard

An end-to-end **retail sales analytics and business intelligence dashboard** built with the UCI Online Retail dataset. The project transforms transaction-level data into decision-ready KPIs, trend analysis, product performance insights, and geographic sales analysis.

## 🎯 Business Objective

Provide a single analytical view to answer:

- How is revenue changing over time?
- Which products and order lines drive sales?
- Which international markets contribute the most revenue?
- What data-quality issues could distort product-performance conclusions?

## 🧰 Tech Stack

**Power BI** · **DAX** · **Python (pandas audit/cleaning script)** · **Data Visualization**

**Dataset:** UCI Online Retail — UK-based online retailer, December 2010–December 2011.

## 🔄 Analytical Workflow

```
Raw Transaction Data
        ↓
Python audit / cleaning (reproducible script)
        ↓
Power BI Data Model
        ↓
DAX Measures & KPIs
        ↓
Sales / Product / Geographic Analysis
        ↓
Business Insights
```

## 📊 Dashboard Preview

### Full Dashboard
![Dashboard Overview](images/dashboard_overview.png)

### KPI & Sales Trend
![KPI and Trend](images/dashboard_kpi_trend.png)

## 📌 Core KPIs

> **Validation status:** The figures below are the values currently displayed by the PBIX, not yet independently reconciled. Do not present them as verified business KPIs until the cancellation policy, DAX definitions, and source totals have been checked.
- **Total Sales:** £10.67M *(current PBIX value; this is consistent with a commonly reported gross-positive-line calculation, but the exact PBIX measure is not inspectable from the repository connector. If the measure excludes C-prefixed cancellation invoices but retains positive original lines, it still includes invoice `581483` (£168,469.60) even though that order was cancelled 12 minutes later. Do not label this as reconciled net sales.)*
- **Orders:** 21K *(current PBIX value; verify distinct invoice count and treatment of cancellation invoices)*
- **Average Order Value:** £514.65 *(current PBIX value; verify as consistently defined Sales ÷ Orders)*
- **Products Sold:** 4,063 *(current PBIX value; confirm whether this means distinct SKUs, descriptions, units, or transaction lines before renaming the card)*

## 🔍 Key Findings

- Monthly sales should be reviewed using a Year-Month key (for example, `2010-12`, `2011-12`) before stating month-specific totals. The month-name-only visual can combine December 2010 and December 2011.
- Shipping/manual adjustment entries such as **DOTCOM POSTAGE**, **Manual**, and **POSTAGE** can distort product rankings if treated as products; the published product ranking should exclude them explicitly and document the rule.
- **REGENCY CAKESTAND 3 TIER** ranked highly in the existing analysis; treat the rank as provisional until signed cancellation lines and non-merchandise descriptions are handled consistently.
- **PAPER CRAFT, LITTLE BIRDIE** contains a confirmed extreme-value transaction: invoice `581483` records 80,995 units at £2.08 (£168,469.60). The source also contains reversal/cancellation invoice `C581484` for -80,995 units at £2.08 on 2011-12-09 09:27, associated with the same customer and description (the raw source varies punctuation spacing). The positive line is therefore offset by a later cancellation in signed net sales, but a gross-sales measure that drops cancellation invoices can still count the £168,469.60 original. The audit script normalizes description punctuation and prints both sides; the PBIX must apply an explicit, consistent policy.
- **WHITE HANGING HEART T-LIGHT HOLDER** combined high order frequency with substantial revenue.
- Among non-UK markets, the Netherlands and EIRE were the leading markets by sales in this analysis.

## 💡 Analytical Takeaway

A dashboard is only as reliable as the definitions and data behind its visuals. Product rankings require distinguishing genuine merchandise from postage and adjustment transactions.

## ▶️ Reproduce the Analysis

1. Download the [UCI Online Retail dataset](https://doi.org/10.24432/C5BW33).
2. Install the Python dependencies `pandas` and `openpyxl` (`pip install pandas openpyxl`).
3. Run `python analysis/audit_online_retail.py path/to/Online_Retail.xlsx --output-dir outputs`. It reports signed sales, cancellation invoices, the `PAPER CRAFT, LITTLE BIRDIE` rows, extreme-value lines, gross and signed-net product rankings, and gross/net monthly sales by Year-Month. The source workbook is never modified.
4. Open `powerbi/Business_Performance_Dashboard.pbix` in Power BI Desktop and point the model to your local dataset.
5. Follow [Power BI repair steps](docs/POWER_BI_REPAIR_CHECKLIST.md): fix the page title, replace month-name-only axes with a sorted Year-Month key, make KPI names/formatting match their DAX definitions, and reconcile gross/net sales before publishing.

Raw data is not included because of size; the project is designed to be reproducible from the public dataset.

## ⚠️ Limitations & Next Steps

- **Dashboard file still requires manual Power BI Desktop edits.** The repository README and audit script are corrected, but the PBIX visuals/model are not represented as fixed until the updated PBIX is saved and committed.
- Reconcile gross sales versus signed net sales, including the confirmed `581483` / `C581484` reversal, before presenting Total Sales as final. A simple `InvoiceNo` starts-with-`C` filter is not enough to remove the original cancelled sale from a gross-sales calculation.
- Use a proper Year-Month dimension rather than month name alone; December 2010 and December 2011 must remain separate.
- Exclude non-product transaction types during product ranking, with an explicit documented list.
- Add customer segmentation and retention analysis.
- Add profitability analysis when cost data is available.

---

## 📄 Data Source & Licensing

**Dataset:** Online Retail, UCI Machine Learning Repository, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

> Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

The Power BI file (`powerbi/Business_Performance_Dashboard.pbix`) includes data derived from this dataset. Changes made in this project: cleaning, feature creation, and aggregation for the dashboard.

**Code license:** Original work in this repository (report design, measures, documentation) is released under the [MIT License](LICENSE). The MIT License does not apply to the UCI dataset, which stays under CC BY 4.0.

## 👩‍💻 Author

**Pranjali Sonkamble**

Focused on **Data Analytics, Business Intelligence, AI/ML, and practical data applications**.
