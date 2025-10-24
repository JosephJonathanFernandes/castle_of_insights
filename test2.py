import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
df_orig = pd.read_csv('cleaned_castle_of_insights.csv')
df_new = pd.read_excel('optimization_analysis.xlsx', sheet_name='Retained_Employees')

# Standardize columns
df_orig.columns = [col.strip().replace(' ', '_') for col in df_orig.columns]
df_new.columns = [col.strip().replace(' ', '_') for col in df_new.columns]

# 1. Overall comparison plots
metrics = {
    'Total Employees': [len(df_orig), len(df_new)],
    'Total Salary': [df_orig['Salary'].sum(), df_new['Salary'].sum()],
    'Average Salary': [df_orig['Salary'].mean(), df_new['Salary'].mean()],
    'Total Output': [df_orig['output_est'].sum(), df_new['output_est'].sum()],
    'Average Output': [df_orig['output_est'].mean(), df_new['output_est'].mean()],
    'Average Output/Cost': [df_orig['output_per_cost'].mean(), df_new['output_per_cost'].mean()],
    'Tenure ≥15': [(df_orig['Tenure'] >= 15).sum(), (df_new['Tenure'] >= 15).sum()],
    'Tenure ≥5': [(df_orig['Tenure'] >= 5).sum(), (df_new['Tenure'] >= 5).sum()]
}

# Plot overall metrics
labels = list(metrics.keys())
orig_vals = [v[0] for v in metrics.values()]
new_vals = [v[1] for v in metrics.values()]

plt.figure(figsize=(10, 6))
x = range(len(labels))
plt.bar(x, orig_vals, width=0.4, label='Original')
plt.bar([i + 0.4 for i in x], new_vals, width=0.4, label='Optimized')
plt.xticks([i + 0.2 for i in x], labels, rotation=30, ha='right')
plt.ylabel('Metric Value')
plt.title('Original vs. Retained Workforce: Key Metrics')
plt.legend()
plt.tight_layout()
plt.show()

# 2. Company split pie charts
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
df_orig['Company_Origin'].value_counts().plot.pie(ax=ax[0], autopct='%1.1f%%', title='Original: Company Split')
df_new['Company_Origin'].value_counts().plot.pie(ax=ax[1], autopct='%1.1f%%', title='Retained: Company Split')
plt.tight_layout()
plt.show()

# 3. Rating distribution bar chart
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
df_orig['Work_Rating'].value_counts().plot.bar(ax=ax[0], color=['#FFD700','#C0C0C0','#673AB7'])
ax[0].set_title('Original: Ratings')
ax[0].set_ylabel('Employee Count')
df_new['Work_Rating'].value_counts().plot.bar(ax=ax[1], color=['#FFD700','#C0C0C0','#673AB7'])
ax[1].set_title('Retained: Ratings')
plt.tight_layout()
plt.show()

# 4. Departmental headcount comparison
dept_orig = df_orig['Department'].value_counts()
dept_new = df_new['Department'].value_counts()
dept_compare = pd.DataFrame({'Original':dept_orig, 'Retained':dept_new}).fillna(0)
dept_compare.plot.bar(figsize=(12,6))
plt.title('Department Size: Original vs Retained')
plt.ylabel('Number of Employees')
plt.tight_layout()
plt.show()
