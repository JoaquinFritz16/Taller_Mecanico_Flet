import flet as ft
import mysql.connector
from db import connect_to_db


class Herramienta_Cliente:
    def __init__(self, page: ft.Page, main_menu_callback, connection):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connection
        self.cursor = self.connection.cursor() if self.connection else None
        self.mostrar_cliente()


    def mostrar_cliente(self, e=None):
        self.page.clean()
        header = ft.Row(
            controls=[
                ft.Text("Herramienta de Gestión de Clientes", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_cliente),
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_cliente),
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_clientes),
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        data_table = self.create_client_table()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[header, data_table],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        )

    def alta_cliente(self, e=None):
        self.page.clean()
        self.dni = ft.TextField(label="DNI", width=300)
        self.apellido = ft.TextField(label="Apellido", width=300)
        self.nombre = ft.TextField(label="Nombre", width=300)
        self.direccion = ft.TextField(label="Dirección", width=300)
        self.telefono = ft.TextField(label="Teléfono", width=300)
        self.cod_cliente = ft.TextField(label="Código Cliente", width=300)

        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_cliente)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_cliente)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Cliente", size=24, weight="bold"),
                    self.dni,
                    self.apellido,
                    self.nombre,
                    self.direccion,
                    self.telefono,
                    self.cod_cliente,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cliente(self, e=None):
        try:
            self.cursor.execute(
                "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.dni.value,
                    self.apellido.value,
                    self.nombre.value,
                    self.direccion.value,
                    self.telefono.value,
                ),
            )
            self.cursor.execute(
                "INSERT INTO cliente (cod_cliente, dni) VALUES (%s, %s)",
                (self.cod_cliente.value, self.dni.value),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente guardado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_cliente()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def consulta_cliente(self, e=None):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Clientes", size=24, weight="bold"))
        self.page.add(self.create_client_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_cliente))
        self.page.update()

    def imprimir_clientes(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)

    def create_client_table(self, e=None):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return ft.Text("No hay conexión a la base de datos")

        listado_todos_clientes = """
            SELECT per.apellido, per.nombre, per.dni,
                per.direccion, per.tele_contac, c.cod_cliente
            FROM persona per INNER JOIN cliente c ON per.dni = c.dni
            ORDER BY per.apellido
        """
        self.cursor.execute(listado_todos_clientes)
        datos_clientes = self.cursor.fetchall()
        rows = []

        for cliente in datos_clientes:
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, c=cliente: self.eliminar_cliente(e, c),
            )

            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, c=cliente: self.actualizar_cliente(e, c),
            )

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cliente[0])),
                        ft.DataCell(ft.Text(cliente[1])),
                        ft.DataCell(ft.Text(str(cliente[2]))),
                        ft.DataCell(ft.Text(cliente[3])),
                        ft.DataCell(ft.Text(cliente[4])),
                        ft.DataCell(ft.Text(str(cliente[5]))),
                        ft.DataCell(
                            ft.Row(controls=[eliminar_button, actualizar_button])
                        ),
                    ],
                ),
            )

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Direccion")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Código de Cliente")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )
        return data_table

    def eliminar_cliente(self, e, cliente):
        try:
            dni = cliente[2]
            cod_cliente = cliente[5]
            self.cursor.execute("DELETE FROM cliente WHERE cod_cliente = %s", (cod_cliente,))
            self.cursor.execute("DELETE FROM persona WHERE dni = %s", (dni,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente eliminado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_cliente()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_cliente(self, e, cliente):
        self.page.clean()
        self.dni = ft.TextField(label="DNI", value=str(cliente[2]), width=300, disabled=True)
        self.apellido = ft.TextField(label="Apellido", value=cliente[0], width=300)
        self.nombre = ft.TextField(label="Nombre", value=cliente[1], width=300)
        self.direccion = ft.TextField(label="Dirección", value=cliente[3], width=300)
        self.telefono = ft.TextField(label="Teléfono", value=cliente[4], width=300)
        self.cod_cliente = ft.TextField(label="Código Cliente", value=str(cliente[5]), width=300, disabled=True)

        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_cambios_cliente(e, cliente))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_cliente)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Cliente", size=24, weight="bold"),
                    self.dni,
                    self.apellido,
                    self.nombre,
                    self.direccion,
                    self.telefono,
                    self.cod_cliente,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cambios_cliente(self, e, cliente):
        try:
            self.cursor.execute(
                "UPDATE persona SET apellido=%s, nombre=%s, direccion=%s, tele_contac=%s WHERE dni=%s",
                (
                    self.apellido.value,
                    self.nombre.value,
                    self.direccion.value,
                    self.telefono.value,
                    self.dni.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Cliente actualizado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_cliente()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def consulta_cliente(self, e=None):
        self.page.clean()

        # Filtros de búsqueda
        self.criterio_dropdown = ft.Dropdown(
            label="Buscar por",
            options=[
                ft.dropdown.Option("DNI"),
                ft.dropdown.Option("Apellido"),
                ft.dropdown.Option("Código Cliente"),
            ],
            width=200,
        )
        self.criterio_text = ft.TextField(label="Valor", width=200)

        buscar_btn = ft.ElevatedButton(
            "Buscar",
            icon=ft.Icons.SEARCH,
            on_click=self.buscar_cliente
        )
        volver_btn = ft.ElevatedButton("Volver", on_click=self.mostrar_cliente)

        self.page.add(
            ft.Column([
                ft.Text("Consulta de Clientes", size=24, weight="bold"),
                ft.Row([self.criterio_dropdown, self.criterio_text, buscar_btn, volver_btn]),
                self.create_client_table()
            ])
        )
        self.page.update()

    def buscar_cliente(self, e=None):
        criterio = self.criterio_dropdown.value
        valor = self.criterio_text.value

        query = """
            SELECT per.apellido, per.nombre, per.dni, per.direccion, per.tele_contac, c.cod_cliente
            FROM persona per INNER JOIN cliente c ON per.dni = c.dni
        """
        if criterio == "DNI":
            query += " WHERE per.dni = %s"
        elif criterio == "Apellido":
            query += " WHERE per.apellido LIKE %s"
            valor = f"%{valor}%"
        elif criterio == "Código Cliente":
            query += " WHERE c.cod_cliente = %s"

        self.cursor.execute(query, (valor,))
        datos_clientes = self.cursor.fetchall()

        # Refrescar tabla con resultados
        self.page.clean()
        self.page.add(ft.Text("Resultados de búsqueda", size=20, weight="bold"))
        self.page.add(self.create_client_table_from_data(datos_clientes))
        self.page.add(ft.ElevatedButton("Volver", on_click=self.consulta_cliente))
        self.page.update()

    def create_client_table_from_data(self, datos_clientes):
        rows = []
        for cliente in datos_clientes:
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, c=cliente: self.eliminar_cliente(e, c),
            )
            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, c=cliente: self.actualizar_cliente(e, c),
            )
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cliente[0])),
                        ft.DataCell(ft.Text(cliente[1])),
                        ft.DataCell(ft.Text(str(cliente[2]))),
                        ft.DataCell(ft.Text(cliente[3])),
                        ft.DataCell(ft.Text(cliente[4])),
                        ft.DataCell(ft.Text(str(cliente[5]))),
                        ft.DataCell(ft.Row(controls=[eliminar_button, actualizar_button])),
                    ],
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Dirección")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Código de Cliente")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )

def main_menu_callback(page: ft.Page):
    page.clean()
    page.add(ft.Text("Menú Principal"))


def main(page: ft.Page):
    app = Herramienta_Cliente(page, main_menu_callback)
