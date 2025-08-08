import flet as ft

class Herramienta_Usuario:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.mostrar_login()

    def mostrar_login(self):
        self.page.clean()
        self.usuario = ft.TextField(label="Usuario", width=300)
        self.contrasena = ft.TextField(label="Contraseña", password=True, width=300)
        iniciar_btn = ft.ElevatedButton("Iniciar sesión")
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.main_menu_callback(self.page))

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
        iniciar_btn = ft.ElevatedButton(
            "Iniciar sesión",
            on_click=self.validar_usuario
        )
    def validar_usuario(self, e):
        username = self.usuario.value
        password = self.contrasena.value
    
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT password_hash, rol FROM usuario WHERE username=%s", (username,))
        result = self.cursor.fetchone()
    
        if result and result[0] == password:  # En producción se usaria bcrypt.checkpw
            self.page.snack_bar = ft.SnackBar(ft.Text("Inicio de sesión exitoso"))
            self.page.snack_bar.open = True
        # Aqui se podria redirigir al menu principal
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Usuario o contraseña incorrectos"))
            self.page.snack_bar.open = True
    
        self.page.update()

