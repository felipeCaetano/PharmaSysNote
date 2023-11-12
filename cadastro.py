import flet
from flet_core import (Card, animation, Container, transform, Column, Row,
                       Text, IconButton, FilledButton, TextField, RadioGroup,
                       Radio, alignment, MainAxisAlignment, Dropdown, dropdown,
                       AnimationCurve, FontWeight)


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
        self.product_generic = RadioGroup(content=Column([Text("Medicamento Genérico:"),
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
            offset=transform.Offset(2, 0),
            animate_offset=animation.Animation(
                500, curve=AnimationCurve.EASE_IN),
            elevation=30,
            content=Container(
                margin=10,
                padding=12,
                alignment=alignment.center,
                bgcolor="green200",
                content=Column([
                    Row([
                        Text("Novo Cadastro", size=20, weight=FontWeight.BOLD),
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
        return inputcon