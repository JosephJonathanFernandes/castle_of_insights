import pandas as pd
import matplotlib.pyplot as plt

# Load the retained employees data
file = 'optimization_analysis.xlsx'
retained = pd.read_excel(file, sheet_name='Retained_Employees')

# 1. Overall stats
total_retained = retained['Employee_ID'].count()
avg_salary = retained['Salary'].mean()
total_salary = retained['Salary'].sum()
avg_output = retained['output_est'].mean()
total_output = retained['output_est'].sum()
avg_outputpercost = retained['output_per_cost'].mean()

print("Total retained:", total_retained)
print("Average salary:", avg_salary)
print("Total salary:", total_salary)
print("Average estimated output:", avg_output)
print("Total estimated output:", total_output)
print("Average output per cost:", avg_outputpercost)

# 2. Company-wise split
company_counts = retained['Company_Origin'].value_counts()
print("\nCompany Split:\n", company_counts)

# 3. Rating distribution
rating_counts = retained['Work_Rating'].value_counts()
print("\nWork Rating Distribution:\n", rating_counts)

# 4. Tenure / Seniority
senior_count = retained['senior'].sum()
experienced_count = retained['experienced'].sum()
senior_pct = 100 * senior_count / total_retained
experienced_pct = 100 * experienced_count / total_retained
print(f"\n≥15 years: {senior_count} ({senior_pct:.2f}%)")
print(f"≥5 years: {experienced_count} ({experienced_pct:.2f}%)")

# 5. Departmental summary
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
print("\nDepartment-wise summary:")
print(department_summary)

# 6. Bar Plot: Retained by Department
department_summary.plot.bar(x='Department', y='TotalRetained', legend=False)
plt.ylabel('Number of Employees')
plt.title('Employees Retained by Department')
plt.tight_layout()
plt.show()

# 7. Pie Chart: Company Split
company_counts.plot.pie(autopct='%1.1f%%', labels=company_counts.index)
plt.ylabel('')
plt.title('Company Split (Retained)')
plt.show()

# 8. Bar plot: Work Rating distribution
rating_counts.plot.bar()
plt.ylabel('Employees')
plt.title('Work Rating Distribution (Retained)')
plt.show()

# 9. Export summary to CSV (optional)
department_summary.to_csv('department_retained_summary.csv', index=False)
