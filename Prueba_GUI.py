import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any

DATA_FILE = "expenses.json"


class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Seguimiento de Gastos")
        self.root.geometry("1000x600")
        self.root.configure(bg='#2c3e50')

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Frame de entrada de datos
        input_frame = ttk.LabelFrame(main_frame, text="Agregar Nuevo Gasto", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Campos de entrada
        ttk.Label(input_frame, text="Descripción:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.desc_entry = ttk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=0, column=1, padx=(0, 10))

        ttk.Label(input_frame, text="Monto:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=3, padx=(0, 10))

        ttk.Label(input_frame, text="Categoría:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.category_combo = ttk.Combobox(input_frame, width=15, values=[
            "General", "Comida", "Transporte", "Entretenimiento",
            "Hogar", "Salud", "Educación", "Otros"
        ])
        self.category_combo.set("General")
        self.category_combo.grid(row=0, column=5)

        # Botones de acción
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=6, padx=(10, 0))

        ttk.Button(button_frame, text="Agregar", command=self.add_expense).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Limpiar", command=self.clear_fields).pack(side=tk.LEFT)

        # Treeview para mostrar gastos
        tree_frame = ttk.LabelFrame(main_frame, text="Gastos Registrados", padding="10")
        tree_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = ('id', 'date', 'description', 'amount', 'category')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        # Definir columnas
        self.tree.heading('id', text='ID')
        self.tree.heading('date', text='Fecha')
        self.tree.heading('description', text='Descripción')
        self.tree.heading('amount', text='Monto')
        self.tree.heading('category', text='Categoría')

        self.tree.column('id', width=50)
        self.tree.column('date', width=100)
        self.tree.column('description', width=200)
        self.tree.column('amount', width=100)
        self.tree.column('category', width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Frame de controles
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Botones de control
        ttk.Button(control_frame, text="Eliminar Seleccionado", command=self.delete_selected).pack(side=tk.LEFT,
                                                                                                   padx=(0, 5))
        ttk.Button(control_frame, text="Editar Seleccionado", command=self.edit_selected).pack(side=tk.LEFT,
                                                                                               padx=(0, 5))

        # Frame de resumen y exportación
        summary_frame = ttk.LabelFrame(main_frame, text="Resumen y Exportación", padding="10")
        summary_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Resumen
        ttk.Label(summary_frame, text="Resumen por mes:").grid(row=0, column=0, sticky=tk.W)
        self.month_combo = ttk.Combobox(summary_frame, width=15, values=[
            "Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.month_combo.set("Todos")
        self.month_combo.grid(row=0, column=1, padx=(5, 10))

        ttk.Button(summary_frame, text="Mostrar Resumen", command=self.show_summary).grid(row=0, column=2, padx=(0, 10))

        self.summary_label = ttk.Label(summary_frame, text="Total: $0.00", font=('Arial', 12, 'bold'))
        self.summary_label.grid(row=0, column=3, padx=(0, 20))

        # Botones de exportación
        ttk.Button(summary_frame, text="Exportar a CSV", command=self.export_to_csv).grid(row=0, column=4)
        ttk.Button(summary_frame, text="Exportar a JSON", command=self.export_to_json).grid(row=0, column=5,
                                                                                            padx=(5, 0))

        # Bind double click para editar
        self.tree.bind('<Double-1>', self.on_double_click)

    def load_data(self):
        """Cargar datos y actualizar treeview"""
        self.expenses = self.load_expenses()
        self.update_treeview()

    def load_expenses(self) -> List[Dict[str, Any]]:
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_expenses(self, expenses: List[Dict[str, Any]]) -> None:
        with open(DATA_FILE, 'w') as f:
            json.dump(expenses, f, indent=2)

    def update_treeview(self):
        """Actualizar el treeview con los datos actuales"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in self.expenses:
            self.tree.insert('', 'end', values=(
                expense['id'],
                expense['date'],
                expense['description'],
                f"${expense['amount']:.2f}",
                expense['category']
            ))

    def clear_fields(self):
        """Limpiar campos de entrada"""
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("General")

    def add_expense(self):
        """Agregar nuevo gasto"""
        description = self.desc_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_combo.get()

        if not description:
            messagebox.showerror("Error", "La descripción es obligatoria")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "El monto debe ser positivo")
                return
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
            return

        # Crear nuevo gasto
        new_id = max([expense['id'] for expense in self.expenses], default=0) + 1
        new_expense = {
            'id': new_id,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'description': description,
            'amount': amount,
            'category': category
        }

        self.expenses.append(new_expense)
        self.save_expenses(self.expenses)
        self.update_treeview()
        self.clear_fields()

        messagebox.showinfo("Éxito", f"Gasto agregado exitosamente (ID: {new_id})")

    def delete_selected(self):
        """Eliminar gasto seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un gasto para eliminar")
            return

        item = selected[0]
        expense_id = self.tree.item(item)['values'][0]

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este gasto?"):
            self.expenses = [exp for exp in self.expenses if exp['id'] != expense_id]
            self.save_expenses(self.expenses)
            self.update_treeview()
            messagebox.showinfo("Éxito", "Gasto eliminado exitosamente")

    def edit_selected(self):
        """Editar gasto seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un gasto para editar")
            return

        self.on_double_click(None)

    def on_double_click(self, event):
        """Manejar doble clic para editar"""
        selected = self.tree.selection()
        if not selected:
            return

        item = selected[0]
        values = self.tree.item(item)['values']
        expense_id = values[0]

        # Encontrar el gasto
        expense = next((exp for exp in self.expenses if exp['id'] == expense_id), None)
        if not expense:
            return

        # Crear ventana de edición
        self.edit_window(expense)

    def edit_window(self, expense):
        """Ventana para editar gasto"""
        window = tk.Toplevel(self.root)
        window.title("Editar Gasto")
        window.geometry("400x200")
        window.transient(self.root)
        window.grab_set()

        ttk.Label(window, text="Descripción:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        desc_entry = ttk.Entry(window, width=30)
        desc_entry.insert(0, expense['description'])
        desc_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(window, text="Monto:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        amount_entry = ttk.Entry(window, width=15)
        amount_entry.insert(0, str(expense['amount']))
        amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        ttk.Label(window, text="Categoría:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        category_combo = ttk.Combobox(window, width=15, values=[
            "General", "Comida", "Transporte", "Entretenimiento",
            "Hogar", "Salud", "Educación", "Otros"
        ])
        category_combo.set(expense['category'])
        category_combo.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        def save_changes():
            description = desc_entry.get().strip()
            amount_str = amount_entry.get().strip()
            category = category_combo.get()

            if not description:
                messagebox.showerror("Error", "La descripción es obligatoria")
                return

            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "El monto debe ser positivo")
                    return
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido")
                return

            # Actualizar gasto
            expense['description'] = description
            expense['amount'] = amount
            expense['category'] = category

            self.save_expenses(self.expenses)
            self.update_treeview()
            window.destroy()
            messagebox.showinfo("Éxito", "Gasto actualizado exitosamente")

        button_frame = ttk.Frame(window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Guardar", command=save_changes).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancelar", command=window.destroy).pack(side=tk.LEFT)

    def show_summary(self):
        """Mostrar resumen de gastos"""
        selected_month = self.month_combo.get()

        if selected_month == "Todos":
            filtered_expenses = self.expenses
            total = sum(exp['amount'] for exp in filtered_expenses)
            self.summary_label.config(text=f"Total: ${total:.2f}")
        else:
            month_num = self.month_combo.current()
            filtered_expenses = [
                exp for exp in self.expenses
                if datetime.strptime(exp['date'], "%Y-%m-%d").month == month_num
            ]
            total = sum(exp['amount'] for exp in filtered_expenses)
            self.summary_label.config(text=f"Total {selected_month}: ${total:.2f}")

    def export_to_csv(self):
        """Exportar gastos a CSV"""
        if not self.expenses:
            messagebox.showwarning("Advertencia", "No hay gastos para exportar")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar como CSV"
        )

        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['id', 'date', 'description', 'amount', 'category'])
                    writer.writeheader()
                    writer.writerows(self.expenses)

                messagebox.showinfo("Éxito", f"Gastos exportados a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    def export_to_json(self):
        """Exportar gastos a JSON"""
        if not self.expenses:
            messagebox.showwarning("Advertencia", "No hay gastos para exportar")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Guardar como JSON"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.expenses, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Éxito", f"Gastos exportados a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")


def main():
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()