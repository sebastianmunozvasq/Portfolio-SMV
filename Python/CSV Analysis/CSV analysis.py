# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 19:30:26 2025

@author: seba2
"""

#!/usr/bin/env python
# coding: utf-8

# Import Python libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('public_transportation_statistics_by_zip_code-1.csv')
df = df.dropna()
print(df.head())
print(df.describe())

# Find minimum and maximum percentages
min_value = df['public_transportation_pct'].min()
max_value = df['public_transportation_pct'].max()

print("Minimum value:", min_value)
print("Maximum value:", max_value)

# Filter out negative values if any
df = df[df['public_transportation_pct'] >= 0]
new_min_value = df['public_transportation_pct'].min()
print("New minimum value:", new_min_value)

# Segmentation by public transportation usage
# Determining the average potential sales in high-use (>10%) and low-use (<=10%) public transportation areas
high_use_zone = df[df['public_transportation_pct'] > 10]
high_use_sales = high_use_zone['public_transportation_population'].mean()
print("Average potential sales in high public transportation use areas:", high_use_sales)

low_use_zone = df[df['public_transportation_pct'] <= 10]
low_use_sales = low_use_zone['public_transportation_population'].mean()
print("Average potential sales in low public transportation use areas:", low_use_sales)

# Calculating the average in each percentage zone does not provide representative results
# because a percentage for each zip code represents a different number of people.

# Assuming potential sales equal the number of people using public transportation
high_use_sales = high_use_zone['public_transportation_population'].sum()
print("Potential sales in high public transportation use areas:", high_use_sales)

low_use_sales = low_use_zone['public_transportation_population'].sum()
print("Potential sales in low public transportation use areas:", low_use_sales)

# Histogram of public transportation usage percentage
plt.figure(figsize=(8, 6))
n, bins, patches = plt.hist(df['public_transportation_pct'], bins=20, color='red', edgecolor='black', alpha=0.7)
plt.title('Histogram of Public Transportation Usage Percentage', fontsize=12)
plt.xlabel('Public Transportation Usage Percentage', fontsize=10)
plt.ylabel('Frequency', fontsize=10)
plt.xticks(bins, rotation=90, fontsize=9)
plt.yticks(fontsize=9)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Potential sales by zip code
# Assuming potential sales equal the population using public transportation
df['potential_sales'] = df['public_transportation_population']
plt.figure(figsize=(12, 6))
plt.scatter(df['zip_code'], df['potential_sales'], alpha=0.7, color='blue', edgecolors='black')
plt.xlabel('Zip Code', fontsize=12)
plt.ylabel('Potential Sales', fontsize=12)
plt.title('Potential Sales by Zip Code', fontsize=14)
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Allows observing in which zip codes there are higher potential sales

# Extra: Potential sales by usage category
# Create public transportation usage categories
bins = [0, 5, 10, 20, 50, 100]  # Usage percentage ranges
labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
# Classify public transportation usage percentages into categories using cut
df['usage_category'] = pd.cut(df['public_transportation_pct'], bins=bins, labels=labels, include_lowest=True)

# Calculate the average number of sales per category
sales_by_category = df.groupby('usage_category')['potential_sales'].sum()
print(sales_by_category)

# Sales by usage category chart
plt.figure(figsize=(10, 6))
sales_by_category.plot(kind='bar', color='red', edgecolor='black', alpha=0.7)
plt.xlabel('Public Transportation Usage Category', fontsize=12)
plt.ylabel('Potential Sales', fontsize=12)
plt.title('Potential Sales by Public Transportation Usage Category', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Allows concluding that regardless of the public transportation usage percentage,
# high sales can be achieved because what matters is the gross number
# of people using public transportation.

# Scatter plot between public transportation usage and potential sales
plt.figure(figsize=(8, 6))
plt.scatter(df['public_transportation_population'], df['potential_sales'], alpha=0.5, color='blue', edgecolors='black')
plt.title('Relationship between Public Transportation Usage and Potential Sales', fontsize=12)
plt.xlabel('Population Using Public Transportation', fontsize=10)
plt.ylabel('Potential Sales', fontsize=10)
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Linear relationship with m=1 because it was assumed that each person using public transportation is a potential buyer

# Scatter plot between public transportation usage percentage and potential sales
plt.figure(figsize=(8, 6))
plt.scatter(df['public_transportation_pct'], df['potential_sales'], alpha=0.5, color='blue', edgecolors='black')
plt.title('Relationship between Public Transportation Usage Percentage and Potential Sales', fontsize=12)
plt.xlabel('Percentage Using Public Transportation', fontsize=10)
plt.ylabel('Potential Sales', fontsize=10)
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# No conclusion can be drawn because a specific percentage represents
# a different population size depending on the zip code.

# Export to Excel
df.to_excel('potential_sales_by_zip_code.xlsx', index=False)
