import flet
from flet_core import (alignment, Animation, AnimationCurve, Card,
                       Column, Container, Dropdown, dropdown, FilledButton,
                       FontWeight, IconButton, MainAxisAlignment, Radio,
                       RadioGroup, Row, Text, TextField, transform)

from appstrings import (DESCRIPTION, GENERIC_DRUG, LOTE, MANUFACTURER, NAME,
                        NEW_REGISTER, NO, PRESENTATION, Presentations, PRICE,
                        PRODUCT_CODE, SAVE, TOTAL_IN_STOCK, VALID_DATE, YES)


class Cadastro(flet.UserControl):
    def __init__(self, save_fn, close_fn):
        super(Cadastro, self).__init__()
        self.save = save_fn
        self.close = close_fn
        self.product_presentation = Dropdown(
            label=PRESENTATION,
            options=[dropdown.Option(x.value) for x in Presentations],
            autofocus=False,
            width=150,
        )
        self.product_lote = TextField(label=LOTE)
        self.product_date = TextField(label=VALID_DATE)
        self.product_generic = RadioGroup(
            content=Column(
                [
                    Text(GENERIC_DRUG),
                    Radio(value="S", label=YES),
                    Radio(value="N", label=NO),
                ]
            )
        )
        self.product_price = TextField(label=PRICE)
        self.product_total_cnt = TextField(label=TOTAL_IN_STOCK)
        self.product_lab = TextField(label=MANUFACTURER)
        self.product_info = TextField(label=DESCRIPTION)
        self.product_name = TextField(label=NAME)
        self.prod_code = TextField(label=PRODUCT_CODE)

    def build(self):
        inputcon = Card(
            offset=transform.Offset(0, 0),
            animate_offset=Animation(500, curve=AnimationCurve.EASE_IN),
            elevation=30,
            content=Container(
                margin=10,
                padding=12,
                alignment=alignment.center,
                bgcolor="green200",
                content=Column(
                    [
                        Row([
                            Text(NEW_REGISTER, size=20, weight=FontWeight.BOLD),
                            IconButton(
                                icon="close", icon_size=30, on_click=self.close
                            ),
                        ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row([
                            self.prod_code,
                            self.product_name,
                            self.product_lote
                        ]),
                        Row([
                            self.product_info,
                            self.product_lab,
                            self.product_total_cnt
                        ]),
                        Row([
                            self.product_price,
                            self.product_generic,
                            self.product_presentation,
                            self.product_date
                        ]),
                        FilledButton(SAVE, on_click=self.save),
                    ],
                    spacing=50,
                ),
            ),
        )
        return inputcon
