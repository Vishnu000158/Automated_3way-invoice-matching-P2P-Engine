# Automated_3way-invoice-matching-P2P-Engine
SQL(LEFT JOIN) &amp; Python P2P reconciliation engine blocks price overbilling, quantity shortages, and missing-GRN invoices before payment


Automated 3-Way Invoice Matching & P2P Leakage Engine

*Author:* Vishnu Pathak | *Domain:* Procure-to-Pay (P2P) & Supply Chain Analytics  
*Tech Stack:* SQL (LEFT JOIN, CASE WHEN, COALESCE), Python (pandas), Advanced Excel (XLOOKUP)

---

# Business Problem Solved
In high-volume procurement operations, manual invoice checking often leads to paying for *short-delivered goods, **unauthorized vendor price hikes, or **in-transit shipments without a warehouse GRN*. This engine reconciles Purchase Orders (PO), Goods Receipt Notes (GRN), and Vendor Invoices (INV) simultaneously to block financial leakage before payment release.

# Key Audit Results (₹2.00+ Crore Audited)
- *Total Payment Leakage Prevented:* *₹33,52,500* across 5 blocked invoices:
  - *Missing GRN (Goods In-Transit):* Blocked *₹26,10,000* (PO-508 — Jiangsu Fine Chem China)
  - *Quantity Shortages:* Blocked *₹5,25,000* (PO-506 — Zhejiang Chem Import & PO-503 — Urmi Chemicals)
  - *Price Overbilling:* Blocked *₹2,17,500* (PO-502 — Chempure Private Ltd & PO-505 — Sanjay Industries)
- *Auto-Approved Clean Invoices:* Cleared *₹90,95,000* (PO-501, PO-504, PO-507) with zero manual intervention.

# Live SQL 3-Way Match Output
![3-Way Match SQL Audit](Project2_SQL_3Way_Match.png)
