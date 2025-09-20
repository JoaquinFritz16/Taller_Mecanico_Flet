import flet as ft
from db import connect_to_db

class Herramienta_FichaTecnica:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connect_to_db()
        self.cursor = self.connection.cursor() if self.connection else None
        self.mostrar_ficha_tecnica()

    def mostrar_ficha_tecnica(self, e=None):
        self.page.clean()

        header = ft.Row(
            controls=[
                ft.Text("Gestión de Fichas Técnicas", size=20, weight="bold"),
                ft.ElevatedButton("Alta", on_click=self.alta_ficha_tecnica),
                ft.ElevatedButton("Consulta", on_click=self.consulta_ficha_tecnica),
                ft.ElevatedButton("Volver al Menú", on_click=self.volver_al_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        data_table = self.create_ficha_tecnica_table()

        self.page.add(ft.Column([header, data_table], spacing=20))
        self.page.update()

    def alta_ficha_tecnica(self, e):
        self.page.clean()

        # Dropdown de clientes
        clientes = self.get_clientes()
        self.cod_cliente_combo = ft.Dropdown(
            label="Cliente",
            options=[ft.dropdown.Option(c['cod_cliente'], c['dni']) for c in clientes],
            on_change=self.actualizar_vehiculos
        )

    
        self.vehiculo_combo = ft.Dropdown(label="Vehículo", options=[])

        # Inputs de costos
        self.subtotal = ft.TextField(label="Subtotal", width=200, value="0")
        self.mano_obra = ft.TextField(label="Mano de Obra", width=200, value="0")
        self.total_general = ft.TextField(label="Total General", width=200, disabled=True)

        guardar_btn = ft.ElevatedButton("Guardar", on_click=self.guardar_ficha_tecnica)
        volver_btn = ft.ElevatedButton("Volver", on_click=self.mostrar_ficha_tecnica)

        self.page.add(ft.Column([
            ft.Text("Alta de Ficha Técnica", size=24, weight="bold"),
            self.cod_cliente_combo,
            self.vehiculo_combo,
            self.subtotal,
            self.mano_obra,
            self.total_general,
            ft.Row([guardar_btn, volver_btn], spacing=10)
        ], spacing=10))

        # Actualizar total al cambiar valores
        self.subtotal.on_change = self.calcular_total
        self.mano_obra.on_change = self.calcular_total

        self.page.update()

    def get_clientes(self):
        self.cursor.execute("SELECT cod_cliente, dni FROM cliente")
        clientes = [{'cod_cliente': c[0], 'dni': c[1]} for c in self.cursor.fetchall()]
        return clientes

    def actualizar_vehiculos(self, e):
        cod_cliente = self.cod_cliente_combo.value
    
        self.cursor.execute("""
            SELECT cd.id_detalle_customer, cd.patente
            FROM customer_detalle cd
            WHERE cd.cod_cliente = %s
        """, (cod_cliente,))
    
        opciones = [ft.dropdown.Option(str(v[0]), v[1]) for v in self.cursor.fetchall()]
        self.vehiculo_combo.options = opciones
        self.vehiculo_combo.value = opciones[0].key if opciones else None
        self.page.update()


    def calcular_total(self, e=None):
        try:
            subtotal = float(self.subtotal.value)
            mano_obra = float(self.mano_obra.value)
            self.total_general.value = str(subtotal + mano_obra)
        except ValueError:
            self.total_general.value = "0"
        self.page.update()


    def guardar_ficha_tecnica(self, e):
        try:
        
            self.cursor.execute(
                "SELECT patente FROM customer_detalle WHERE id_detalle_customer=%s",
                (self.vehiculo_combo.value,)
            )
            patente = self.cursor.fetchone()[0]

            self.cursor.execute(
                "INSERT INTO ficha_tecnica (cod_cliente, vehiculo, subtotal, mano_obra, total_general) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    self.cod_cliente_combo.value,
                    patente,
                    float(self.subtotal.value),
                    float(self.mano_obra.value),
                    float(self.total_general.value)
                )
            )
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Ficha técnica guardada correctamente"))
            self.page.snack_bar.open = True
            self.mostrar_ficha_tecnica()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def create_ficha_tecnica_table(self):
        self.cursor.execute("""
            SELECT f.nro_ficha, f.cod_cliente, f.vehiculo, f.subtotal, f.mano_obra, f.total_general
            FROM ficha_tecnica f
            ORDER BY f.nro_ficha
        """)
        datos = self.cursor.fetchall()
        rows = []
        for ficha in datos:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(ficha[0]))),
                ft.DataCell(ft.Text(str(ficha[1]))),
                ft.DataCell(ft.Text(str(ficha[2]))),
                ft.DataCell(ft.Text(str(ficha[3]))),
                ft.DataCell(ft.Text(str(ficha[4]))),
                ft.DataCell(ft.Text(str(ficha[5]))),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, f=ficha: self.actualizar_ficha_tecnica(e, f)),
                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, f=ficha: self.eliminar_ficha_tecnica(e, f)),
                ]))
            ]))
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nro Ficha")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Vehículo")),
                ft.DataColumn(ft.Text("Subtotal")),
                ft.DataColumn(ft.Text("Mano de Obra")),
                ft.DataColumn(ft.Text("Total General")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows
        )

    def eliminar_ficha_tecnica(self, e, ficha):
        try:
            nro_ficha = ficha[0]
            self.cursor.execute("DELETE FROM ficha_tecnica WHERE nro_ficha=%s", (nro_ficha,))
            self.connection.commit()
            self.page.snack_bar = ft.SnackBar(ft.Text("Ficha técnica eliminada"))
            self.page.snack_bar.open = True
            self.mostrar_ficha_tecnica()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_ficha_tecnica(self, e, ficha):
        pass

    def consulta_ficha_tecnica(self, e):
        self.page.clean()
        self.page.add(ft.Text("Consulta de Fichas Técnicas", size=24, weight="bold"))
        self.page.add(self.create_ficha_tecnica_table())
        self.page.add(ft.ElevatedButton("Volver", on_click=self.mostrar_ficha_tecnica))
        self.page.update()

    def volver_al_menu(self, e):
        self.page.clean()
        self.main_menu_callback(self.page)