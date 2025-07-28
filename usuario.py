# usuario.py

import flet as ft

def Herramienta_Usuario(page: ft.Page, volver_callback):
    page.controls.clear()
    page.add(
        ft.Text("Gestión de Usuarios", size=30, weight="bold"),
        ft.ElevatedButton(text="Volver al menú", on_click=lambda e: volver_callback(page))
    )
    page.update()
