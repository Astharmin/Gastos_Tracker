# 💰 ExpenseTracker - Gestor de Gastos Personal

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-%23039BE5?logo=tkinter)
![JSON](https://img.shields.io/badge/Data-JSON-000000?logo=json)
![Executable](https://img.shields.io/badge/Windows-Executable-0078D6?logo=windows)
![License](https://img.shields.io/badge/Licencia-MIT-green)

> *"Ahora con interfaz gráfica y ejecutable - Gestión de gastos fácil y visual"*

## 🌟 Nuevas Características (GUI Edition)

- 🖼️ **Interfaz gráfica moderna** con Tkinter
- 🚀 **Ejecutable nativo** (no necesita Python instalado)
- 📊 **Tabla visual** de gastos registrados
- 🗑️ **Eliminación con selección** (sin recordar IDs)
- 📅 **Filtrado por mes** integrado en la UI
- 💾 **Exportación a CSV/JSON** desde botones

## 🎯 Modos de Uso

```bash
# Clonar y usar
git clone https://github.com/tuusuario/Gestos_Tracker.git

cd Gastos_Tracker

python main.py --help
```
## 😴 Guia de uso para vagos 
```bash
# Agregar gastos
python main.py add --description "Supermercado" --amount 45.30 --category "Comida"
python main.py add --description "Gasolina" --amount 25.00 --category "Transporte"

# Ver y gestionar
python main.py list
python main.py delete --id 2
python main.py update --id 3 --amount 15.75
python main.py summary --month 11
python main.py export

# O ejecutar directamente el .exe
ExpenseTracker.exe  # ¡Sin necesidad de Python!
```

https://roadmap.sh/projects/expense-tracker
