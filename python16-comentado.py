import sqlite3

# Abro la conexión a la base de datos 'inventario.db' y creo un cursor para ejecutar comandos SQL
conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# Creo la tabla 'productos' si no existe aún
# La tabla tendrá columnas para id (clave primaria autoincremental), nombre, descripción, cantidad, precio y categoría
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
# Guardo los cambios en la base de datos
conn.commit()

# Función para registrar un nuevo producto con validaciones en los datos ingresados
def registrar_producto():
    # Pido el nombre y me aseguro que no quede vacío
    nombre_producto = input("Nombre del producto: ").strip()
    while not nombre_producto:
        print("El nombre no puede estar vacío.")
        nombre_producto = input("Nombre del producto: ").strip()

    # La descripción es opcional, por eso la pido sin validación estricta
    descripcion_producto = input("Descripción (opcional): ").strip()

    # Valido que la cantidad sea un número entero mayor o igual a cero
    while True:
        cantidad_inventario = input("Cantidad: ").strip()
        if cantidad_inventario.isdigit() and int(cantidad_inventario) >= 0:
            cantidad_inventario = int(cantidad_inventario)
            break
        else:
            print("Cantidad inválida. Debe ser un entero >= 0.")

    # Valido que el precio sea un número decimal positivo
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

    # Pido la categoría del producto, sin validaciones estrictas
    categoria_producto = input("Categoría: ").strip()

    # Inserto el nuevo producto en la base de datos con todos los datos ya validados
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre_producto, descripcion_producto, cantidad_inventario, precio_producto, categoria_producto))
    conn.commit()
    print("Producto registrado con éxito.")

# Función para mostrar todos los productos almacenados en la base
def mostrar_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    # Si no hay productos, aviso y salgo de la función
    if not productos:
        print("No hay productos registrados.")
        return

    print("\n--- Productos en Inventario ---")
    # Recorro cada producto y muestro sus datos ordenadamente
    for p in productos:
        print(f"ID: {p[0]} | Nombre: {p[1]} | Descripción: {p[2]} | Cantidad: {p[3]} | Precio: ${p[4]:.2f} | Categoría: {p[5]}")

# Función para buscar un producto específico por su ID
def buscar_producto():
    mostrar_productos()  # Primero muestro la lista para ayudar a elegir el ID correcto

    id_producto_buscar = input("Ingrese ID del producto a buscar: ").strip()
    # Valido que el ID ingresado sea un número entero válido
    if not id_producto_buscar.isdigit():
        print("ID inválido.")
        return
    id_producto = int(id_producto_buscar)

    # Busco en la base el producto con ese ID
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()

    # Si lo encuentro, muestro sus datos completos, sino aviso que no existe
    if producto:
        print(f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: ${producto[4]:.2f} | Categoría: {producto[5]}")
    else:
        print("Producto no encontrado.")

# Función para actualizar los datos de un producto usando su ID
def actualizar_producto():
    mostrar_productos()  # Muestro los productos para facilitar elegir el ID a modificar

    id_producto_actualizar = input("ID del producto a actualizar: ").strip()
    # Valido que el ID sea correcto
    if not id_producto_actualizar.isdigit():
        print("ID inválido.")
        return
    id_producto = int(id_producto_actualizar)

    # Obtengo los datos actuales del producto para mostrar y usar como valores por defecto
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        print("Producto no encontrado.")
        return

    print("Deja vacío para mantener el valor actual.")

    # Guardo los valores actuales para comparar con los nuevos datos que ingrese el usuario
    valores_actuales = {
        "nombre": producto[1],
        "descripcion": producto[2],
        "cantidad": producto[3],
        "precio": producto[4],
        "categoria": producto[5]
    }

    # Pido nuevos valores, si el usuario deja vacío se mantiene el valor anterior
    nuevo_nombre = input(f"Nuevo nombre (actual: {valores_actuales['nombre']}): ").strip()
    nueva_descripcion = input(f"Nueva descripción (actual: {valores_actuales['descripcion']}): ").strip()

    # Valido que la cantidad sea válida o dejo la anterior si está vacío
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

    # Valido el precio nuevo o mantengo el anterior
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

    # Pido nueva categoría, o mantengo la anterior si se deja vacío
    nueva_categoria = input(f"Nueva categoría (actual: {valores_actuales['categoria']}): ").strip()

    # Preparo la lista con los datos actualizados (o antiguos si no hubo cambios)
    campos_actualizados = [
        nuevo_nombre or valores_actuales['nombre'],
        nueva_descripcion or valores_actuales['descripcion'],
        nueva_cantidad,
        nuevo_precio,
        nueva_categoria or valores_actuales['categoria'],
        id_producto
    ]

    # Ejecuto la actualización en la base de datos con los nuevos datos
    cursor.execute('''
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    ''', campos_actualizados)
    conn.commit()
    print("Producto actualizado con éxito.")

# Función para eliminar un producto mediante su ID, con confirmación previa
def eliminar_producto():
    mostrar_productos()  # Muestro la lista para ayudar a elegir el producto correcto

    id_producto_eliminar = input("ID del producto a eliminar: ").strip()
    # Valido que el ID sea válido
    if not id_producto_eliminar.isdigit():
        print("ID inválido.")
        return
    id_producto = int(id_producto_eliminar)

    # Busco el producto en la base
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        print("Producto no encontrado.")
        return

    # Confirmo que el usuario realmente quiere eliminar el producto
    confirmacion = input(f"Confirma eliminar '{producto[1]}'? (s/n): ").lower()
    if confirmacion == 's':
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conn.commit()
        print("Producto eliminado.")
    else:
        print("Eliminación cancelada.")

# Función para mostrar un reporte de productos con cantidad igual o menor a un valor especificado por el usuario
def reporte_cantidad_minima():
    # Pido y valido el límite de cantidad para filtrar los productos
    while True:
        limite_cantidad = input("Mostrar productos con cantidad <= a: ").strip()
        if limite_cantidad.isdigit():
            limite_cantidad = int(limite_cantidad)
            break
        else:
            print("Ingrese un número entero válido.")

    # Busco todos los productos con cantidad menor o igual al límite indicado
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite_cantidad,))
    productos = cursor.fetchall()

    if not productos:
        print("No hay productos con esa cantidad o menos.")
        return

    print(f"\n--- Productos con cantidad menor o igual a {limite_cantidad} ---")
    # Muestro el listado filtrado con la información relevante
    for p in productos:
        print(f"ID: {p[0]} | Nombre: {p[1]} | Cantidad: {p[3]} | Precio: ${p[4]:.2f}")

# Función principal que muestra el menú y permite al usuario elegir qué acción realizar
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

        # Según la opción elegida, llamo a la función correspondiente
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

# Si este archivo se ejecuta directamente, arranco el menú
if __name__ == "__main__":
    menu()
    # Cierro la conexión con la base de datos al salir del programa
    conn.close()
