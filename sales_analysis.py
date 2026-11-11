import pandas as pd
import matplotlib.pyplot as plt

# Load the actual CSV dataset
df = pd.read_csv("Day-2 Challenge.csv")

# Display the dataset
print("ORIGINAL DATASET")
print(df.to_string(index=False))

# Check total records
print("\nTOTAL RECORDS:", len(df))

# Check columns
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

# Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# DATA VALIDATION

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

# TOTAL REVENUE

valid["Revenue"] = (
    valid["Quantity"] * valid["UnitPrice"]
)

total_revenue = valid["Revenue"].sum()

# TOTAL ORDERS

total_orders = valid["OrderID"].nunique()

# AVERAGE ORDER VALUE

aov = total_revenue / total_orders if total_orders else 0

print("\nSALES CALCULATIONS")

print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Average Order Value:", round(aov, 2))

# PRODUCT-WISE REVENUE

product_revenue = valid.groupby(
    "ProductName"
)["Revenue"].sum().sort_values(ascending=False)

print("\nPRODUCT-WISE REVENUE")
print(product_revenue)

print("\nTOP PRODUCT BY REVENUE")
print(product_revenue.head(1))

# PRODUCT-WISE QUANTITY

product_quantity = valid.groupby(
    "ProductName"
)["Quantity"].sum().sort_values(ascending=False)

print("\nPRODUCT-WISE QUANTITY")
print(product_quantity)

print("\nTOP PRODUCT BY QUANTITY")

print(
    product_quantity[
        product_quantity == product_quantity.max()
    ]
)

# REVENUE CHART

product_revenue.plot(
    kind="bar",
    color="skyblue",
    title="Revenue by Product"
)

plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("revenue_chart.png")
plt.show()


# QUANTITY CHART

product_quantity.plot(
    kind="bar",
    color="orange",
    title="Quantity Sold by Product"
)

plt.xlabel("Product")
plt.ylabel("Quantity")
plt.tight_layout()
plt.savefig("quantity_chart.png")
plt.show()

# SAVE VALID AND INVALID DATA

valid.to_csv("valid_sales_data.csv", index=False)
invalid.to_csv("invalid_sales_data.csv", index=False)

print("\nPROJECT COMPLETED SUCCESSFULLY!")