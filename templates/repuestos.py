import flet as ft
import mysql.connector
from db import connect_to_db

class Herramienta_Repuesto:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None
        self.mostrar_repuesto()

    def mostrar_repuesto(self, e=None):
        self.page.clean()
        header = ft.Row(
            controls=[
                ft.Text("Herramienta de Gestión de Repuestos", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_repuesto),
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_repuesto),
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_repuestos),
                ft.ElevatedButton(text="Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        data_table = self.create_repuesto_table()
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

    def alta_repuesto(self, e):
        self.page.clean()
        self.cod_repuesto = ft.TextField(label="Código Repuesto", width=300)
        self.descripcion = ft.TextField(label="Descripción", width=300)
        self.precio = ft.TextField(label="Precio Unitario", width=300)

        guardar_btn = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_repuesto)
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_repuesto)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Alta de Repuesto", size=24, weight="bold"),
                    self.cod_repuesto,
                    self.descripcion,
                    self.precio,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_repuesto(self, e):
        try:
            self.cursor.execute(
                "INSERT INTO repuestos (cod_repuesto, descripcion, pcio_unit) VALUES (%s, %s, %s)",
                (
                    self.cod_repuesto.value,
                    self.descripcion.value,
                    self.precio.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Repuesto guardado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_repuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def consulta_repuesto(self, e):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Repuestos", size=24, weight="bold"))
        self.page.add(self.create_repuesto_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_repuesto))
        self.page.update()

    def imprimir_repuestos(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de impresión no implementada"))
        self.page.snack_bar.open = True
        self.page.update()

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)

    def create_repuesto_table(self):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return ft.Text("No hay conexión a la base de datos")

        listado_todos_repuestos = """
            SELECT cod_repuesto, descripcion, pcio_unit
            FROM repuestos
            ORDER BY cod_repuesto
        """
        self.cursor.execute(listado_todos_repuestos)
        datos_repuestos = self.cursor.fetchall()
        rows = []

        for repuesto in datos_repuestos:
            eliminar_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, r=repuesto: self.eliminar_repuesto(e, r),
            )

            actualizar_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, r=repuesto: self.actualizar_repuesto(e, r),
            )

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(repuesto[0]))),
                        ft.DataCell(ft.Text(repuesto[1])),
                        ft.DataCell(ft.Text(str(repuesto[2]))),
                        ft.DataCell(
                            ft.Row(controls=[eliminar_button, actualizar_button])
                        ),
                    ],
                ),
            )

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código de Repuesto")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Precio Unitario")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
        )
        return data_table

    def eliminar_repuesto(self, e, repuesto):
        try:
            cod_repuesto = repuesto[0]
            self.cursor.execute("DELETE FROM repuestos WHERE cod_repuesto = %s", (cod_repuesto,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Repuesto eliminado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_repuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_repuesto(self, e, repuesto):
        self.page.clean()
        self.cod_repuesto = ft.TextField(label="Código Repuesto", value=str(repuesto[0]), width=300, disabled=True)
        self.descripcion = ft.TextField(label="Descripción", value=repuesto[1], width=300)
        self.precio = ft.TextField(label="Precio Unitario", value=str(repuesto[2]), width=300)

        guardar_btn = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_cambios_repuesto(e, repuesto))
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_repuesto)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Editar Repuesto", size=24, weight="bold"),
                    self.cod_repuesto,
                    self.descripcion,
                    self.precio,
                    ft.Row([guardar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
            )
        )
        self.page.update()

    def guardar_cambios_repuesto(self, e, repuesto):
        try:
            self.cursor.execute(
                "UPDATE repuestos SET descripcion=%s, pcio_unit=%s WHERE cod_repuesto=%s",
                (
                    self.descripcion.value,
                    self.precio.value,
                    self.cod_repuesto.value,
                ),
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Repuesto actualizado correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_repuesto()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()


def main_menu_callback(page: ft.Page):
    page.clean()
    page.add(ft.Text("Menú Principal"))


def main(page: ft.Page):
    app = Herramienta_Repuesto(page, main_menu_callback)
