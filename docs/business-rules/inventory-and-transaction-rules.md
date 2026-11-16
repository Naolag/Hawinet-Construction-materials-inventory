# Inventory and Transaction Rules

- Stock is displayed in each inventory item's primary stock unit.
- Alternative-unit conversion factors belong to an inventory item, not a global unit pair.
- Posting is the point at which stock movement occurs; drafts do not change stock.
- Sales can be paid, partially paid or unpaid, with subsequent payment entries.
- Stock-out transactions must not reduce available stock below zero.
- Returns reference original posted transactions and cannot exceed eligible remaining quantities.
- Voiding a posted transaction requires authorization and a reason; stock movements must be reversed atomically.
- Transaction date and identifiers are system-generated.
- These are UI/business rules; enforcement remains the backend's responsibility.
