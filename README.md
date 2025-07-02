# Python-Trabajo-Final

# 📦 Inventario de Productos en Python con SQLite y Colorama

Este proyecto es una aplicación de consola desarrollada en **Python 3** que permite registrar, visualizar, modificar y eliminar productos de un inventario, utilizando una base de datos SQLite y colores personalizados para una mejor experiencia visual con **Colorama**.

---

## 🧰 Tecnologías utilizadas

- **Python 3.x** 🐍
- **SQLite** 🗂️ para almacenamiento de datos
- **Colorama** 🎨 para colorizar la terminal

---

## 🎨 Estilo y Colores con Colorama

Se usaron colores específicos para mejorar la usabilidad y estética del sistema:

| Función                           | Color `Colorama`             | Uso                                   |
|----------------------------------|------------------------------|----------------------------------------|
| Entradas del usuario             | `Fore.LIGHTGREEN_EX`         | Campos como nombre, cantidad, precio   |
| Validaciones y errores           | `Fore.RED`                   | Para mostrar errores o entradas inválidas |
| Confirmaciones o éxitos          | `Fore.GREEN`                 | Registro o actualización exitosa       |
| Preguntas de confirmación        | `Fore.YELLOW`                | Preguntar si desea eliminar un producto |
| Lista de productos eliminados    | `Fore.RED`                   | Mensaje al eliminar un producto        |
| Actualización de productos       | `Fore.LIGHTRED_EX`           | Aviso de mantener campos vacíos        |
| Listado general de productos     | `Fore.MAGENTA`               | Mostrar todos los productos            |
| Reporte por cantidad mínima      | `Fore.LIGHTMAGENTA_EX`       | Título del listado con pocos productos |
| Reporte de cantidades            | `Fore.GREEN`                 | Datos dentro del reporte               |
| Menú principal                   | `Fore.LIGHTBLUE_EX`          | Encabezado del menú principal          |

---

## 🔧 Funcionalidades del sistema

### 📥 Registrar producto
Permite al usuario ingresar:
- Nombre (obligatorio)
- Descripción (opcional)
- Cantidad (entero ≥ 0)
- Precio (decimal > 0)
- Categoría (opcional)

✔️ El sistema valida todos los campos antes de guardar.

---

### 📋 Mostrar productos
Muestra en consola todos los productos existentes en la base de datos en color **fucsia** (`Fore.MAGENTA`).

---

### 🔍 Buscar producto por ID
Permite ingresar un ID y devuelve los datos del producto si existe.

---

### 📝 Actualizar producto
- Muestra todos los productos
- Permite seleccionar uno por ID
- Cada campo puede dejarse vacío para mantener el valor actual

⚠️ Las instrucciones se muestran en color **naranja aproximado** (`Fore.LIGHTRED_EX`).

---

### 🗑️ Eliminar producto
- Pide confirmación antes de eliminar
- Usa color **amarillo** para preguntar
- Usa **rojo** para confirmar la eliminación

---

### 📉 Reporte por cantidad baja
- Permite definir un límite (por ejemplo, 5)
- Muestra todos los productos cuya cantidad es menor o igual
- Usa color **fucsia brillante** (`Fore.LIGHTMAGENTA_EX`) en el título del listado

---

### 🔚 Salir
Finaliza el programa cerrando la conexión con la base de datos.

---

## 💽 Base de datos

El sistema crea automáticamente una base de datos SQLite local (`inventario.db`) con la tabla `productos`, que contiene:

- `id` (INTEGER, PRIMARY KEY)
- `nombre` (TEXT)
- `descripcion` (TEXT)
- `cantidad` (INTEGER)
- `precio` (REAL)
- `categoria` (TEXT)

---

## 🚀 Ejecución

Para correr el programa:

```bash
python inventario.py
