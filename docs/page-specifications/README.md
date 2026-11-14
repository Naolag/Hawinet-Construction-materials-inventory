# Hawinet Page Specifications

## Workspace
- Dashboard: daily sales, gross profit, total orders, sales by category, unpaid sales, weekly stock movement, inventory overview and stock requiring attention.
- Products: product identity and optional variants. Active parent products only in the catalog; brand appears beneath the product name. No stock intake or sales on this page.
- Inventory Management: inventory-level records, base-unit stock, item-specific minimum stock and per-unit purchase/selling prices. It is not a transaction history or stock movement entry page. Provide quick links to Measurement Units and Unit Conversions.
- Transactions: primary operational area for stock receipt, sale, customer return, supplier return, stock increase and stock decrease. One New Transaction selector. Include transaction history, drafts, posting, voiding and partial/unpaid sales presentation.
- Measurement Units: reusable unit definitions.
- Unit Conversions: item-specific conversion factors. A unit such as a pack may represent different quantities for different inventory items.
- Reports: separate destination for inventory availability, low-stock and out-of-stock summaries.
- Categories: product categorization and category-level attributes context.
- Employee Management: employee directory and role presentation.
- Settings: business information, regional preferences and transaction safeguards.

## Responsive behavior
Desktop: dark sidebar and full tables. Tablet: compact navigation and flexible content. Mobile: dismissible drawer, stacked controls and summary cards; avoid forcing wide tables onto narrow screens.

## Transaction type forms
Each transaction type has its own form context. Stock receipt identifies supplier and supplier reference; sale identifies customer and payment state; customer return references the original sale and reason; supplier return references original receipt and reason; stock adjustments require a reason. Transaction date and ID are system-generated in the intended product.
