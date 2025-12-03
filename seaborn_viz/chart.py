# chart.py
# Generates a Seaborn scatterplot for Customer LTV vs Acquisition Cost
# Saves chart.png at 512x512 px
# Author: Rahul Kumar
# Email: 24f2001869@ds.study.iitm.ac.in

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

np.random.seed(123)

# Generate realistic synthetic customer cohort data
n = 600
# Acquisition cost in USD: skewed positive distribution
acquisition_cost = np.random.gamma(shape=2.0, scale=30.0, size=n) + np.random.normal(0, 5, n)

# Lifetime value: positively related to acquisition cost with noise
ltv = acquisition_cost * np.random.normal(3.5, 0.7, n) + np.random.normal(0, 200, n)

# Clean and clip values to reasonable business ranges
acquisition_cost = np.clip(acquisition_cost, 5, 1000)
ltv = np.clip(ltv, 50, 20000)

segments = np.random.choice(["Retail", "SMB", "Enterprise"], size=n, p=[0.6, 0.3, 0.1])

df = pd.DataFrame({
    "Acquisition_Cost": acquisition_cost,
    "Customer_LTV": ltv,
    "Segment": segments
})

# Seaborn styling
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=0.9)
palette = {"Retail": "#1f77b4", "SMB": "#ff7f0e", "Enterprise": "#2ca02c"}

# Create figure 512x512 px: 8 inches * 64 dpi
plt.figure(figsize=(8, 8), dpi=64)
ax = sns.scatterplot(
    data=df,
    x="Acquisition_Cost",
    y="Customer_LTV",
    hue="Segment",
    palette=palette,
    alpha=0.75,
    edgecolor="w",
    linewidth=0.4,
    s=70,
)

# Add a global regression line (no scatter)
sns.regplot(
    data=df,
    x="Acquisition_Cost",
    y="Customer_LTV",
    scatter=False,
    ax=ax,
    line_kws={"color": "black", "lw": 1.2, "alpha": 0.7},
)

ax.set_title("Customer Lifetime Value vs Acquisition Cost", pad=14)
ax.set_xlabel("Acquisition Cost (USD)")
ax.set_ylabel("Customer Lifetime Value (USD)")
ax.legend(title="Segment", loc="upper left", frameon=True)

plt.tight_layout()

# Save as specified
plt.savefig("chart.png", dpi=64, bbox_inches="tight")
plt.close()

# Ensure final image is exactly 512x512 pixels
img = Image.open("chart.png")
if img.size != (512, 512):
    img = img.resize((512, 512), Image.LANCZOS)
    img.save("chart.png")

print("Saved: chart.png (512x512)")
