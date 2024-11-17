import pandas as pd
import matplotlib.pyplot as plt
import shutil
import os

# Path to your main CSV file and backup location
input_file = r"C:\Data\workspace\Advance Python\Practical 9\expenses2.csv"
backup_file = r"C:\Data\workspace\Advance Python\Practical 9\expenses_backup.csv"

# Function to create a backup of the CSV file
def backup_csv():
    try:
        shutil.copy(input_file, backup_file)
        print("Backup created successfully.")
    except FileNotFoundError:
        print("Original file not found. Cannot create backup.")
    except Exception as e:
        print(f"An error occurred while creating backup: {e}")

# Function to restore the CSV file from backup
def restore_csv():
    try:
        if os.path.exists(backup_file):
            shutil.copy(backup_file, input_file)
            print("Data restored from backup successfully.")
        else:
            print("Backup file not found. Unable to restore.")
    except Exception as e:
        print(f"An error occurred while restoring backup: {e}")

# Read the CSV file into a DataFrame
try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print("The file is missing. Attempting to restore from backup...")
    restore_csv()
    df = pd.read_csv(input_file)

# Display the DataFrame
print("Initial DataFrame:")
print(df)

# Check for null values and replace them with 0 in the 'Amount' column
df['Amount'] = df['Amount'].fillna(0)

# Check if 'Category' column exists, if not, add one
if 'Category' not in df.columns:
    df['Category'] = None  # Initialize with None or empty values
    print("\n'Category' column not found. Adding a new 'Category' column.")

# Prompt the user to assign a category for each expense entry without a category
for index, row in df.iterrows():
    if pd.isna(row['Category']) or row['Category'] == "":  # Check for NaN or empty string
        print(f"\nExpense Entry:\nDate: {row['Date']}\nAmount: {row['Amount']}\nName: {row['Name']}")
        category = input("Please enter a category for this expense (e.g., groceries, utilities, entertainment): ")
        df.at[index, 'Category'] = category  # Update the DataFrame with the entered category
        print(f"Assigned Category: {category} for expense on {row['Date']}")

# Save the updated DataFrame back to the CSV file
df.to_csv(input_file, index=False)
print("\nCSV file updated with categories.")

# Convert 'Date' column to datetime if it's not already in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Create a new 'Month-Year' column for grouping by month and year
df['Month-Year'] = df['Date'].dt.to_period('M')

# Group by 'Category' and 'Month-Year' and calculate the sum of 'Amount'
monthly_category_expenses = df.groupby(['Month-Year', 'Category'])['Amount'].sum().unstack(fill_value=0)

# Prompt user to enter a monthly budget for each category
print("Set your monthly budget for each category:")
monthly_budget = {}
for category in df['Category'].unique():
    monthly_budget_input = input(f"Enter your monthly budget for {category}: ")
    monthly_budget[category] = float(monthly_budget_input)

print("\nYour monthly budget for each category:")
print(monthly_budget)

# Calculate remaining budget for each category by month and check for overspending
remaining_monthly_budget = monthly_category_expenses.copy()
for category in monthly_budget:
    remaining_monthly_budget[category] = monthly_budget[category] - monthly_category_expenses[category]

print("\nRemaining budget by month and category:")
print(remaining_monthly_budget)

# Check for overspending and alert the user
for month, expenses in remaining_monthly_budget.iterrows():
    for category, remaining in expenses.items():
        if remaining < 0:
            print(f"\nWarning: Budget exceeded for {category} in {month}. You overspent by {-remaining:.2f}.")

# Visualize the monthly budget vs. expenses
for month in monthly_category_expenses.index:
    plt.figure(figsize=(10, 6))
    monthly_data = monthly_category_expenses.loc[month]
    budget_data = pd.Series(monthly_budget).reindex(monthly_data.index)

    # Plotting the budget vs expenses for each category
    plt.bar(monthly_data.index, budget_data, width=0.4, label='Budget', color='lightgreen', align='center')
    plt.bar(monthly_data.index, monthly_data, width=0.4, label='Expenses', color='tomato', align='edge')

    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.title(f'Budget vs. Expenses for {month}')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

# Backup the file after updates
backup_csv()
