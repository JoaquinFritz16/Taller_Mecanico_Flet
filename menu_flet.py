import flet as ft
import mysql.connector

#--Importar los archivos correspondiente al sistema con las clases
from usuario import Herramienta_Usuario

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='root',
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

connection = connect_to_db()

def menu_principal(page: ft.Page):
    page.window.maximized=True
    page.add(ft.Text("Prueba de conexión a la base de datos"))
    page.title = "Administración de Taller Mecánico"
    
    # ----Iconos Personales--- 
    #  Crear un Row personalizado para el PopupMenuItem y barra de herramientas
        
    cliente_icono = ft.Image(src="iconos/iconos/usuario.png", width=28, height=28)
    cliente_item = ft.Row(
        controls=[
            cliente_icono,
            ft.Text("Cliente"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )

    proveedor_icono = ft.Image(src="iconos/iconos/proveedor.png", width=28, height=28)
    proveedor_item = ft.Row(
        controls=[
            proveedor_icono,
            ft.Text("Proveedor"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )

    repuesto_icono = ft.Image(src="iconos/iconos/caja-de-cambios.png", width=28, height=28)
    repuesto_item = ft.Row(
        controls=[
            repuesto_icono,
            ft.Text("Repuesto"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )

    empleado_icono = ft.Image(src="iconos/iconos/empleado.png", width=28, height=28)
    empleado_item = ft.Row(
        controls=[
            empleado_icono,
            ft.Text("Empleado"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )

    usuario_icono = ft.Image(src="iconos/iconos/usuarios.png", width=28, height=28)
    usuario_item = ft.Row(
        controls=[
            usuario_icono,
            ft.Text("Usuario"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )

    ficha_tecnica_icono=ft.Image(src="iconos/iconos/auto.png", width=28, height=28)
    ficha_tecnica_item=ft.Row(
        controls=[
            ficha_tecnica_icono,
            ft.Text("Ficha Técnica")
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )

    presupuesto_icono=ft.Image(src="iconos/iconos/presupuesto.png", width=28, height=28)
    presupuesto_icono_item=ft.Row(
         controls=[
             presupuesto_icono,
             ft.Text("Presupuesto")
         ]
     )
    
    # ---Barra de Menú---
    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Copiar", icon=ft.Icons.COPY),
            ft.PopupMenuItem(text="Salir", icon=ft.Icons.EXIT_TO_APP),
        ],
        content=ft.Text("Archivo"), tooltip="Archivo"
    )

    herramientas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=cliente_item, on_click=lambda e: cliente(e, page)),
            ft.PopupMenuItem(content=proveedor_item, on_click=lambda e:proveedor(e, page)),
            ft.PopupMenuItem(content=repuesto_item, on_click=lambda e: producto(e, page)),
            ft.PopupMenuItem(content=empleado_item, on_click=lambda e: empleado(e, page)),
            ft.PopupMenuItem(content=usuario_item, on_click=lambda e: usuario(e, page)),
        ],
        content=ft.Text("Herramientas"), tooltip="Administrador de archivos maestros"
        
    )
    
    administracion = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ficha_tecnica_item),#, on_click=lambda e: cliente(e, page)),
            ft.PopupMenuItem(content=presupuesto_icono_item),#, on_click=lambda e:proveedor(e, page)),
        ],
        content=ft.Text("Administración"), tooltip="Administración de presupuesto y ficha técnica"
        
    )
    
    
    #--Barra de Herramientas--
    #--Cliente
    boton_cliente_item=ft.Row(
        controls=[
            cliente_icono,
        ],
    )
    boton_cliente = ft.IconButton(content=boton_cliente_item, tooltip="Cliente")
    
    
    #--Repuesto
    boton_repuesto_item=ft.Row(
        controls=[
            repuesto_icono,
        ],
    )
    boton_producto = ft.IconButton(content=boton_repuesto_item, tooltip="Repuesto")
    
     #--Ficha Técnica
    boton_ficha_tecnica_item=ft.Row(
        controls=[
                 ficha_tecnica_icono,
        ]
    )
    boton_ficha_tecnica = ft.IconButton(content=boton_ficha_tecnica_item,tooltip="Ficha Técnica")
    
    #--Presupuesto
    boton_presupuesto_item=ft.Row(
        controls=[
            presupuesto_icono,
        ]
    )
    boton_presupuesto=ft.IconButton(content=boton_presupuesto_item,tooltip="Presupuesto")
    
    
    
    
    page.add(
        ft.Row(
            controls=[
                archivo_menu,
                administracion,
                herramientas_menu
                
            ],
            spacing=10,
        ),
        
        ft.Row(
            controls=[
                boton_cliente,
                boton_producto,
                boton_ficha_tecnica,
                boton_presupuesto
            ]
        )
    
    )

def cliente(e, page: ft.Page):
    pass
    
def proveedor(e, page: ft.Page):
    pass
    
def producto(e, page: ft.Page):
    pass

def empleado(e, page: ft.Page):
    pass

def usuario(e, page: ft.Page):
    Herramienta_Usuario(page, menu_principal)



def main(page: ft.Page):
    page.window.maximized = True
    menu_principal(page)

ft.app(target=main)
