import flet as ft
from cliente import VistaCliente
from usuario import VistaUsuario

def main(page: ft.Page):
    page.title = "Administración de Taller Mecánico"
    page.window.maximized = True
    page.theme_mode = ft.ThemeMode.DARK
    
    page.assets_dir = "iconos"
    page.update()

    main_container = ft.Column(expand=True)

    def menu_principal():
        main_container.controls.clear()

        cliente_icono = ft.Image(src="iconos/iconos/Cliente.png", width=28, height=28)
        proveedor_icono = ft.Image(src="iconos/iconos/proveedor.png", width=28, height=28)
        usuario_icono = ft.Image(src="iconos/iconos/usuario.png", width=28, height=28)
        cliente_item = ft.Row(controls=[ft.Image(src=cliente_icono.src, width=28, height=28), ft.Text("Cliente")])
        proveedor_item = ft.Row(controls=[ft.Image(src=proveedor_icono.src, width=28, height=28), ft.Text("Proveedor")])
        usuario_item = ft.Row(controls=[ft.Image(src=usuario_icono.src, width=28, height=28), ft.Text("Usuario")])
        menu_bar = ft.Row(
            controls=[
                ft.PopupMenuButton(
                    content=ft.Text("Archivo"),
                    items=[
                        ft.PopupMenuItem(text="Salir", icon=ft.Icons.EXIT_TO_APP, on_click=lambda _: page.window_destroy()),
                    ]
                ),
                ft.PopupMenuButton(
                    content=ft.Text("Herramientas"),
                    items=[
                        ft.PopupMenuItem(content=cliente_item, on_click=lambda _: herramienta_cliente()),
                        ft.PopupMenuItem(content=proveedor_item),
                        ft.PopupMenuItem(content=usuario_item, on_click=lambda _: herramienta_usuario()),
                    ]
                ),
            ]
        )

        toolbar = ft.Row(
            controls=[
                ft.IconButton(content=ft.Image(src=cliente_icono.src, width=28, height=28), tooltip="Cliente", on_click=lambda _: herramienta_cliente()),
            ]
        )

        main_container.controls.extend([
            menu_bar,
            toolbar,
            ft.Divider(),
            ft.Container(
                content=ft.Text("Taller Mecanico con Flet", size=40, text_align=ft.TextAlign.CENTER),
                expand=True,
                alignment=ft.alignment.center
            )
        ])
        page.update()

    def herramienta_cliente():
        main_container.controls.clear()
        vista = VistaCliente(page, menu_principal)
        main_container.controls.append(vista.build())
        page.update()

    def herramienta_usuario():
        main_container.controls.clear()
        vista = VistaUsuario(page, menu_principal)
        main_container.controls.append(vista.build())
        page.update()

    page.add(main_container)
    menu_principal()

ft.app(target=main, assets_dir="iconos")