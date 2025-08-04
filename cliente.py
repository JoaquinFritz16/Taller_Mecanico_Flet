import flet as ft
import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            database='Taller_Mecanico',
            ssl_disabled=True
        )
        if connection.is_connected():
            print('Conexión exitosa')
            return connection
    except Exception as ex:
        print('Conexión errónea')
        print(ex)
        return None

class Herramienta_Cliente:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None
        self.mostrar_cliente()

    def mostrar_cliente(self):
        self.bgcolor = ft.Colors.BLUE_50
        self.page.clean()
        header = ft.Row(
            controls=[
                ft.Text("Herramienta de Gestión de Clientes", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta"),
                ft.ElevatedButton(text="Consulta"),
                ft.ElevatedButton(text="Imprimir"),
                ft.ElevatedButton(text="<--Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        data_table = self.create_client_table()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        header,
                        data_table
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20
            )
        )

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)

    def create_client_table(self):
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
            eliminar_button = ft.Container(
                content=ft.Image(src="assets/bote-de-basura.png", width=28, height=28, tooltip="Borrar"),
                on_click=lambda e, c=cliente: self.eliminar_cliente(e, c),
                ink=True,
                padding=5
            )

            actualizar_button = ft.Container(
                content=ft.Image(src="assets/modificar.png", width=28, height=28,tooltip="Modificar"),
                on_click=lambda e, c=cliente: self.actualizar_cliente(e, c),
                ink=True,
                padding=5
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
                            ft.Row(
                                controls=[
                                    eliminar_button,
                                    actualizar_button
                                ]
                            )
                        )
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
        print(f"Eliminar {cliente[0]}")

    def actualizar_cliente(self, e, cliente):
        print(f"Actualizar {cliente[0]}")

def main_menu_callback(page: ft.Page):
    page.clean()
    page.add(ft.Text("Menú Principal"))

def main(page: ft.Page):
    app = Herramienta_Cliente(page, main_menu_callback)

ft.app(target=main)