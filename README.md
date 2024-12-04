# Expense Tracker CLI

A simple command-line application to manage your finances. The Expense Tracker allows you to add, update, delete, and view expenses. It also provides summaries of your expenses and features budgeting capabilities.
https://roadmap.sh/projects/expense-tracker
## Features

- Add an expense with a description and amount.
- Update an existing expense.
- Delete an expense by its ID.
- List all expenses or specific ones by their IDs.
- View a summary of total expenses.
- View monthly or yearly expense summaries.
- Set a monthly budget and get warnings when exceeding it.
- Export expenses to a CSV file for external use.

## Requirements

- Python 3.9
- `pandas` library for CSV export

## Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```bash
   pip install pandas
    ```
   
## Usage

Run the application using the command line:
Commands and Examples
Add an Expense
```bash
$ expense-tracker add --description "Lunch" --amount 20
Expense added successfully
```
Update an Expense
```bash
$ expense-tracker update --id 1 --description "Dinner" --amount 15
Expense 1 updated successfully
```
Delete an Expense
```bash
$ expense-tracker delete --id 1
Expense deleted successfully
```
List All Expenses
```bash
$ expense-tracker list --all
```
List specific expenses by IDs:
```bash
$ expense-tracker list --ids 1 2
```
Summary of all expenses:
```bash
$ expense-tracker summary --all
```
Summary of monthly expenses:
```bash
$ expense-tracker summary --month 8
```
summary of yearly expenses:
```bash
$ expense-tracker summary --year 2024
```
Set a Budget
```bash
$ expense-tracker setbudget 500
Budget set successfully
```
Export Expenses
```bash
$ expense-tracker export expenses.csv
Expenses exported successfully
```
File Storage

    Expenses are stored in expenses.json.
    Budgets are stored as part of the same JSON structure.

Error Handling

    Handles invalid inputs such as negative amounts or non-existent IDs.
    Provides warnings when an expense exceeds the set budget.