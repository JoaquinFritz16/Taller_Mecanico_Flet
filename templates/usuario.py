import flet as ft
import mysql.connector  # Asegurate de tener mysql-connector-python instalado

class Herramienta_Usuario:
    def __init__(self, page: ft.Page, main_menu_callback, connection):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.connection = connection  # <<--- guardamos la conexión a MySQL
        self.mostrar_login()

    def mostrar_login(self):
        self.page.clean()
        self.usuario = ft.TextField(label="Usuario", width=300)
        self.contrasena = ft.TextField(label="Contraseña", password=True, width=300)

        iniciar_btn = ft.ElevatedButton(
            "Iniciar sesión",
            icon=ft.Icons.LOGIN,
            on_click=self.validar_usuario
        )
        volver_btn = ft.ElevatedButton(
            "Volver",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: self.main_menu_callback(self.page)
        )

        self.page.add(
            ft.Column(
                [
                    ft.Text("Inicio de Sesión", size=24, weight="bold"),
                    self.usuario,
                    self.contrasena,
                    ft.Row([iniciar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        self.page.update()

    def validar_usuario(self, e):
        username = self.usuario.value
        password = self.contrasena.value

        cursor = self.connection.cursor()
        cursor.execute("SELECT password_hash, rol FROM usuario WHERE username=%s", (username,))
        result = cursor.fetchone()

        if result and result[0] == password:  # ⚠️ usar bcrypt en producción
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Bienvenido {username} (Rol: {result[1]})"))
            self.page.snack_bar.open = True
            self.page.update()
            
            # Redirigir al menú principal
            self.main_menu_callback(self.page)

        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Usuario o contraseña incorrectos"))
            self.page.snack_bar.open = True
            self.page.update()
