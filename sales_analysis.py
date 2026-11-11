import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================
# 1. LOAD DATASET
# =====================================

folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(folder, "Day-2 Challenge.csv"))

print("ORIGINAL DATASET")
print(df.to_string(index=False))

print("\nTOTAL RECORDS:", len(df))
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

# =====================================
# 2. DATA VALIDATION
# =====================================

print("\nMISSING VALUES:")
print(df.isnull().sum())

valid_condition = (
    df["OrderID"].notna() &
    df["OrderID"].astype(str).str.strip().ne("") &
    pd.to_datetime(df["OrderDate"], errors="coerce").notna() &
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0) &
    (df["UnitCost"] >= 0) &
    ~df["OrderID"].duplicated(keep=False)
)

valid = df[valid_condition].copy()
invalid = df[~valid_condition].copy()

print("\nINVALID RECORDS")
print(invalid.to_string(index=False))

print("\nVALIDATION SUMMARY")
print("Total Records:", len(df))
print("Valid Records:", len(valid))
print("Invalid Records:", len(invalid))
print("Invalid IDs:", invalid["OrderID"].tolist())

# =====================================
# 3. SALES CALCULATIONS
# =====================================

valid["Revenue"] = valid["Quantity"] * valid["UnitPrice"]

total_revenue = valid["Revenue"].sum()
total_orders = valid["OrderID"].nunique()
total_quantity = int(valid["Quantity"].sum())

aov = total_revenue / total_orders if total_orders else 0

print("\nSALES CALCULATIONS")
print("Total Revenue:", round(total_revenue, 2))
print("Total Valid Orders:", total_orders)
print("Average Order Value:", round(aov, 2))
print("Total Quantity Sold:", total_quantity)

# =====================================
# 4. PRODUCT-WISE ANALYSIS
# =====================================

product_revenue = valid.groupby(
    "ProductName"
)["Revenue"].sum().sort_values(ascending=False)

product_quantity = valid.groupby(
    "ProductName"
)["Quantity"].sum().sort_values(ascending=False)

print("\nPRODUCT-WISE REVENUE")
print(product_revenue)

print("\nPRODUCT-WISE QUANTITY")
print(product_quantity)

top_product = (
    product_revenue.idxmax()
    if not product_revenue.empty else None
)

top_quantity_product = (
    product_quantity.idxmax()
    if not product_quantity.empty else None
)

print("\nTOP PRODUCT BY REVENUE:", top_product)
print("TOP PRODUCT BY QUANTITY:", top_quantity_product)

# =====================================
# 5. REGION-WISE ANALYSIS
# =====================================

if "Region" in valid.columns:
    region_revenue = valid.groupby(
        "Region"
    )["Revenue"].sum().sort_values(ascending=False)

    top_region = (
        region_revenue.idxmax()
        if not region_revenue.empty else None
    )

    print("\nREGION-WISE REVENUE")
    print(region_revenue)

    print("\nHIGHEST REVENUE REGION:", top_region)

else:
    region_revenue = pd.Series(dtype=float)
    top_region = None
    print("\nRegion column not found in dataset.")

# =====================================
# 6. REVENUE CHART
# =====================================

if not product_revenue.empty:
    product_revenue.plot(
        kind="bar",
        color="skyblue",
        title="Revenue by Product"
    )

    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "revenue_chart.png"))
    plt.show()
    plt.close()

# =====================================
# 7. QUANTITY CHART
# =====================================

if not product_quantity.empty:
    product_quantity.plot(
        kind="bar",
        color="orange",
        title="Quantity Sold by Product"
    )

    plt.xlabel("Product")
    plt.ylabel("Quantity")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "quantity_chart.png"))
    plt.show()
    plt.close()

# =====================================
# 8. CREATE SALES SUMMARY
# =====================================

sales_summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Valid Orders",
        "Average Order Value",
        "Total Quantity Sold",
        "Top Performing Product",
        "Highest Revenue Region"
    ],
    "Value": [
        round(total_revenue, 2),
        total_orders,
        round(aov, 2),
        total_quantity,
        top_product,
        top_region
    ]
})

# =====================================
# 9. CREATE PRODUCT ANALYSIS
# =====================================

product_analysis = valid.groupby("ProductName").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Quantity=("Quantity", "sum")
).reset_index()

# =====================================
# 10. EXPORT CSV FILES
# =====================================

sales_summary.to_csv(
    os.path.join(folder, "sales_summary.csv"),
    index=False
)

product_analysis.to_csv(
    os.path.join(folder, "product_analysis.csv"),
    index=False
)

valid.to_csv(
    os.path.join(folder, "valid_sales_data.csv"),
    index=False
)

invalid.to_csv(
    os.path.join(folder, "invalid_sales_data.csv"),
    index=False
)

print("\n=====================================")
print("PROJECT COMPLETED SUCCESSFULLY!")
print("=====================================")

print("\nCSV FILES CREATED:")
print("1. sales_summary.csv")
print("2. product_analysis.csv")
print("3. valid_sales_data.csv")
print("4. invalid_sales_data.csv")

print("\nSAVED LOCATION:", folder)