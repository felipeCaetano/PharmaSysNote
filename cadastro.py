import flet
from flet_core import (
    Card, animation, Container, transform, Column, Row, Text, IconButton,
    FilledButton, TextField, RadioGroup, Radio, alignment, MainAxisAlignment,
    Dropdown, dropdown)


class Cadastro(flet.UserControl):
    def __init__(self, save_fn, close_fn):
        super(Cadastro, self).__init__()
        self.save = save_fn
        self.close = close_fn
        self.product_presentation = Dropdown(
            label="Apresentação",
            hint_text="Apresentação",
            options=[
                dropdown.Option("unidade"),
                dropdown.Option("cartela"),
                dropdown.Option("caixa")
            ],
            autofocus=False,
            width=150
        )
        self.product_lote = TextField(label="Lote:")
        self.product_date = TextField(label="Validade:")
        self.product_generic = RadioGroup(
            content=Column([Text("Medicamento Genérico:"),
                            Radio(value='S', label="Sim"),
                            Radio(value='N', label="Não")
                            ]))
        self.product_price = TextField(label="Preço:")
        self.product_total_cnt = TextField(label="Total em Estoque:")
        self.product_lab = TextField(label="Fabricante:")
        self.product_info = TextField(label="Descrição:")
        self.product_name = TextField(label="Nome:")
        self.product_code = TextField(label="Código:")

    def build(self):
        inputcon = Card(
            offset=transform.Offset(-2, 0),
            animate_offset=animation.Animation(500, curve="easeIn"),
            elevation=10,
            content=Container(
                margin=10,
                padding=12,
                alignment=alignment.center,
                bgcolor="green200",
                content=Column([
                    Row([
                        Text("Novo Cadastro", size=20, weight="bold"),
                        IconButton(icon="close", icon_size=30,
                                   on_click=self.close)
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Row([self.product_code, self.product_name,
                         self.product_lote]),
                    Row([self.product_info, self.product_lab,
                         self.product_total_cnt]),
                    Row([self.product_price, self.product_generic,
                         self.product_presentation, self.product_date]),
                    FilledButton("Salvar", on_click=self.save)
                ],
                    spacing=50
                )
            ))
        self.offset = inputcon.offset
        return inputcon


product_presentation = Dropdown(label="Apresentação", hint_text="Apresentação",
                                options=[
                                    dropdown.Option("unidade"),
                                    dropdown.Option("cartela"),
                                    dropdown.Option("caixa")
                                ],
                                autofocus=False,
                                width=150
                                )
product_lote = TextField(label="Lote:")
product_date = TextField(label="Validade:")
product_generic = RadioGroup(content=Column([Text("Medicamento Genérico:"),
                                             Radio(value='S', label="Sim"),
                                             Radio(value='N', label="Não")
                                             ]))
product_price = TextField(label="Preço:")
product_total_cnt = TextField(label="Total em Estoque:")
product_lab = TextField(label="Fabricante:")
product_info = TextField(label="Descrição:")
product_name = TextField(label="Nome:")
product_code = TextField(label="Código:")

save_button = FilledButton("Salvar")
close_button = IconButton(icon="close", icon_size=30)
inputcon = Card(
    offset=transform.Offset(-2, -2),
    animate_offset=animation.Animation(500, curve="easeIn"),
    elevation=30,
    content=Container(
        margin=10,
        padding=12,
        alignment=alignment.center,
        bgcolor="green200",
        content=Column([
            Row([
                Text("Novo Cadastro", size=20, weight="bold"),
                close_button
            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            Row([product_code, product_name, product_lote]),
            Row([product_info, product_lab, product_total_cnt]),
            Row([product_price, product_generic, product_presentation,
                 product_date]),
            save_button
        ],
            spacing=50
        )
    ))
