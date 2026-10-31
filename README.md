# Business Performance Dashboard

An end-to-end **retail sales analytics and business intelligence dashboard** built with the UCI Online Retail dataset. The project uses Power BI, DAX and a reproducible Python audit to turn invoice-level retail transactions into KPIs, time trends, product performance insights and geographic analysis.

## Project status

**Dashboard prototype:** The repository includes a Power BI preview and a prior Power BI Desktop inspection recorded **531,283 rows** in `Table1` and **5 explicit DAX measures** (`Average order Value`, `Distinct Products`, `Total Orders`, `Total Sales`, and `Total Units Sold`). Sales definitions, cancellation completeness, order count, average order value, and filtered product totals have **not yet been independently reconciled against the source workbook and Python audit**, so KPI values remain provisional. The report should not be described as fully validated until the reconciliation steps below are completed.

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

### Latest dashboard
![Business Performance Dashboard — latest refreshed report](images/Business_Performance_Dashboard.png)

> Screenshot from the current repository preview; it is not evidence of reconciled KPI values.

## KPIs

The report is designed to show **Total Sales**, **Total Orders**, **Average Order Value**, and **Distinct Products** (distinct product descriptions, not total units sold). Figures previously recorded for the cleaned workbook—sales **£10,666,684.54**, **20,726** distinct invoice IDs, AOV **£514.65**, and **4,063** distinct descriptions—are **provisional and not certified**. The cleaned workbook reportedly contains no invoice IDs beginning with `C` and no negative quantity/sales rows. Until source cancellation completeness and the sales policy are verified, do not interpret the sales total as validated gross or net sales.

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
5. Follow the [reconciliation checklist](docs/POWER_BI_REPAIR_CHECKLIST.md) in the `docs/` folder. Reconcile Power BI measures against audit output before publishing final figures.

The raw dataset is not included in this repository because of its size. The audit script does not modify the source workbook.

## Validation status

This repository includes a Python audit script, a Power BI report, and a preview image. The following figures remain provisional until the same source workbook, filter policy, and formulas are compared side by side:

- Gross sales versus signed net sales and cancellation/credit treatment.
- Distinct invoice count and the order-count policy.
- Average order value using a compatible sales numerator and order denominator.
- Distinct product descriptions versus units sold.
- Product-ranking totals after the documented non-merchandise exclusions.
- Monthly totals using a chronological Year-Month key.

Reproduce the source-side calculations with `analysis/audit_online_retail.py`, then compare like-for-like outputs with the refreshed PBIX in Power BI Desktop. Only label the KPI values as reconciled after documenting the chosen definitions and matching results. The implementation detail checklist is maintained in [`docs/POWER_BI_REPAIR_CHECKLIST.md`](docs/POWER_BI_REPAIR_CHECKLIST.md); it is a developer worksheet, not a project deliverable.

## Data source and licensing

**Dataset:** Online Retail, UCI Machine Learning Repository, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

> Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

The Power BI file contains data derived from this dataset. The project's original code, report design and documentation are released under the [MIT License](LICENSE); that license does not apply to the UCI dataset.

## Author

**Pranjali Sonkamble**

Focus areas: Data Analytics, Business Intelligence, AI/ML and practical data applications.
