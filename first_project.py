import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Theme
plt.style.use("default")

# Load Data

df = pd.read_csv("phone search.csv")

df = df.dropna(subset=[
    "product_price",
    "product_num_ratings",
    "product_star_rating",
    "sales_volume",
    "product_availability"
])

# Data Cleaning

def clean_sales_volume(x):
    if pd.isna(x):
        return np.nan

    s = str(x).lower().replace(",", "").replace("+", "")

    for word in ["bought", "sold", "orders", "items",
                 "in past month", "in past year",
                 "list:", "typical:", "more buying choices"]:
        s = s.replace(word, "")

    s = s.strip()

    m = re.search(r"(\d+(?:\.\d+)?)(?:[-–](\d+(?:\.\d+)?))?\s*([km]?)", s)
    if not m:
        return np.nan

    n1 = float(m.group(1))
    n2 = m.group(2)
    unit = m.group(3)

    base = (n1 + float(n2)) / 2 if n2 else n1

    if unit == "k":
        base *= 1000
    elif unit == "m":
        base *= 1_000_000

    return base


def clean_price(x):
    if pd.isna(x):
        return np.nan
    s = re.sub(r"[^\d\.]", "", str(x))
    return float(s) if s else np.nan


def clean_availability(x):
    if pd.isna(x):
        return np.nan

    s = str(x).lower()

    if "out of stock" in s:
        return 0

    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else np.nan


df["sales_volume_numeric"] = df["sales_volume"].apply(clean_sales_volume)
df["product_price_numeric"] = df["product_price"].apply(clean_price)
df["availability_numeric"] = df["product_availability"].apply(clean_availability)

df_plotable = df.dropna(subset=[
    "sales_volume_numeric",
    "product_price_numeric",
    "availability_numeric"
])

# Brand + Model

def extract_brand_model(title):
    if pd.isna(title):
        return "UNKNOWN"

    t = re.sub(r"[,\-_|(){}\[\]]+", " ", str(title))
    words = t.split()

    if len(words) < 2:
        return words[0]

    brand = words[0].capitalize()

    stop_words = {"gb", "ram", "5g", "4g", "dual", "sim",
                  "case", "cover", "camera", "battery"}

    model_parts = []

    for w in words[1:10]:
        if w.lower() in stop_words:
            break
        model_parts.append(w)
        if len(model_parts) >= 3:
            break

    return f"{brand} {' '.join(model_parts)}"


df_plotable["brand_model"] = df_plotable["product_title"].apply(extract_brand_model)

# Color Function (3 Levels)

def get_color(value, low, high):
    if value <= low:
        return "red"
    elif value <= high:
        return "orange"
    else:
        return "green"

# Calculations

df_sorted = df_plotable.sort_values("product_price_numeric")

best_selling = (
    df_plotable.groupby("brand_model")["sales_volume_numeric"]
    .sum().sort_values(ascending=False).head(10)
)

df_plotable["weighted_rating"] = (
    df_plotable["product_star_rating"] *
    np.log1p(df_plotable["product_num_ratings"])
)

best_reviewed = (
    df_plotable.groupby("brand_model")["weighted_rating"]
    .mean().sort_values(ascending=False).head(10)
)

low_stock = df_plotable[df_plotable["availability_numeric"] <= 10]
low_stock_sorted = low_stock.sort_values("availability_numeric")

df_plotable["popularity_score"] = (
    df_plotable["product_star_rating"] *
    np.log1p(df_plotable["sales_volume_numeric"])
)

upcoming_popular = df_plotable.sort_values(
    "popularity_score", ascending=False
).head(10)

# 1. Price vs Sales

plt.figure(figsize=(12, 6))
plt.plot(
    df_sorted["product_price_numeric"],
    df_sorted["sales_volume_numeric"],
    color="green",
    linewidth=2
)

plt.title("Price vs Sales Volume")
plt.xlabel("Price ($)")
plt.ylabel("Sales Volume")
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("Price Vs Sales.png", dpi=300)
plt.show()

input("Press Enter to continue...")

# 2. Best Selling Models

low_q = best_selling.quantile(0.33)
high_q = best_selling.quantile(0.66)

colors1 = [get_color(v, low_q, high_q) for v in best_selling.values]

plt.figure(figsize=(12, 6))
plt.barh(best_selling.index, best_selling.values, color=colors1)
plt.gca().invert_yaxis()

plt.title("Top 10 Best Selling Models")
plt.xlabel("Sales Volume")
plt.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("Best Selling Models.png", dpi=300)
plt.show()

input("Press Enter to continue...")

# 3. Best Reviewed Models

low_q = best_reviewed.quantile(0.33)
high_q = best_reviewed.quantile(0.66)

colors2 = [get_color(v, low_q, high_q) for v in best_reviewed.values]

plt.figure(figsize=(12, 6))
plt.barh(best_reviewed.index, best_reviewed.values, color=colors2)
plt.gca().invert_yaxis()

plt.title("Top 10 Best Reviewed")
plt.xlabel("Weighted Rating")
plt.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("Best Reviewed.png", dpi=300)
plt.show()

input("Press Enter to continue...")

# 4. Low Stock

colors3 = [get_color(v, 3, 7) for v in low_stock_sorted["availability_numeric"]]

plt.figure(figsize=(12, 8))
plt.barh(low_stock_sorted["brand_model"],
         low_stock_sorted["availability_numeric"],
         color=colors3)

plt.gca().invert_yaxis()

plt.title("Low Stock Models (≤10 Units)")
plt.xlabel("Stock Quantity")
plt.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("Low Stock Models.png", dpi=300)
plt.show()

input("Press Enter to continue...")

# 5. Popular Models

low_q = upcoming_popular["popularity_score"].quantile(0.33)
high_q = upcoming_popular["popularity_score"].quantile(0.66)

colors4 = [
    get_color(v, low_q, high_q)
    for v in upcoming_popular["popularity_score"]
]

plt.figure(figsize=(12, 6))
plt.barh(upcoming_popular["brand_model"],
         upcoming_popular["popularity_score"],
         color=colors4)

plt.gca().invert_yaxis()

plt.title("Popular Phones")
plt.xlabel("Popularity Score")
plt.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("Popular Models.png", dpi=300)
plt.show()


