import flet as ft
from decimal import Decimal

class SalesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "POS - Dulcería La Rosa"
        self.page.padding = 0
        self.page.theme_mode = "light"
        self.page.bgcolor = "#FFFFFF"
        self.page.window_width = 1024
        self.page.window_height = 768
        self.page.window_resizable = False
        
        self.cart = {}
        self.total = Decimal('0.00')
        
        self.initialize_components()
        self.build()

    def build(self):
        # Layout principal usando Stack para posicionar el total al fondo
        main_layout = ft.Column(
            controls=[
                # Sección superior con productos y botones de acción
                ft.Row(
                    controls=[
                        # Columna izquierda con productos y ticket
                        ft.Column(
                            controls=[
                                ft.Container(  # Contenedor para la sección superior
                                    content=ft.Column(
                                        controls=[
                                            self.products_grid,
                                            self.code_input,
                                        ],
                                    ),
                                    height=300,  # 50% del espacio disponible
                                ),
                                ft.Container(  # Contenedor para el ticket
                                    content=self.cart_container,
                                    height=300,  # 50% del espacio disponible
                                ),
                            ],
                            expand=True,
                            spacing=0,
                        ),
                        # Columna derecha con botones de acción
                        self.create_action_buttons(),
                    ],
                    expand=True,
                ),
                # Total siempre al fondo
                self.total_container,
            ],
            spacing=0,
            expand=True,
        )

        self.page.add(main_layout)

    def initialize_components(self):
        # Sección de botones de productos
        self.products_grid = ft.Container(
            content=self.create_product_buttons(),
            bgcolor="#F5F5F5",
            padding=10,
            height=300,  # Aumentamos la altura del contenedor de productos
        )

        # Sección del ticket
        self.cart_items = ft.DataTable(
            width=800,
            border_radius=8,
            data_row_max_height=40,
            heading_row_height=40,
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#EEEEEE"),
            columns=[
                ft.DataColumn(ft.Text("Código", size=14, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Artículo", size=14, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("P. Unit", size=14, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cant.", size=14, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Total", size=14, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("", size=14)),
            ],
            rows=[],
        )

        # Contenedor del ticket con scroll
        self.cart_container = ft.Container(
            content=self.cart_items,
            bgcolor="#FFFFFF",
            padding=10,
            height=350,  # Altura fija para el ticket
            border=ft.border.all(1, "#EEEEEE"),
            border_radius=8,
        )

        # Campo de código
        self.code_input = ft.TextField(
            label="Código",
            width=200,
            height=35,
            bgcolor="#FFFFFF",
            border_radius=5,
            text_size=14,
            on_submit=self.on_code_submit
        )

        # Total display
        self.total_display = ft.Text(
            value="$ 0.00",
            size=40,
            weight=ft.FontWeight.BOLD,
            color="#000000",
        )

        # Contenedor del total
        self.total_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("$ ", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "0.00",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,  # Alinea a la derecha
            ),
            padding=10,
            width=self.page.width,  # Usa el ancho completo de la página
        )


    def create_product_buttons(self):
        products = [
            {"code": "BOLIS", "name": "Bolis de Fresa", "price": 5.00},
            {"code": "BOTANA", "name": "BOTANA", "price": 12.00},
            {"code": "DULCE", "name": "Dulce", "price": 15.00},
            {"code": "VASO16", "name": "VASO 16", "price": 35.00},
            {"code": "CHOCO", "name": "CHOCOLATE\nNUGS", "price": 78.00},
            {"code": "PALETA", "name": "PALETA\nJUMBO", "price": 25.00},
            {"code": "PALOM", "name": "PALOMITAS\nCON QUEMSO", "price": 45.00},
        ]
        
        return ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=150,
            spacing=5,
            run_spacing=5,
            controls=[
                ft.Container(
                    content=ft.Text(
                        product["name"],
                        size=11,
                        text_align=ft.TextAlign.CENTER,
                        no_wrap=False,
                    ),
                    width=120,  # Ancho fijo para todos los botones
                    height=45,
                    bgcolor="#B3E5FC",
                    border_radius=8,
                    padding=5,
                    on_click=lambda e, p=product: self.add_product(p["code"], p["name"], p["price"]),
                    ink=True,
                    alignment=ft.alignment.center,  # Centra el contenido
                ) for product in products
            ],
        )



    def create_action_buttons(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.RECEIPT_LONG, color="#1565C0"),
                                ft.Text("Ticket F10", size=14),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor="#FFFFFF",
                            shape={"": ft.RoundedRectangleBorder(radius=8)},
                        ),
                        width=160,
                        height=45,
                        on_click=self.show_payment_dialog
                    ),
                ],
                spacing=10,
            ),
            padding=20,
            width=200,
        )

    def add_product(self, code, name, price):
        if code in self.cart:
            self.cart[code]["quantity"] += 1
        else:
            self.cart[code] = {
                "name": name,
                "price": Decimal(str(price)),
                "quantity": 1
            }
        self.update_cart_display()

    def remove_product(self, code):
        if code in self.cart:
            del self.cart[code]
            self.update_cart_display()

    def update_cart_display(self):
        # Actualizar la tabla del carrito
        self.cart_items.rows = []
        self.total = Decimal('0.00')

        for code, item in self.cart.items():
            subtotal = item["price"] * item["quantity"]
            self.total += subtotal

            self.cart_items.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(code)),
                        ft.DataCell(ft.Text(item["name"])),
                        ft.DataCell(ft.Text(f"${item['price']:.2f}")),
                        ft.DataCell(ft.Text(str(item["quantity"]))),
                        ft.DataCell(ft.Text(f"${subtotal:.2f}")),
                        ft.DataCell(
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                icon_color="red",
                                on_click=lambda e, c=code: self.remove_product(c)
                            )
                        ),
                    ]
                )
            )

        # Actualizar el total
        self.total_display.value = f"$ {self.total:.2f}"
        self.page.update()

    def on_code_submit(self, e):
        code = e.control.value.strip().upper()
        
        # Diccionario simulado de productos (esto debería venir de tu base de datos)
        products_db = {
            "BOLIS": {"name": "Bolis de Fresa", "price": 5.00},
            "BOTANA": {"name": "Botana", "price": 12.00},
            "DULCE": {"name": "Dulce", "price": 15.00},
            "VASO16": {"name": "Vaso 16", "price": 35.00},
        }
        
        if code in products_db:
            product = products_db[code]
            self.add_product(code, product["name"], product["price"])
        else:
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Producto no encontrado: {code}"),
                    action="Ok"
                )
            )
        
        e.control.value = ""
        self.page.update()

    def show_payment_dialog(self, e):
        def close_dlg():
            dlg_modal.open = False
            self.page.update()

        def process_payment():
            # Aquí puedes agregar la lógica para guardar la venta
            self.cart = {}
            self.update_cart_display()
            close_dlg()

        def handle_enter(e):
            if received_field.value == "0.00" or received_field.value == "":
                # Si no se ha ingresado monto, usar el total
                received_field.value = f"{self.total:.2f}"
                calculate_change(None)
                self.page.update()
            else:
                # Verificar si el cambio ya fue calculado
                try:
                    change_amount = float(change_field.value)
                    # Si llegamos aquí, el cambio ya está calculado, procedemos con el pago
                    process_payment()
                except ValueError:
                    # Si el cambio aún no se ha calculado, calcularlo primero
                    calculate_change(None)
                    self.page.update()



        def calculate_change(e):
            try:
                received = Decimal(received_field.value if received_field.value else "0")
                change = received - self.total
                change_text.value = f"${change:.2f}"
                if change >= 0:
                    process_button.disabled = False
                    change_text.color = "blue"
                else:
                    process_button.disabled = True
                    change_text.color = "red"
                self.page.update()
            except:
                change_text.value = "Monto inválido"
                change_text.color = "red"
                process_button.disabled = True
                self.page.update()

        # Campos superiores con mejor diseño
        amounts_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("TOTAL A PAGAR", size=14, color="#1565C0", weight=ft.FontWeight.BOLD),
                        ft.Text(f"${self.total:.2f}", 
                            size=28, 
                            color="#E53935", 
                            weight=ft.FontWeight.BOLD)
                    ]),
                    bgcolor="white",
                    padding=15,
                    border_radius=8,
                    border=ft.border.all(1, "#E0E0E0"),
                    width=200,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("RECIBIDO", size=14, color="#2E7D32", weight=ft.FontWeight.BOLD),
                        received_field := ft.TextField(
                            value="0.00",
                            text_align=ft.TextAlign.RIGHT,
                            width=150,
                            height=40,
                            text_size=24,
                            border_color="#2E7D32",
                            focused_border_color="#2E7D32",
                            on_change=calculate_change,
                            on_submit=handle_enter,  # Cambiado de on_key_event a on_submit
                        )
                    ]),
                    bgcolor="white",
                    padding=15,
                    border_radius=8,
                    border=ft.border.all(1, "#E0E0E0"),
                    width=200,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("CAMBIO", size=14, color="#1565C0", weight=ft.FontWeight.BOLD),
                        change_text := ft.Text("$0.00", 
                                            size=28, 
                                            color="#1565C0", 
                                            weight=ft.FontWeight.BOLD)
                    ]),
                    bgcolor="white",
                    padding=15,
                    border_radius=8,
                    border=ft.border.all(1, "#E0E0E0"),
                    width=200,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        payment_method = ft.Ref[ft.RadioGroup]()

        # Lista de métodos de pago con mejor diseño
        payment_methods = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("MÉTODO DE PAGO", 
                            size=14, 
                            color="#1565C0", 
                            weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.RadioGroup(
                                ref=payment_method,
                                content=ft.Column(
                                    controls=[
                                        ft.Radio(value="EFECTIVO", label="EFECTIVO",
                                                fill_color="#2E7D32"),
                                        ft.Radio(value="VISA", label="VISA",
                                                fill_color="#1565C0"),
                                        ft.Radio(value="MASTERCARD", label="MASTERCARD",
                                                fill_color="#E53935"),
                                        ft.Radio(value="AMEX", label="AMEX",
                                                fill_color="#1565C0"),
                                        ft.Radio(value="CHEQUE", label="CHEQUE",
                                                fill_color="#795548"),
                                    ],
                                ),
                            ),
                            bgcolor="white",
                            border=ft.border.all(1, "#E0E0E0"),
                            border_radius=8,
                            padding=10,
                        )
                    ],
                ),
            )

        # Modificar la función process_payment para incluir el método de pago
        def process_payment():
            selected_method = payment_method.current.value
            # Aquí puedes usar selected_method para guardar el método de pago
            # junto con los demás datos de la venta
            self.cart = {}
            self.update_cart_display()
            close_dlg()

        # Botones de acción con mejor diseño
        action_buttons = ft.Row(
            controls=[
                process_button := ft.ElevatedButton(
                    "REGISTRAR VENTA",
                    icon=ft.icons.POINT_OF_SALE,
                    style=ft.ButtonStyle(
                        bgcolor={"": "#2E7D32"},
                        color={"": "white"},
                    ),
                    on_click=lambda _: process_payment(),
                    height=50,
                ),
                ft.ElevatedButton(
                    "CANCELAR",
                    icon=ft.icons.CANCEL,
                    style=ft.ButtonStyle(
                        bgcolor={"": "#C62828"},
                        color={"": "white"},
                    ),
                    on_click=lambda _: close_dlg(),
                    height=50,
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=20,
        )

        # Contenido del diálogo
        dlg_content = ft.Container(
            content=ft.Column(
                controls=[
                    amounts_row,
                    ft.Divider(height=1, color="#E0E0E0"),
                    ft.Row(
                        controls=[payment_methods],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=1, color="#E0E0E0"),
                    action_buttons,
                ],
                spacing=20,
            ),
            padding=30,
            width=800,
        )

        # Diálogo modal
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Registro de Venta", 
                        size=20, 
                        weight=ft.FontWeight.BOLD,
                        color="#1565C0"),
            content=dlg_content,
        )

        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()
        # Hacer focus en el campo de monto recibido
        received_field.focus()
        self.page.update()


    

def main(page: ft.Page):
    app = SalesView(page)

ft.app(target=main)
