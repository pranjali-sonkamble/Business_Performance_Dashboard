# Business Performance Dashboard

An end-to-end **retail sales analytics and business intelligence dashboard** built with the UCI Online Retail dataset. The project transforms transaction-level data into decision-ready KPIs, trend analysis, product performance insights, and geographic sales analysis.

## 🎯 Business Objective

Provide a single analytical view to answer:

- How is revenue changing over time?
- Which products and order lines drive sales?
- Which international markets contribute the most revenue?
- What data-quality issues could distort product-performance conclusions?

## 🧰 Tech Stack

**Power BI** · **DAX** · **Data Cleaning** · **Data Visualization**

**Dataset:** UCI Online Retail — UK-based online retailer, December 2010–December 2011.

## 🔄 Analytical Workflow

```
Raw Transaction Data
        ↓
Data Cleaning & Feature Creation
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

- **Total Sales:** £10.67M
- **Orders:** 21K
- **Average Order Value:** £514.65
- **Unique Products:** 4,063

## 🔍 Key Findings

- Monthly sales increased substantially through the analysis period, reaching approximately £1.5M in the final two months.
- Shipping/manual adjustment entries such as **DOTCOM POSTAGE**, **Manual**, and **POSTAGE** can distort product rankings if treated as products.
- **REGENCY CAKESTAND 3 TIER** was the highest genuine product by revenue in the analysis.
- **WHITE HANGING HEART T-LIGHT HOLDER** combined high order frequency with substantial revenue.
- Among non-UK markets, the Netherlands and EIRE were the leading markets by sales in this analysis.

## 💡 Analytical Takeaway

A dashboard is only as reliable as the definitions and data behind its visuals. Product rankings require distinguishing genuine merchandise from postage and adjustment transactions.

## ▶️ Reproduce the Analysis

1. Download the UCI Online Retail dataset.
2. Open `powerbi/Business_Performance_Dashboard.pbix` in Power BI Desktop.
3. Point the model to your local dataset.
4. Refresh the model.
5. Review the DAX-driven KPIs and visual analysis.

Raw data is not included because of size; the project is designed to be reproducible from the public dataset.

## ⚠️ Limitations & Next Steps

- Use a proper Year-Month dimension rather than month name alone.
- Exclude non-product transaction types during modeling.
- Add customer segmentation and retention analysis.
- Add profitability analysis when cost data is available.

---

## Data Source & Licensing

The project uses the **Online Retail** dataset from the UCI Machine Learning Repository: [Online Retail dataset](https://doi.org/10.24432/C5BW33). Cite it as: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. The dataset is licensed under **CC BY 4.0**; attribution is required when sharing or adapting the dataset.

The MIT License in this repository applies only to original project code and documentation. It does not replace or supersede the dataset's CC BY 4.0 terms.

## 👩‍💻 Author

**Pranjali Sonkamble**

Focused on **Data Analytics, Business Intelligence, AI/ML, and practical data applications**.
