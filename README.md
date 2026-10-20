# Business Performance Dashboard

An end-to-end **retail sales analytics and business intelligence dashboard** built with the UCI Online Retail dataset. The project uses Power BI, DAX and a reproducible Python audit to turn invoice-level retail transactions into KPIs, time trends, product performance insights and geographic analysis.

## Project status

**Dashboard repair and metric reconciliation are in progress.** The current Power BI file must be refreshed and validated in Power BI Desktop before the metrics below can be called final. Row count and DAX measure count are intentionally not stated until measured from the source and model.

## Business objective

The dashboard is designed to answer:
- How does sales value change over time?
- Which products and invoice lines contribute most to sales?
- Which international markets contribute most?
- Which data-quality issues could materially distort the results?

## Tech stack

**Power BI** · **DAX** · **Python (pandas audit)** · **Data visualization**

**Dataset:** UCI Online Retail, covering transactions from December 2010 through December 2011.

## Dashboard preview

### Full dashboard
![Dashboard Overview](images/dashboard_overview.png)

### KPI and sales trend
![KPI and Trend](images/dashboard_kpi_trend.png)

> These screenshots are the current repository previews; replace them with screenshots captured from the corrected, refreshed PBIX after repairs are complete.

## KPIs

The report is intended to show **Sales**, **Orders**, **Average Order Value**, and a correctly defined product/quantity metric. The actual values and measure definitions are still being reconciled. Do not treat the existing Power BI card values as verified until they match the independent audit and the selected business definitions.

## Data-quality and interpretation notes

- Use a chronological **Year-Month** key on monthly visuals. A month-name-only axis may combine December 2010 and December 2011.
- Distinguish **gross sales** from **signed net sales**. Signed net sales retains signed cancellation/credit rows so they can offset original transactions; gross sales follows a separately documented inclusion policy.
- Do not treat postage and adjustment entries such as **DOTCOM POSTAGE**, **MANUAL**, and **POSTAGE** as merchandise in product ranking visuals unless the business question explicitly requires them.
- The source includes an extreme-value line for **PAPER CRAFT, LITTLE BIRDIE** (invoice `581483`, 80,995 units at £2.08). The audit script checks the related cancellation/reversal details. Do not remove this line or claim a cancellation offset without verifying the source rows and the policy used by the model.
- Product rankings, order counts and average order value must all use explicitly documented definitions.

## Reproduce the audit

1. Download the [UCI Online Retail dataset](https://doi.org/10.24432/C5BW33).
2. Install dependencies:
   ```bash
   python -m pip install pandas openpyxl
   ```
3. Run:
   ```bash
   python analysis/audit_online_retail.py path/to/Online_Retail.xlsx --output-dir outputs
   ```
4. Open `powerbi/Business_Performance_Dashboard.pbix` in Power BI Desktop and point the model to the local source workbook.
5. Follow [the Power BI repair checklist](docs/POWER_BI_REPAIR_CHECKLIST.md). Reconcile the Power BI measures against audit output before publishing final figures.

The raw dataset is not included in this repository because of its size. The audit script does not modify the source workbook.

## Repair status

- [ ] Verify source/model row counts and document the counting stage.
- [ ] Count explicit DAX measures from the actual Power BI model.
- [ ] Reconcile sales definitions, cancellation handling, order counts and AOV.
- [ ] Repair and sort the Year-Month axis.
- [ ] Correct KPI labels and currency formatting.
- [ ] Apply documented non-merchandise exclusions to product rankings.
- [ ] Refresh and save the PBIX in Power BI Desktop.
- [ ] Replace preview images with fresh screenshots of the corrected report.
- [ ] Commit the reconciled PBIX, screenshots and verified figures.

See [POWER_BI_REPAIR_CHECKLIST.md](docs/POWER_BI_REPAIR_CHECKLIST.md) for implementation details.

## Data source and licensing

**Dataset:** Online Retail, UCI Machine Learning Repository, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

> Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

The Power BI file contains data derived from this dataset. The project's original code, report design and documentation are released under the [MIT License](LICENSE); that license does not apply to the UCI dataset.

## Author

**Pranjali Sonkamble**

Focus areas: Data Analytics, Business Intelligence, AI/ML and practical data applications.
