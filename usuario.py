# usuario.py

import flet as ft
# Agregamos las otras importaciones que necesitaremos
import mysql.connector
from db import connect_to_db

class VistaUsuario:
    # --- CORRECCIÓN AQUÍ: El __init__ ahora acepta 'page' y 'callback_volver' ---
    def __init__(self, page: ft.Page, callback_volver):
        self.page = page
        self.callback_volver = callback_volver
        
        # Definimos los controles que usará la clase
        self.txt_nombre_usuario = ft.TextField(label="Nombre de Usuario")
        self.txt_nombre_completo = ft.TextField(label="Nombre Completo")
        
        self.tabla_usuarios = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Nombre Completo")),
                ft.DataColumn(ft.Text("Rol")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
            expand=True,
        )

    def build(self):
        """Construye y devuelve la interfaz de usuario para esta vista."""
        self.refrescar_tabla_usuarios() # Cargamos los datos al construir
        
        return ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Gestión de Usuarios", size=24, weight="bold"),
                        ft.ElevatedButton(
                            "Volver al Menú",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.callback_volver(),
                        ),
                    ],
                ),
                ft.Divider(),
                # Aquí puedes agregar botones como "Nuevo Usuario", etc.
                ft.Column(controls=[self.tabla_usuarios], scroll=ft.ScrollMode.ALWAYS, expand=True)
            ]
        )

    def refrescar_tabla_usuarios(self):
        """Carga los datos de los usuarios desde la base de datos y los muestra en la tabla."""
        self.tabla_usuarios.rows.clear()
        conn = connect_to_db()
        if not conn:
            print("No se pudo conectar a la base de datos para cargar usuarios.")
            return
        
        try:
            cursor = conn.cursor()
            query = "SELECT id_usuario, nombre_usuario, nombre_completo, rol FROM usuario ORDER BY nombre_usuario"
            cursor.execute(query)
            for row in cursor.fetchall():
                self.tabla_usuarios.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(row[0]))),
                        ft.DataCell(ft.Text(row[1])),
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3])),
                        ft.DataCell(ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Modificar"),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar"),
                        ])),
                    ])
                )
        except Exception as e:
            print(f"Error al refrescar tabla de usuarios: {e}")
        finally:
            conn.close()
        
        # Es importante actualizar la página para que se vean los cambios
        if self.page:
            self.page.update()