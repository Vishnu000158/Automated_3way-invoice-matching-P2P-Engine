import pandas as pd

# 1. LOAD THE 3 RELATIONAL ERP TABLES (Or create them automatically if missing)
po_df = pd.DataFrame([
    {"PO_ID": "PO-501", "Vendor_Name": "Aarti Industries Ltd", "SKU_Name": "DMAP Pure Grade", "PO_Qty": 2500, "PO_Unit_Price": 980},
    {"PO_ID": "PO-502", "Vendor_Name": "Chempure Private Ltd", "SKU_Name": "Benzoic Acid Technical", "PO_Qty": 8000, "PO_Unit_Price": 310},
    {"PO_ID": "PO-503", "Vendor_Name": "Urmi Chemicals", "SKU_Name": "DMAP Catalyst Grade", "PO_Qty": 2000, "PO_Unit_Price": 1000},
    {"PO_ID": "PO-504", "Vendor_Name": "Sinochem Pharma China", "SKU_Name": "HATU Coupling Reagent", "PO_Qty": 1500, "PO_Unit_Price": 2450},
    {"PO_ID": "PO-505", "Vendor_Name": "Sanjay Industries", "SKU_Name": "Benzoic Acid IP/BP", "PO_Qty": 6500, "PO_Unit_Price": 340},
    {"PO_ID": "PO-506", "Vendor_Name": "Zhejiang Chem Import", "SKU_Name": "HATU Peptide Grade", "PO_Qty": 1200, "PO_Unit_Price": 2500},
    {"PO_ID": "PO-507", "Vendor_Name": "Nutron Chemicals", "SKU_Name": "DMAP High Purity", "PO_Qty": 3000, "PO_Unit_Price": 990},
    {"PO_ID": "PO-508", "Vendor_Name": "Jiangsu Fine Chem China", "SKU_Name": "Benzoic Acid Flakes", "PO_Qty": 9000, "PO_Unit_Price": 290}
])

grn_df = pd.DataFrame([
    {"GRN_ID": "GRN-901", "PO_ID": "PO-501", "Received_Qty": 2500},
    {"GRN_ID": "GRN-902", "PO_ID": "PO-502", "Received_Qty": 8000},
    {"GRN_ID": "GRN-903", "PO_ID": "PO-503", "Received_Qty": 1850},
    {"GRN_ID": "GRN-904", "PO_ID": "PO-504", "Received_Qty": 1500},
    {"GRN_ID": "GRN-905", "PO_ID": "PO-505", "Received_Qty": 6500},
    {"GRN_ID": "GRN-906", "PO_ID": "PO-506", "Received_Qty": 1050},
    {"GRN_ID": "GRN-907", "PO_ID": "PO-507", "Received_Qty": 3000}
])

inv_df = pd.DataFrame([
    {"Invoice_ID": "INV-701", "PO_ID": "PO-501", "Billed_Qty": 2500, "Billed_Unit_Price": 980},
    {"Invoice_ID": "INV-702", "PO_ID": "PO-502", "Billed_Qty": 8000, "Billed_Unit_Price": 325},
    {"Invoice_ID": "INV-703", "PO_ID": "PO-503", "Billed_Qty": 2000, "Billed_Unit_Price": 1000},
    {"Invoice_ID": "INV-704", "PO_ID": "PO-504", "Billed_Qty": 1500, "Billed_Unit_Price": 2450},
    {"Invoice_ID": "INV-705", "PO_ID": "PO-505", "Billed_Qty": 6500, "Billed_Unit_Price": 355},
    {"Invoice_ID": "INV-706", "PO_ID": "PO-506", "Billed_Qty": 1200, "Billed_Unit_Price": 2500},
    {"Invoice_ID": "INV-707", "PO_ID": "PO-507", "Billed_Qty": 3000, "Billed_Unit_Price": 990},
    {"Invoice_ID": "INV-708", "PO_ID": "PO-508", "Billed_Qty": 9000, "Billed_Unit_Price": 290}
])

# 2. PERFORM 3-WAY LEFT JOIN & CALCULATE EXACT RUPEE LEAKAGE
merged = po_df.merge(grn_df, on="PO_ID", how="left").merge(inv_df, on="PO_ID", how="left")
merged["Received_Qty"] = merged["Received_Qty"].fillna(0)
merged["Payable_Value_INR"] = merged["Received_Qty"] * merged["PO_Unit_Price"]
merged["Invoiced_Value_INR"] = merged["Billed_Qty"] * merged["Billed_Unit_Price"]
merged["Leakage_Blocked_INR"] = merged["Invoiced_Value_INR"] - merged["Payable_Value_INR"]

def audit_bill(r):
    if pd.isna(r["GRN_ID"]):
        return "BLOCK: Missing GRN (In-Transit)"
    elif r["Billed_Unit_Price"] > r["PO_Unit_Price"]:
        return "BLOCK: Price Overbilling"
    elif r["Billed_Qty"] > r["Received_Qty"]:
        return "BLOCK: Quantity Shortage"
    return "APPROVE: 3-Way Match Passed"

merged["Audit_Status"] = merged.apply(audit_bill, axis=1)

# 3. EXPORT FULL AUDIT REPORT TO EXCEL
merged.to_excel("P2P_3Way_Audit_Report.xlsx", index=False)
print("✅ SUCCESS: P2P_3Way_Audit_Report.xlsx created in your folder!")
print(f"💰 TOTAL PAYMENT LEAKAGE PREVENTED: Rs. {merged['Leakage_Blocked_INR'].sum():,.0f}\n")

# 4. AUTO-DRAFT VENDOR DISPUTE / CREDIT NOTE EMAILS FOR BLOCKED BILLS
blocked = merged[merged["Audit_Status"] != "APPROVE: 3-Way Match Passed"]
for _, r in blocked.iterrows():
    print("=" * 65)
    print(f"TO: Accounts Receivable - {r['Vendor_Name']}")
    print(f"SUBJECT: PAYMENT ON HOLD ({r['Audit_Status']}) | {r['Invoice_ID']} / {r['PO_ID']}")
    print(f"Body: Dear {r['Vendor_Name']} Team, Invoice {r['Invoice_ID']} for {r['SKU_Name']} (Billed: Rs. {r['Invoiced_Value_INR']:,.0f}) is on hold due to '{r['Audit_Status']}' (Variance: Rs. {r['Leakage_Blocked_INR']:,.0f}). Please issue a revised invoice or Credit Note to release payment.\n")