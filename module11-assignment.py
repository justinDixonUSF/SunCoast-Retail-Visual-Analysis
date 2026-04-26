# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# (DATA CREATION CODE UNCHANGED ABOVE...)

# TODO 1: Time Series Visualization
def plot_quarterly_sales_trend():
    ## Group total sales by quarter
    sales_trend = sales_df.groupby('QuarterLabel')['Sales'].sum()

    ## Create figure
    fig, ax = plt.subplots()

    ## Plot line chart
    ax.plot(sales_trend.index, sales_trend.values, marker='o')

    ## Add labels and formatting
    ax.set_title("Total Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    ax.grid(True)

    plt.xticks(rotation=45)
    return fig


def plot_location_sales_comparison():
    ## Group sales by quarter and location
    grouped = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()

    fig, ax = plt.subplots()

    ## Plot each location line
    for location in grouped.columns:
        ax.plot(grouped.index, grouped[location], marker='o', label=location)

    ax.set_title("Quarterly Sales by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    ax.legend()
    ax.grid(True)

    plt.xticks(rotation=45)
    return fig


# TODO 2: Categorical Comparison
def plot_category_performance_by_location():
    ## Filter most recent quarter
    latest = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']

    ## Pivot table for grouped bar chart
    pivot = latest.pivot_table(index='Category', columns='Location', values='Sales', aggfunc='sum')

    fig, ax = plt.subplots()

    ## Plot grouped bars
    pivot.plot(kind='bar', ax=ax)

    ax.set_title("Category Performance by Location (Q4 2023)")
    ax.set_ylabel("Sales")
    plt.xticks(rotation=45)

    return fig


def plot_sales_composition_by_location():
    ## Group sales
    grouped = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()

    ## Convert to percentage
    percent = grouped.div(grouped.sum(axis=1), axis=0)

    fig, ax = plt.subplots()

    ## Stacked bar chart
    percent.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title("Sales Composition by Location")
    ax.set_ylabel("Percentage")

    return fig


# TODO 3: Relationship Analysis
def plot_ad_spend_vs_sales():
    fig, ax = plt.subplots()

    ## Scatter plot
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.6)

    ## Best-fit line
    z = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    p = np.poly1d(z)
    ax.plot(sales_df['AdSpend'], p(sales_df['AdSpend']), color='red')

    ax.set_title("Ad Spend vs Sales")
    ax.set_xlabel("Ad Spend")
    ax.set_ylabel("Sales")

    return fig


def plot_ad_efficiency_over_time():
    ## Group efficiency by quarter
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()

    fig, ax = plt.subplots()

    ax.plot(efficiency.index, efficiency.values, marker='o')

    ax.set_title("Advertising Efficiency Over Time")
    ax.set_ylabel("Sales per Dollar Spent")
    ax.grid(True)

    plt.xticks(rotation=45)
    return fig


# TODO 4: Distribution Analysis
def plot_customer_age_distribution():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    ## Overall distribution
    axes[0, 0].hist(customer_df['Age'], bins=20)
    axes[0, 0].set_title("Overall Age Distribution")

    ## Mean & median lines
    axes[0, 0].axvline(customer_df['Age'].mean(), color='red')
    axes[0, 0].axvline(customer_df['Age'].median(), color='green')

    ## By location
    for ax, location in zip(axes.flatten()[1:], customer_df['Location'].unique()):
        subset = customer_df[customer_df['Location'] == location]
        ax.hist(subset['Age'], bins=15)
        ax.set_title(location)

    return fig


def plot_purchase_by_age_group():
    ## Create age groups
    bins = [18, 30, 45, 60, 80]
    labels = ['18-30', '31-45', '46-60', '61+']
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels)

    fig, ax = plt.subplots()

    ## Boxplot
    customer_df.boxplot(column='PurchaseAmount', by='AgeGroup', ax=ax)

    ax.set_title("Purchase Amount by Age Group")
    plt.suptitle("")  # remove default title

    return fig


# TODO 5: Sales Distribution
def plot_purchase_amount_distribution():
    fig, ax = plt.subplots()

    ## Histogram
    ax.hist(customer_df['PurchaseAmount'], bins=20)

    ax.set_title("Purchase Amount Distribution")

    return fig


def plot_sales_by_price_tier():
    ## Count by tier
    counts = customer_df['PriceTier'].value_counts()

    ## Explode largest slice
    explode = [0.1 if i == counts.idxmax() else 0 for i in counts.index]

    fig, ax = plt.subplots()

    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', explode=explode)

    ax.set_title("Sales by Price Tier")

    return fig


# TODO 6: Market Share
def plot_category_market_share():
    counts = sales_df.groupby('Category')['Sales'].sum()

    explode = [0.1 if i == counts.idxmax() else 0 for i in counts.index]

    fig, ax = plt.subplots()

    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', explode=explode)

    ax.set_title("Category Market Share")

    return fig


def plot_location_sales_distribution():
    counts = sales_df.groupby('Location')['Sales'].sum()

    fig, ax = plt.subplots()

    ax.pie(counts, labels=counts.index, autopct='%1.1f%%')

    ax.set_title("Sales by Location")

    return fig


# TODO 7: Dashboard
def create_business_dashboard():
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    ## 1: Sales trend
    sales_trend = sales_df.groupby('QuarterLabel')['Sales'].sum()
    axes[0, 0].plot(sales_trend.index, sales_trend.values)
    axes[0, 0].set_title("Sales Trend")

    ## 2: Ad efficiency
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()
    axes[0, 1].plot(efficiency.index, efficiency.values)
    axes[0, 1].set_title("Ad Efficiency")

    ## 3: Category share
    cat = sales_df.groupby('Category')['Sales'].sum()
    axes[1, 0].pie(cat, labels=cat.index, autopct='%1.1f%%')

    ## 4: Location share
    loc = sales_df.groupby('Location')['Sales'].sum()
    axes[1, 1].pie(loc, labels=loc.index, autopct='%1.1f%%')

    fig.suptitle("SunCoast Retail Dashboard")

    return fig


# Main function
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    fig13 = create_business_dashboard()

    ## Business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    print("- Sales peak in Q4 due to seasonal demand.")
    print("- Miami consistently generates the highest sales.")
    print("- Electronics dominate category performance.")
    print("- Positive correlation between ad spend and sales.")
    print("- Mid-range products drive most purchases.")
    print("- Customer demographics vary significantly by location.")

    plt.show()


if __name__ == "__main__":
    main()