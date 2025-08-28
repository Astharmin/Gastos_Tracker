import argparse
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any

DATA_FILE = "expenses.json"

def load_expenses() -> List[Dict[str, Any]]:

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_expenses(expenses: List[Dict[str, Any]]) -> None:

    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)


def add_expense(description: str, amount: float, category: str = "General") -> None:

    if amount <= 0:
        print("Error: El monto debe ser positivo")
        return

    expenses = load_expenses()

    # Crear nuevo gasto
    new_id = max([expense['id'] for expense in expenses], default=0) + 1
    new_expense = {
        'id': new_id,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'description': description,
        'amount': amount,
        'category': category
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Gasto agregado exitosamente (ID: {new_id})")


def list_expenses() -> None:

    expenses = load_expenses()

    if not expenses:
        print("No hay gastos registrados")
        return

    print("\nID  Fecha       Descripción          Monto     Categoría")
    print("-" * 60)
    for expense in expenses:
        print(
            f"{expense['id']:<3} {expense['date']} {expense['description']:<20} ${expense['amount']:<8} {expense['category']}")


def delete_expense(expense_id: int) -> None:

    expenses = load_expenses()
    original_count = len(expenses)

    expenses = [expense for expense in expenses if expense['id'] != expense_id]

    if len(expenses) == original_count:
        print(f"Error: No se encontró gasto con ID {expense_id}")
        return

    save_expenses(expenses)
    print(f"Gasto eliminado exitosamente")


def update_expense(expense_id: int, description: str = None, amount: float = None, category: str = None) -> None:

    expenses = load_expenses()

    for expense in expenses:
        if expense['id'] == expense_id:
            if description:
                expense['description'] = description
            if amount:
                if amount <= 0:
                    print("Error: El monto debe ser positivo")
                    return
                expense['amount'] = amount
            if category:
                expense['category'] = category

            save_expenses(expenses)
            print(f"Gasto actualizado exitosamente")
            return

    print(f"Error: No se encontró gasto con ID {expense_id}")


def show_summary(month: int = None) -> None:

    expenses = load_expenses()

    if not expenses:
        print("No hay gastos registrados")
        return

    if month:
        # Filtrar por mes
        filtered_expenses = [
            expense for expense in expenses
            if datetime.strptime(expense['date'], "%Y-%m-%d").month == month
        ]
        total = sum(expense['amount'] for expense in filtered_expenses)
        month_name = datetime(2024, month, 1).strftime("%B")
        print(f"Total de gastos para {month_name}: ${total:.2f}")
    else:
        # Resumen general
        total = sum(expense['amount'] for expense in expenses)
        print(f"Total de gastos: ${total:.2f}")


def export_to_csv() -> None:

    expenses = load_expenses()

    if not expenses:
        print("No hay gastos para exportar")
        return

    filename = f"expenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'date', 'description', 'amount', 'category'])
        writer.writeheader()
        writer.writerows(expenses)

    print(f"Gastos exportados exitosamente a {filename}")


def main():

    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Comando add
    add_parser = subparsers.add_parser('add', help='Agregar un nuevo gasto')
    add_parser.add_argument('--description', required=True, help='Descripción del gasto')
    add_parser.add_argument('--amount', type=float, required=True, help='Monto del gasto')
    add_parser.add_argument('--category', default='General', help='Categoría del gasto')

    # Comando list
    subparsers.add_parser('list', help='Listar todos los gastos')

    # Comando delete
    delete_parser = subparsers.add_parser('delete', help='Eliminar un gasto')
    delete_parser.add_argument('--id', type=int, required=True, help='ID del gasto a eliminar')

    # Comando update
    update_parser = subparsers.add_parser('update', help='Actualizar un gasto')
    update_parser.add_argument('--id', type=int, required=True, help='ID del gasto a actualizar')
    update_parser.add_argument('--description', help='Nueva descripción')
    update_parser.add_argument('--amount', type=float, help='Nuevo monto')
    update_parser.add_argument('--category', help='Nueva categoría')

    # Comando summary
    summary_parser = subparsers.add_parser('summary', help='Mostrar resumen de gastos')
    summary_parser.add_argument('--month', type=int, help='Mes específico (1-12)')

    # Comando export
    subparsers.add_parser('export', help='Exportar gastos a CSV')

    args = parser.parse_args()

    try:
        if args.command == 'add':
            add_expense(args.description, args.amount, args.category)
        elif args.command == 'list':
            list_expenses()
        elif args.command == 'delete':
            delete_expense(args.id)
        elif args.command == 'update':
            update_expense(args.id, args.description, args.amount, args.category)
        elif args.command == 'summary':
            show_summary(args.month)
        elif args.command == 'export':
            export_to_csv()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()