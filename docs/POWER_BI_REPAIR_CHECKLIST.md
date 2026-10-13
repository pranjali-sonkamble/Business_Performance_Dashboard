# Power BI repair checklist

This file records the required repairs for `powerbi/Business_Performance_Dashboard.pbix`. The README and Python audit script have been updated, but these visual/model changes must be made in Power BI Desktop and the saved PBIX committed before the dashboard itself can be described as fixed.

## 1. Correct the page title

- Open `powerbi/Business_Performance_Dashboard.pbix`.
- Change the visible page title from **Bussiness_Performance_Dashboard** to **Business Performance Dashboard**.
- Rename the report page in the page tab too, if it carries the typo.

## 2. Use one date-only key and a Year-Month axis

The current model appears to expose duplicate date fields (`Invoice_Date` and `InvoiceDate`). Inspect their source and data types before removing either; keep one canonical date field and avoid using both interchangeably.

1. In `Table1`, create a date-only column from the canonical invoice timestamp:
   ```DAX
   InvoiceDateOnly =
       DATE(
           YEAR(Table1[InvoiceDate]),
           MONTH(Table1[InvoiceDate]),
           DAY(Table1[InvoiceDate])
       )
   ```
   Replace `InvoiceDate` above with the verified canonical field if needed.
2. Create a calendar table:
   ```DAX
   Calendar =
       CALENDAR(
           MIN(Table1[InvoiceDateOnly]),
           MAX(Table1[InvoiceDateOnly])
       )
   ```
3. Add these calculated columns to `Calendar`:
   ```DAX
   YearMonth = FORMAT(Calendar[Date], "yyyy-MM")
   YearMonthSort = YEAR(Calendar[Date]) * 100 + MONTH(Calendar[Date])
   MonthName = FORMAT(Calendar[Date], "MMM")
   ```
4. Sort `Calendar[YearMonth]` by `Calendar[YearMonthSort]`; mark `Calendar` as the date table using `Calendar[Date]`.
5. Create a one-to-many relationship from `Calendar[Date]` to `Table1[InvoiceDateOnly]`.
6. Put `Calendar[YearMonth]` on the monthly trend X-axis. Do not use month name alone: December 2010 and December 2011 must be separate points.
7. Check whether the chart is displaying gross or net sales and name its title/axis accordingly.

If the existing model already has a valid calendar table, reuse and repair it rather than creating a duplicate.

## 3. Define cancellation and sales policy before reconciling KPIs

Add a cancellation flag based on the UCI convention that cancellation invoice numbers start with `C`:

```DAX
IsCancellationInvoice =
    LEFT(UPPER(TRIM(Table1[InvoiceNo])), 1) = "C"
```

Add a signed line value:

```DAX
LineSales = Table1[Quantity] * Table1[UnitPrice]
```

The following are different definitions and must not be conflated:

- **Signed net sales:** sum signed line values, retaining negative cancellation/credit-note rows so they can offset sales.
- **Gross merchandise sales:** sum positive-quantity, non-cancellation lines for merchandise only.
- **Orders:** distinct invoice numbers under a documented cancellation policy.
- **Average order value:** the chosen sales measure divided by the compatible order count.

Do not calculate “net sales” by simply deleting every cancellation invoice: that can remove the credit while retaining the original sale. Conversely, do not assume every negative row is a cancellation without inspecting the source. The Python script prints the signed total and cancellation details for reconciliation.

## 4. Exclude non-merchandise descriptions from product rankings

At minimum, review these adjustment/shipping descriptions before publishing product rankings:

- DOTCOM POSTAGE
- MANUAL
- POSTAGE
- BANK CHARGES
- CARRIAGE
- DISCOUNT
- AMAZON FEE
- CRUK COMMISSION
- POSTAGE CHARGES
- SAMPLES

Apply a consistent exclusion rule to product-ranking visuals and label the rule in a tooltip or note. Do not apply it blindly to every financial KPI; postage/discounts may still matter to a broader revenue or adjustment analysis.

## 5. Investigate the PAPER CRAFT, LITTLE BIRDIE outlier

- Run the Python audit script and inspect `outputs/paper_craft_little_birdie_rows.csv`, `outputs/extreme_lines_for_review.csv`, and `outputs/cancellation_invoice_rows.csv`.
- Confirm the invoice number, quantity, line value, and whether the row is actually on a cancellation invoice.
- Do not automatically delete the £168,469.60 line or assert that it was later cancelled without evidence in the source rows.
- If the line is excluded as an anomaly, document the business rule and show its effect on the KPI totals and product ranking.

## 6. Fix KPI names and number formats

For every KPI card, inspect the actual DAX measure and apply these rules:

- **Total Sales:** name it **Gross Merchandise Sales** or **Signed Net Sales** to match the measure; format as GBP (£) with sensible display units (e.g. £10.67M).
- **Orders:** use a documented distinct-invoice definition; cancellation invoices must be treated consistently.
- **Average Order Value:** use `DIVIDE([chosen sales measure], [compatible order count])`; format as GBP (£).
- **Products Sold:** do not use this label for a distinct count of SKUs/descriptions. Use **Distinct Products** for a distinct product count, or **Units Sold** for quantity, as appropriate to the verified DAX expression.
- Reconcile the displayed values to the Python audit outputs before calling them validated.

## 7. Clean presentation and capture final screenshots

- Hide unnecessary Fields/Data, Filters, and Visualizations panes in the published screenshot; use Reading view or a clean presentation layout.
- Use consistent GBP formatting and explicit labels on all currency cards.
- Check that the trend chart has a readable chronological axis and that all report titles are spelled correctly.
- Export fresh screenshots only after the PBIX is saved and refreshed.

## Validation checklist

- [ ] Python audit ran successfully against the downloaded UCI workbook.
- [ ] Gross and signed-net sales are reconciled to the chosen DAX definitions.
- [ ] Cancellation rows and the PAPER CRAFT outlier have been investigated, not guessed.
- [ ] Month trend uses a sorted Year-Month field.
- [ ] KPI titles and formats match their measures.
- [ ] Product rankings exclude the documented non-merchandise descriptions.
- [ ] PBIX saved and committed; screenshots refreshed from the corrected report.
