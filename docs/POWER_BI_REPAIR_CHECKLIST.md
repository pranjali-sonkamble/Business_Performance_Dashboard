# Power BI repair checklist

This checklist distinguishes fixes that can be prepared in documentation from fixes that require Power BI Desktop and the source workbook. Do not mark the dashboard as corrected until the saved PBIX and refreshed screenshots are committed.

## 0. Create a working copy

1. Pull the latest `main` branch.
2. Open `powerbi/Business_Performance_Dashboard.pbix` in Power BI Desktop.
3. Use **File → Save As** to create a backup copy before editing.
4. Obtain the official UCI Online Retail workbook from the dataset link in the README and record the downloaded filename/date.
5. In Power Query, inspect the source columns and types. Keep a single verified invoice timestamp field and do not assume similarly named date fields are identical.

## 1. Dataset facts and model inventory

Record these from the refreshed model before changing measures:
- Source data rows loaded (exclude the column-header row).
- Model tables and columns.
- Total DAX measures (explicit measures only; do not count calculated columns as measures).
- Calculated columns, relationships, and any Power Query filtering.
- Min/max invoice date, nulls in key fields, and duplicate-row checks.

The row count should be measured against the same stage used by the report: raw worksheet rows versus rows remaining after Power Query filters are not necessarily equal. Document which count is reported.

## 2. Repair date granularity and sorting

Prefer an existing valid calendar table if present; do not create duplicates.

If the fact table is `Table1` and its verified timestamp column is `InvoiceDate`, add a date-only column:

```DAX
InvoiceDateOnly =
DATE(
    YEAR(Table1[InvoiceDate]),
    MONTH(Table1[InvoiceDate]),
    DAY(Table1[InvoiceDate])
)
```

Create a calendar table only if one does not already exist:

```DAX
Calendar =
CALENDAR(
    MIN(Table1[InvoiceDateOnly]),
    MAX(Table1[InvoiceDateOnly])
)
```

Add to Calendar:

```DAX
YearMonth = FORMAT(Calendar[Date], "yyyy-MM")
YearMonthSort = YEAR(Calendar[Date]) * 100 + MONTH(Calendar[Date])
MonthName = FORMAT(Calendar[Date], "MMM")
```

Then:
1. Sort `Calendar[YearMonth]` by `Calendar[YearMonthSort]`.
2. Mark Calendar as the date table using `Calendar[Date]`.
3. Create/verify a one-to-many relationship from `Calendar[Date]` to `Table1[InvoiceDateOnly]`.
4. Use `Calendar[YearMonth]` on the monthly trend axis—not month name alone.
5. Confirm December 2010 and December 2011 display as distinct periods.

## 3. Establish sales definitions before fixing cards

Create/verify these base fields (replace column names only after confirming the actual model schema):

```DAX
LineSales = Table1[Quantity] * Table1[UnitPrice]

IsCancellationInvoice =
LEFT(UPPER(TRIM(Table1[InvoiceNo])), 1) = "C"
```

Document the chosen KPI policy:
- **Gross merchandise sales:** positive quantity, non-cancellation invoice lines, excluding documented non-merchandise descriptions.
- **Signed net sales:** signed line values, retaining credit/cancellation rows so they can offset original sales; state whether adjustments/non-merchandise lines are included.
- **Orders:** distinct invoices under an explicit cancellation policy.
- **Average order value:** the selected sales measure divided by a compatible order count.
- **Products sold:** rename to **Distinct Products** if it counts distinct products/descriptions; use **Units Sold** if it sums quantities.

Do not remove every cancellation invoice from signed net sales; doing so can remove the credit while retaining the original transaction. Do not silently delete the high-value PAPER CRAFT transaction. Inspect invoice 581483 and cancellation invoice C581484 in the source, verify their descriptions and quantities, then document the treatment.

For product ranking visuals, review and consistently exclude non-merchandise descriptions including DOTCOM POSTAGE, MANUAL, POSTAGE, BANK CHARGES, CARRIAGE, DISCOUNT, AMAZON FEE, CRUK COMMISSION, POSTAGE CHARGES, and SAMPLES. Do not automatically apply this product-ranking exclusion to every financial KPI.

## 4. Format and label visuals

- Correct the report/page title to **Business Performance Dashboard**.
- Label the sales card to match its definition: **Gross Merchandise Sales** or **Signed Net Sales**, not a vague Total Sales if its meaning is ambiguous.
- Format all currency measures as GBP (£), with consistent decimal/display units.
- Verify KPI labels and DAX expressions agree.
- Give the monthly trend a clear title that indicates gross or net sales.
- Add a tooltip/note to product rankings describing merchandise exclusions.
- Hide editing panes and refresh screenshots only after saving and refreshing the PBIX.

## 5. Verify the figures

Run the reproducible audit script from the repository root:

```bash
python -m pip install pandas openpyxl
python analysis/audit_online_retail.py path/to/Online_Retail.xlsx --output-dir outputs
```

Save the console output and outputs CSVs locally; do not commit the full raw dataset. Compare the dataset row count and selected sales definitions against Power BI after applying equivalent filters and policies.

Publish figures only after independently reconciling:
- source row count and model row count;
- explicit DAX measure count;
- sales total(s) and cancellation treatment;
- invoice/order count;
- average order value;
- distinct product or unit count;
- monthly totals using Year-Month keys.

## Completion checklist

- [ ] PBIX backed up before editing.
- [ ] Source row count and report-model row count verified and definitions documented.
- [ ] Explicit DAX measures counted from the model.
- [ ] Sales/cancellation policy documented and reconciled to the Python audit.
- [ ] Year-Month axis chronologically sorted and December periods separated.
- [ ] KPI names, formulas, and GBP formats agree.
- [ ] Product-ranking exclusions documented and applied consistently.
- [ ] Report refreshed and saved in Power BI Desktop.
- [ ] Fresh screenshots captured from the corrected report.
- [ ] Corrected PBIX, screenshots, README figures, and checklist committed together.
