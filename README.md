# 💰 ExpenseTracker CLI - Gestor de Gastos Personales

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-CLI-4EAA25?logo=terminal)
![JSON](https://img.shields.io/badge/Data-JSON-000000?logo=json)
![License](https://img.shields.io/badge/Licencia-MIT-green)

> *"Gestor de gastos personal desde la terminal - simple, rápido y sin distracciones"*

## 🌟 Características

- ✅ **CRUD completo** (Crear, Leer, Actualizar, Eliminar gastos)
- 📊 **Resumen mensual** de gastos
- 📁 **Exportación a CSV** para análisis externos
- 🏷️ **Categorización** de gastos
- 💾 **Persistencia en JSON** (sin base de datos necesaria)
- 🐍 **100% Python puro** - cero dependencias

## 🚀 Instalación y Uso

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
```
https://roadmap.sh/projects/expense-tracker
