import flet as ft
from decimal import Decimal

class SalesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "POS - Dulcería La Rosa"
        self.page.padding = 0
        self.page.theme_mode = "light"
        self.page.window_bgcolor = "#FFFFFF"
        
        # Diccionario para almacenar los productos en el carrito
        self.cart = {}
        self.total = Decimal('0.00')
        
        # Productos de prueba
        self.test_products = [
            ["BOLIS", "Bolis de Fresa", "5.00", "1", "5.00"],
            ["BOTANA", "Botana MR Saulo", "15.00", "2", "30.00"],
            ["DULCE", "Dulce a Granel", "8.50", "3", "25.50"],
            ["BOLSA", "Bolsa 8x24", "12.00", "1", "12.00"],
        ]

        # Inicializar componentes
        self.initialize_components()
        
    def on_code_submit(self, e):
        
        code = e.control.value.strip().upper()
        
        # Diccionario simulado de productos (esto debería venir de tu base de datos)
        products_db = {
            "BOLIS": {"name": "Bolis de Fresa", "price": 5.00},
            "BOLSA": {"name": "Bolsa 8x24", "price": 12.00},
            "BOTANA": {"name": "Botana MR Saulo", "price": 15.00},
            "DULCE": {"name": "Dulce a Granel", "price": 8.50},
        }
        
        if code in products_db:
            product = products_db[code]
            self.add_product(code, product["name"], product["price"])
        else:
            # Mostrar mensaje de error si el producto no existe
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Producto no encontrado: {code}"),
                    action="Ok"
                )
            )
        
        # Limpiar el campo de entrada
        e.control.value = ""
        self.page.update()

    def initialize_components(self):
        # Modificamos cart_items para que inicie vacío
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
                ft.DataColumn(ft.Text("", size=14)),  # Columna para botón eliminar
            ],
            rows=[],
        )

        self.code_input = ft.TextField(
            label="Código",
            width=200,
            height=35,
            bgcolor="#FFFFFF",
            border_radius=5,
            text_size=14,
            on_submit=self.on_code_submit  # Asegúrate de que esta línea esté presente
        )

        self.total_display = ft.Text(
            value="$ 0.00",
            size=40,
            weight=ft.FontWeight.BOLD,
            color="#000000",
        )

    def add_product(self, code, name, price):
        if code in self.cart:
            self.cart[code]['quantity'] += 1
        else:
            self.cart[code] = {
                'name': name,
                'price': Decimal(str(price)),
                'quantity': 1
            }
        
        self.update_cart_display()

    def remove_product(self, code):
        if code in self.cart:
            del self.cart[code]
            self.update_cart_display()

    def update_quantity(self, code, new_quantity):
        if code in self.cart and new_quantity > 0:
            self.cart[code]['quantity'] = new_quantity
            self.update_cart_display()
        elif new_quantity <= 0:
            self.remove_product(code)

    def update_cart_display(self):
        # Actualizar tabla
        new_rows = []
        self.total = Decimal('0.00')
        
        for code, item in self.cart.items():
            subtotal = item['price'] * item['quantity']
            self.total += subtotal
            
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(code)),
                        ft.DataCell(ft.Text(item['name'])),
                        ft.DataCell(ft.Text(f"${item['price']:.2f}")),
                        ft.DataCell(
                            ft.TextField(
                                value=str(item['quantity']),
                                width=50,
                                text_align=ft.TextAlign.CENTER,
                                on_submit=lambda e, c=code: self.update_quantity(c, int(e.control.value))
                            )
                        ),
                        ft.DataCell(ft.Text(f"${subtotal:.2f}")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color="red",
                                on_click=lambda e, c=code: self.remove_product(c)
                            )
                        ),
                    ]
                )
            )
        
        self.cart_items.rows = new_rows
        self.total_display.value = f"$ {self.total:.2f}"
        self.page.update()

    def show_payment_dialog(self, e):
        def close_dlg(e):
            payment_dialog.open = False
            self.page.update()

        def process_payment(e):
            # Lógica para procesar el pago
            self.cart = {}
            self.update_cart_display()
            close_dlg(e)

        def update_received_amount(number):
            current = amount_received.value or "0"
            if number == "." and "." in current:
                return
            if number == "x":  # borrar último dígito
                amount_received.value = current[:-1] if len(current) > 1 else "0"
            else:
                amount_received.value = (current + str(number)) if current != "0" else str(number)
            
            try:
                payment_amount = Decimal(amount_received.value)
                change_amount = payment_amount - self.total
                change_display.value = f"{change_amount:.2f}"
            except:
                change_display.value = "0.00"
            
            self.page.update()

        # Crear los controles principales
        amount_received = ft.TextField(
            value="0.00",
            read_only=True,
            width=200,
            text_size=24,
            text_align=ft.TextAlign.RIGHT,
            bgcolor="#FFFFFF"
        )

        change_display = ft.TextField(
            value="0.00",
            read_only=True,
            width=200,
            text_size=24,
            text_align=ft.TextAlign.RIGHT,
            bgcolor="#FFFFFF"
        )

        # Crear el pad numérico
        numpad = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(text="7", width=50, on_click=lambda e: update_received_amount("7")),
                        ft.ElevatedButton(text="8", width=50, on_click=lambda e: update_received_amount("8")),
                        ft.ElevatedButton(text="9", width=50, on_click=lambda e: update_received_amount("9")),
                        ft.ElevatedButton(text="109.00", width=100),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(text="4", width=50, on_click=lambda e: update_received_amount("4")),
                        ft.ElevatedButton(text="5", width=50, on_click=lambda e: update_received_amount("5")),
                        ft.ElevatedButton(text="6", width=50, on_click=lambda e: update_received_amount("6")),
                        ft.ElevatedButton(text="10", width=100),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(text="1", width=50, on_click=lambda e: update_received_amount("1")),
                        ft.ElevatedButton(text="2", width=50, on_click=lambda e: update_received_amount("2")),
                        ft.ElevatedButton(text="3", width=50, on_click=lambda e: update_received_amount("3")),
                        ft.ElevatedButton(text="20", width=100),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(text="0", width=50, on_click=lambda e: update_received_amount("0")),
                        ft.ElevatedButton(text=".", width=50, on_click=lambda e: update_received_amount(".")),
                        ft.ElevatedButton(text="x", width=50, on_click=lambda e: update_received_amount("x")),
                        ft.ElevatedButton(text="50", width=100),
                    ]
                ),
            ]
        )

        # Lista de métodos de pago
        payment_methods = ft.ListView(
            width=200,
            height=200,
            spacing=2,
            controls=[
                ft.ListTile(title=ft.Text("EFECTIVO"), selected=True),
                ft.ListTile(title=ft.Text("VISA")),
                ft.ListTile(title=ft.Text("MASTERCARD")),
                ft.ListTile(title=ft.Text("AMEX")),
                ft.ListTile(title=ft.Text("CHEQUE")),
            ],
        )

        payment_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Registro Venta"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Fila superior con totales
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text("TOTAL", size=12),
                                        ft.Text(f"{self.total:.2f}", size=24, color="red"),
                                    ],
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Recibido", size=12),
                                        amount_received,
                                    ],
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Saldo", size=12),
                                        change_display,
                                    ],
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        # Fila con pad numérico y métodos de pago
                        ft.Row(
                            controls=[
                                numpad,
                                ft.Column(
                                    controls=[
                                        ft.Text("Modo de Pago"),
                                        payment_methods,
                                    ],
                                ),
                            ],
                        ),
                        # Botones de acción
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Registrar",
                                    icon=ft.icons.PRINT,
                                    on_click=process_payment
                                ),
                                ft.ElevatedButton(
                                    "Cancelar",
                                    icon=ft.icons.CANCEL,
                                    on_click=close_dlg
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                ),
                padding=20,
            ),
        )

        self.page.dialog = payment_dialog
        payment_dialog.open = True
        self.page.update()

    def create_product_buttons(self):
        products = [
            {"code": "BOLIS", "name": "Bolis de Fresa", "price": 29.00},
            {"code": "BOTANA", "name": "BOTANA", "price": 45.00},
            {"code": "DULCE", "name": "Dulce", "price": 12.00},
            {"code": "VASO", "name": "VASO 16", "price": 35.00},
            {"code": "CHOCOLATE", "name": "CHOCOLATE NUGS", "price": 78.00},
            {"code": "PALETA", "name": "PALETA JUMBO", "price": 99.00},
            {"code": "PALOMITAS", "name": "PALOMITAS", "price": 40.00},
        ]
        
        return ft.Container(
        content=ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            spacing=10,
            run_spacing=10,
            controls=[
                ft.ElevatedButton(
                    text=product["name"],
                    style=ft.ButtonStyle(
                        bgcolor="#B3E5FC",
                        color="#000000",
                        shape={"": ft.RoundedRectangleBorder(radius=8)},
                    ),
                    width=140,
                    height=50,
                    on_click=lambda e, p=product: self.add_product(p["code"], p["name"], p["price"])
                ) for product in products
            ],
        ),
        padding=20,
        bgcolor="#F5F5F5",
        height=300,
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
                    # ... otros botones ...
                ],
                spacing=10,
            ),
            padding=20,
        )

    def create_action_button(self, text, icon):
        return ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color="#1565C0"),
                    ft.Text(text, size=14),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            style=ft.ButtonStyle(
                bgcolor="#FFFFFF",
                shape={"": ft.RoundedRectangleBorder(radius=8)},
            ),
            width=160,
            height=45,
        )

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Panel superior con botones de productos
                    self.create_product_buttons(),
                    
                    # Área principal
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                # Área del ticket
                                ft.Column(
                                    controls=[
                                        self.cart_items,
                                        ft.Container(
                                            content=self.code_input,
                                            padding=ft.padding.only(top=10),
                                        ),
                                    ],
                                    expand=True,
                                ),
                                # Botones de acción
                                self.create_action_buttons(),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=20,
                        expand=True,
                    ),
                    
                    # Total
                    ft.Container(
                        content=self.total_display,
                        alignment=ft.alignment.center_right,
                        padding=ft.padding.only(right=40),
                        height=60,
                        bgcolor="#F5F5F5",
                    ),
                ],
                spacing=0,
            ),
            border_radius=10,
            bgcolor="#FFFFFF",
        )
