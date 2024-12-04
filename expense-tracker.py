import argparse
import json
from datetime import datetime
import pandas as pd



def main():

    parser = argparse.ArgumentParser(description='Expense Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Create the parser for the "setbudget" command
    setbudget_parser = subparsers.add_parser('setbudget', help='Set the budget for the month')
    setbudget_parser.add_argument('budget', type=float, help='Budget for the month')

    # Create the parser for the "add" command
    add_parser = subparsers.add_parser('add', help='Add an expense')
    add_parser.add_argument('description', type=str, help='Expense Description')
    add_parser.add_argument('amount', type=float, help='Expense Amount')

    # Create the parser for the "update" command
    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    update_parser.add_argument('id', type=int, help='Expense ID')
    update_parser.add_argument('description', type=str, help='New expense description')
    update_parser.add_argument('amount', type=float, help='New expense amount')

    # Create the parser for the "delete" command
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('id', type=int, help='Expense ID')

    # Create the parser for the "list" command
    list_parser = subparsers.add_parser('list', help='List all expenses')
    list_parser.add_argument('--all', action='store_true', help='List all expenses')
    list_parser.add_argument('--ids', type=int, nargs='+', help='List selected expenses')

    # Create the parser for the "summary" command
    summary_parser = subparsers.add_parser('summary', help='Show summary of expenses')
    summary_parser.add_argument('--month', type=int, help='Month to show summary')
    summary_parser.add_argument('--year', type=int, help='Year to show summary')
    summary_parser.add_argument('--category', type=str, help='Category to show summary')
    summary_parser.add_argument('--all', action='store_true', help='Show summary of all expenses')

    # Create a parser for the "export" command
    export_parser = subparsers.add_parser('export', help='Export expenses to a csv file')
    export_parser.add_argument('filename', type=str, help='Name of the file to export')


    args = parser.parse_args()

    if args.command == 'add':
        add_expense(args.description, args.amount)
    elif args.command == 'update':
        update_expense(args.id, args.description, args.amount)
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'list':
        list_expenses(all=args.all, ids=args.ids)
    elif args.command == 'summary':
        show_summary(month=args.month, year=args.year, category=args.category, all=args.all)
    elif args.command == 'export':
        export_expenses(args.filename)
    elif args.command == 'setbudget':
        set_budget(args.budget)
        print('Budget set successfully')


def load_expenses():
    try:
        with open('expenses.json', 'r') as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []
    return expenses

def save_expenses(expenses):
    try:
        with open('expenses.json', 'w') as file:
            json.dump(expenses, file, indent=4)
    except FileNotFoundError:
        print('Error saving expenses')
    return None

def export_expenses(filename):
    expenses = load_expenses()
    df = pd.DataFrame(expenses)
    df.to_csv(filename, index=False)
    print('Expenses exported successfully')

# def set_budget(budget):
#     with open('budget.json', 'w') as file:
#         json.dump({'budget': budget}, file)
#     return None

def set_budget(budget):
    expenses = load_expenses()
    expenses.append({'budget': budget})
    save_expenses(expenses)

def add_expense(description, amount):
    expenses = load_expenses()
    if not any('budget' in expense for expense in expenses):
            expense = {
                'id': len(expenses) + 1,
                'description': description,
                'amount': amount,
                'timestamp': datetime.now().isoformat()
            }
            expenses.append(expense)
            save_expenses(expenses)
            print('Expense added successfully')
    else:
        if sum(expense['amount'] for expense in expenses if 'budget' not in expense) + amount <= next(expense['budget'] for expense in expenses if 'budget' in expense):
            expense = {
                'id': len(expenses) + 1,
                'description': description,
                'amount': amount,
                'timestamp': datetime.now().isoformat()
            }
            expenses.append(expense)
            save_expenses(expenses)
            print('Expense added successfully')
        else:
            print('Expense exceeds budget')
            expense = {
                'id': len(expenses) + 1,
                'description': description,
                'amount': amount,
                'timestamp': datetime.now().isoformat()
            }
            expenses.append(expense)
            save_expenses(expenses)
            print('Expense added successfully')



def update_expense(expense_id, description, amount):
    expenses = load_expenses()
    for expense in expenses:
        if expense['id'] == expense_id:
            expense['description'] = description
            expense['amount'] = amount
            expense['timestamp'] = datetime.now().isoformat()
            save_expenses(expenses)
            print(f'Expense {expense_id} updated successfully')
            return None
    print(f'Expense {expense_id} not found')

def delete_expense(expense_id):
    expenses = load_expenses()
    for expense in expenses:
        if expense['id'] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            print(f'Expense {expense_id} deleted successfully')
            return None

def list_expenses(all=None, ids=None):
    expenses = load_expenses()
    for expense in expenses:
        if 'budget' not in expense:
            if all:
                    print(f"{expense['id']}: {expense['description']} - {expense['amount']} - {expense['timestamp']}")
            elif ids:
                    if expense['id'] in ids:
                        print(f"{expense['id']}: {expense['description']} - {expense['amount']} - {expense['timestamp']}")
            else:
                print('No expenses found')

def show_summary(month=None, year=None, category=None, all=None):
    expenses = load_expenses()
    if all:
        total_expense = sum([expense['amount'] for expense in expenses if 'budget' not in expense])
        print(f"The total expense is {total_expense}")
    elif year:
        total_expense = sum([expense['amount'] for expense in expenses if 'budget' not in expense and expense['timestamp'].startswith(str(year))])
        print(f"The total expense for {year} is {total_expense}")
    elif month:
        total_expense = sum([expense['amount'] for expense in expenses if 'budget' not in expense and expense['timestamp'].startswith(f'{year}-{month}')])
        print(f"The total expense for {month}/{year} is {total_expense}")
    else:
        print('No expenses found')

if __name__ == '__main__':
    main()