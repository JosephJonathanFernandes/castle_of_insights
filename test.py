import pandas as pd

# Load retained employee data from optimization_analysis.xlsx
file = 'optimization_analysis.xlsx'
retained = pd.read_excel(file, sheet_name='Retained_Employees')

# Overall stats
stats = {
    'Total retained': retained['Employee_ID'].count(),
    'Average salary': retained['Salary'].mean(),
    'Total salary': retained['Salary'].sum(),
    'Average estimated output': retained['output_est'].mean(),
    'Total estimated output': retained['output_est'].sum(),
    'Average output per cost': retained['output_per_cost'].mean()
}

# Company split
company_counts = retained['Company_Origin'].value_counts()

# Work rating distribution
rating_counts = retained['Work_Rating'].value_counts()

# Tenure / Seniority
senior_count = retained['senior'].sum()
experienced_count = retained['experienced'].sum()
senior_pct = 100 * senior_count / stats['Total retained']
experienced_pct = 100 * experienced_count / stats['Total retained']

# Department-level summary
department_summary = retained.groupby('Department').agg({
    'Employee_ID':'count',
    'Company_Origin':lambda x: (x=='Technova').sum(),
    'Tenure':lambda x: (x>=15).sum(),
    'Work_Rating':lambda x: (x=='A').sum(),
    'Salary':'sum',
    'output_est':'sum'
}).reset_index().rename(columns={
    'Employee_ID':'TotalRetained',
    'Company_Origin':'TechnovaRetained',
    'Tenure':'Tenure15+',
    'Work_Rating':'ARated',
    'Salary':'TotalSalary',
    'output_est':'TotalOutput'
})

# Print results
print("=== Overall Statistics ===")
for k, v in stats.items():
    print(f"{k}: {v}")
print("\nCompany Split:\n", company_counts)
print("\nWork Rating Distribution:\n", rating_counts)
print(f"\n≥15 years: {senior_count} ({senior_pct:.2f}%)")
print(f"≥5 years: {experienced_count} ({experienced_pct:.2f}%)")
print("\n=== Department-wise Summary ===")
print(department_summary)
