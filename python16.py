import sqlite3

# Abrir conexión y cursor
conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT
)
''')
conn.commit()

# Registrar producto con validaciones
def registrar_producto():
    nombre_producto = input("Nombre del producto: ").strip()
    while not nombre_producto:
        print("El nombre no puede estar vacío.")
        nombre_producto = input("Nombre del producto: ").strip()

    descripcion_producto = input("Descripción (opcional): ").strip()

    while True:
        cantidad_inventario = input("Cantidad: ").strip()
        if cantidad_inventario.isdigit() and int(cantidad_inventario) >= 0:
            cantidad_inventario = int(cantidad_inventario)
            break
        else:
            print("Cantidad inválida. Debe ser un entero >= 0.")

    while True:
        precio_producto = input("Precio: ").strip()
        try:
            precio_producto = float(precio_producto)
            if precio_producto > 0:
                break
            else:
                print("El precio debe ser mayor que cero.")
        except:
            print("Precio inválido, ingrese un número válido.")

    categoria_producto = input("Categoría: ").strip()

    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre_producto, descripcion_producto, cantidad_inventario, precio_producto, categoria_producto))
    conn.commit()
    print("Producto registrado con éxito.")

# Mostrar todos los productos
def mostrar_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if not productos:
        print("No hay productos registrados.")
        return
    print("\n--- Productos en Inventario ---")
    for p in productos:
        print(f"ID: {p[0]} | Nombre: {p[1]} | Descripción: {p[2]} | Cantidad: {p[3]} | Precio: ${p[4]:.2f} | Categoría: {p[5]}")

# Buscar producto por ID
def buscar_producto():
    mostrar_productos()  # Mostrar antes de pedir ID
    id_producto_buscar = input("Ingrese ID del producto a buscar: ").strip()
    if not id_producto_buscar.isdigit():
        print("ID inválido.")
        return
    id_producto = int(id_producto_buscar)
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    if producto:
        print(f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: ${producto[4]:.2f} | Categoría: {producto[5]}")
    else:
        print("Producto no encontrado.")

# Actualizar producto por ID
def actualizar_producto():
    mostrar_productos()  # Mostrar antes de pedir ID
    id_producto_actualizar = input("ID del producto a actualizar: ").strip()
    if not id_producto_actualizar.isdigit():
        print("ID inválido.")
        return
    id_producto = int(id_producto_actualizar)
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    if not producto:
        print("Producto no encontrado.")
        return

    print("Deja vacío para mantener el valor actual.")

    valores_actuales = {
        "nombre": producto[1],
        "descripcion": producto[2],
        "cantidad": producto[3],
        "precio": producto[4],
        "categoria": producto[5]
    }

    nuevo_nombre = input(f"Nuevo nombre (actual: {valores_actuales['nombre']}): ").strip()
    nueva_descripcion = input(f"Nueva descripción (actual: {valores_actuales['descripcion']}): ").strip()

    while True:
        nueva_cantidad = input(f"Nueva cantidad (actual: {valores_actuales['cantidad']}): ").strip()
        if nueva_cantidad == "":
            nueva_cantidad = valores_actuales['cantidad']
            break
        elif nueva_cantidad.isdigit() and int(nueva_cantidad) >= 0:
            nueva_cantidad = int(nueva_cantidad)
            break
        else:
            print("Cantidad inválida.")

    while True:
        nuevo_precio = input(f"Nuevo precio (actual: {valores_actuales['precio']}): ").strip()
        if nuevo_precio == "":
            nuevo_precio = valores_actuales['precio']
            break
        try:
            nuevo_precio_val = float(nuevo_precio)
            if nuevo_precio_val > 0:
                nuevo_precio = nuevo_precio_val
                break
            else:
                print("El precio debe ser mayor que cero.")
        except:
            print("Precio inválido.")

    nueva_categoria = input(f"Nueva categoría (actual: {valores_actuales['categoria']}): ").strip()

    campos_actualizados = [
        nuevo_nombre or valores_actuales['nombre'],
        nueva_descripcion or valores_actuales['descripcion'],
        nueva_cantidad,
        nuevo_precio,
        nueva_categoria or valores_actuales['categoria'],
        id_producto
    ]

    cursor.execute('''
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    ''', campos_actualizados)
    conn.commit()
    print("Producto actualizado con éxito.")

# Eliminar producto por ID con confirmación
def eliminar_producto():
    mostrar_productos()
    id_producto_eliminar = input("ID del producto a eliminar: ").strip()
    if not id_producto_eliminar.isdigit():
        print("ID inválido.")
        return
    id_producto = int(id_producto_eliminar)
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    if not producto:
        print("Producto no encontrado.")
        return

    confirmacion = input(f"Confirma eliminar '{producto[1]}'? (s/n): ").lower()
    if confirmacion == 's':
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conn.commit()
        print("Producto eliminado.")
    else:
        print("Eliminación cancelada.")

# Reporte productos con cantidad <= límite
def reporte_cantidad_minima():
    while True:
        limite_cantidad = input("Mostrar productos con cantidad <= a: ").strip()
        if limite_cantidad.isdigit():
            limite_cantidad = int(limite_cantidad)
            break
        else:
            print("Ingrese un número entero válido.")

    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite_cantidad,))
    productos = cursor.fetchall()
    if not productos:
        print("No hay productos con esa cantidad o menos.")
        return

    print(f"\n--- Productos con cantidad menor o igual a {limite_cantidad} ---")
    for p in productos:
        print(f"ID: {p[0]} | Nombre: {p[1]} | Cantidad: {p[3]} | Precio: ${p[4]:.2f}")

# Menú principal
def menu():
    while True:
        print("""
--- MENÚ DE INVENTARIO ---
1. Registrar producto
2. Mostrar todos los productos
3. Actualizar producto
4. Eliminar producto
5. Buscar producto por ID
6. Reporte productos con cantidad baja
7. Salir
""")
        opcion_menu = input("Seleccione una opción: ").strip()

        if opcion_menu == '1':
            registrar_producto()
        elif opcion_menu == '2':
            mostrar_productos()
        elif opcion_menu == '3':
            actualizar_producto()
        elif opcion_menu == '4':
            eliminar_producto()
        elif opcion_menu == '5':
            buscar_producto()
        elif opcion_menu == '6':
            reporte_cantidad_minima()
        elif opcion_menu == '7':
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()
    conn.close()
