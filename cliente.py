import flet as ft
import mysql.connector
from db import connect_to_db

class VistaCliente:
    def __init__(self, page: ft.Page, callback_volver):
        self.page = page
        self.callback_volver = callback_volver
        
        # --- CREACIÓN DE CONTROLES EN __init__ ---
        self.txt_apellido = ft.TextField(label="Apellido")
        self.txt_nombre = ft.TextField(label="Nombre")
        self.txt_dni = ft.TextField(label="DNI")
        self.txt_direccion = ft.TextField(label="Dirección")
        self.txt_telefono = ft.TextField(label="Teléfono")
        self.txt_cod_cliente = ft.TextField(label="Código de Cliente (ej: C001)")

        self.tabla_clientes = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Apellido")), ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("DNI")), ft.DataColumn(ft.Text("Dirección")),
                ft.DataColumn(ft.Text("Teléfono")), ft.DataColumn(ft.Text("Cód. Cliente")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[], expand=True,
        )

        # --- CAMBIO CLAVE #1: Creamos el diálogo como siempre ---
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo Cliente"),
            content=ft.Column(
                controls=[
                    self.txt_apellido, self.txt_nombre, self.txt_dni,
                    self.txt_direccion, self.txt_telefono, self.txt_cod_cliente
                ], tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                ft.FilledButton("Guardar", on_click=self.guardar_cliente),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def build(self):
        """Construye la vista y AÑADE el diálogo al overlay."""
        # --- CAMBIO CLAVE #2: Añadimos el diálogo a la capa superpuesta DE INMEDIATO ---
        # El diálogo ahora "existe" en la página desde el principio, solo que está oculto.
        if self.dlg_modal not in self.page.overlay:
             self.page.overlay.append(self.dlg_modal)
        
        self.refrescar_tabla()
        
        return ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Gestión de Clientes", size=24, weight="bold"),
                        ft.ElevatedButton("Volver al Menú", icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.callback_volver()),
                    ],
                ),
                ft.Row(
                    controls=[ft.ElevatedButton("Nuevo Cliente", icon=ft.Icons.ADD, on_click=self.mostrar_dialogo_alta)]
                ),
                ft.Divider(),
                ft.Column(controls=[self.tabla_clientes], scroll=ft.ScrollMode.ALWAYS, expand=True)
            ],
        )

    def refrescar_tabla(self):
        self.tabla_clientes.rows.clear()
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT per.apellido, per.nombre, per.dni, per.direccion, per.tele_contac, c.cod_cliente FROM persona per JOIN cliente c ON per.dni = c.dni ORDER BY per.apellido"
                cursor.execute(query)
                for row in cursor.fetchall():
                    self.tabla_clientes.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(row[0])), ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(row[2])), ft.DataCell(ft.Text(row[3])),
                            ft.DataCell(ft.Text(row[4])), ft.DataCell(ft.Text(row[5])),
                            ft.DataCell(ft.Row([
                                ft.IconButton(icon=ft.Icons.EDIT, tooltip="Modificar", icon_color="blue"),
                                ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red"),
                            ])),
                        ])
                    )
            except Exception as e:
                print(f"Error al refrescar tabla: {e}")
            finally:
                if conn.is_connected():
                    conn.close()
        self.page.update()

    def mostrar_dialogo_alta(self, e):
        """Muestra el diálogo que ya está en el overlay."""
        print("Abriendo diálogo...")
        for field in [self.txt_apellido, self.txt_nombre, self.txt_dni, self.txt_direccion, self.txt_telefono, self.txt_cod_cliente]:
            field.value = ""

        # --- CAMBIO CLAVE #3: Solo cambiamos 'open' a True y actualizamos. ---
        self.dlg_modal.open = True
        self.page.update()

    def cerrar_dialogo(self, e):
        """Cierra el diálogo."""
        self.dlg_modal.open = False
        self.page.update()

    def guardar_cliente(self, e):
        # ... (El resto del código de guardar es el mismo y está bien)
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                sql_persona = "INSERT INTO Persona (DNI, Nombre, Apellido, Direccion, Tele_Contac) VALUES (%s, %s, %s, %s, %s)"
                val_persona = (self.txt_dni.value, self.txt_nombre.value, self.txt_apellido.value, self.txt_direccion.value, self.txt_telefono.value)
                cursor.execute(sql_persona, val_persona)
                
                sql_cliente = "INSERT INTO Cliente (Cod_Cliente, DNI) VALUES (%s, %s)"
                val_cliente = (self.txt_cod_cliente.value, self.txt_dni.value)
                cursor.execute(sql_cliente, val_cliente)
                
                conn.commit()
                print("Cliente guardado con éxito.")
            except Exception as ex:
                print(f"Error al guardar cliente: {ex}")
                conn.rollback()
            finally:
                if conn.is_connected():
                    conn.close()

        self.cerrar_dialogo(e)
        self.refrescar_tabla()