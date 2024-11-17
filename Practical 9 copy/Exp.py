import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import shutil

# File name
CSV_FILE = 'expenses2.csv'
BACKUP_FOLDER = 'backup/'

# Function to log an expense
def log_expense():
    name = input("Enter your name: ")
    date = input("Enter the date (YYYY-MM-DD): ")
    description = input("Enter description of the expense: ")
    amount = float(input("Enter the amount spent: "))
    category = input("Enter the category (e.g., groceries, utilities, entertainment): ")

    # Append to CSV file
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, date, description, amount, category])

    print("Expense logged successfully.")

# Function to initialize CSV file if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Date', 'Description', 'Amount', 'Category'])

# Function for expense analysis
def analyze_expenses():
    df = pd.read_csv(CSV_FILE)
    total_expenses = df.groupby('Name')['Amount'].sum()
    average_daily_expense = df['Amount'].sum() / df['Date'].nunique()

    print("\nTotal expenses by family member:")
    print(total_expenses)
    print(f"\nAverage daily expense for the household: ${average_daily_expense:.2f}")

# Function to show expense trends
def plot_expense_trends():
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    last_month = df[df['Date'] >= (datetime.now() - pd.DateOffset(days=30))]
    daily_expense = last_month.groupby('Date')['Amount'].sum().cumsum()

    plt.figure(figsize=(10, 6))
    daily_expense.plot(kind='line', marker='o')
    plt.title('Expense Trends Over Last Month')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Expenses')
    plt.grid()
    plt.show()

# Function for categorizing expenses and monthly report
def monthly_expense_report():
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    current_month = df[df['Date'].dt.month == datetime.now().month]
    
    total_by_member = current_month.groupby('Name')['Amount'].sum()
    print("\nTotal expenses for each family member this month:")
    print(total_by_member)

    expenses_by_category = current_month.groupby('Category')['Amount'].sum()
    print("\nExpense breakdown by category:")
    print(expenses_by_category)

    # Monthly comparison
    monthly_totals = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
    monthly_totals.plot(kind='bar', color='skyblue', figsize=(10, 6))
    plt.title('Monthly Expenses Comparison')
    plt.xlabel('Month')
    plt.ylabel('Total Expenses')
    plt.show()

# Function for setting and checking budget
def set_and_check_budget():
    budget = {}
    while True:
        category = input("Enter category for budget (or 'done' to finish): ")
        if category.lower() == 'done':
            break
        amount = float(input(f"Enter budget amount for {category}: "))
        budget[category] = amount

    df = pd.read_csv(CSV_FILE)
    current_month = df[df['Date'].str.startswith(datetime.now().strftime('%Y-%m'))]
    expenses_by_category = current_month.groupby('Category')['Amount'].sum()

    for category, amount in budget.items():
        spent = expenses_by_category.get(category, 0)
        remaining = amount - spent
        if remaining < 0:
            print(f"Warning: Over budget in {category} by ${-remaining:.2f}")
        else:
            print(f"Remaining budget for {category}: ${remaining:.2f}")

# Function for backup and restore
def backup_data():
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    backup_file = os.path.join(BACKUP_FOLDER, f'expenses_backup_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv')
    shutil.copy(CSV_FILE, backup_file)
    print(f"Data backed up successfully to {backup_file}")

def restore_data():
    backups = sorted([f for f in os.listdir(BACKUP_FOLDER) if f.startswith('expenses_backup')], reverse=True)
    if not backups:
        print("No backup files found.")
        return

    print("Available backups:")
    for idx, backup in enumerate(backups, 1):
        print(f"{idx}. {backup}")
    
    choice = int(input("Enter the number of the backup to restore: ")) - 1
    backup_file = os.path.join(BACKUP_FOLDER, backups[choice])
    shutil.copy(backup_file, CSV_FILE)
    print(f"Data restored successfully from {backup_file}")

# Main program loop
def main():
    initialize_csv()

    while True:
        print("\nExpense Management System")
        print("1. Log Expense")
        print("2. Analyze Expenses")
        print("3. Show Expense Trends")
        print("4. Monthly Expense Report")
        print("5. Set and Check Budget")
        print("6. Backup Data")
        print("7. Restore Data")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            log_expense()
        elif choice == '2':
            analyze_expenses()
        elif choice == '3':
            plot_expense_trends()
        elif choice == '4':
            monthly_expense_report()
        elif choice == '5':
            set_and_check_budget()
        elif choice == '6':
            backup_data()
        elif choice == '7':
            restore_data()
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
