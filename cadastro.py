import flet
from flet_core import (alignment, Animation, AnimationCurve, Card,
                       colors, Column, Container, Dropdown, dropdown,
                       FilledButton,
                       FontWeight, IconButton, icons, MainAxisAlignment, Radio,
                       RadioGroup, Row, Text, TextField, transform)

from appstrings import (DESCRIPTION, GENERIC_DRUG, LOTE, MANUFACTURER, NAME,
                        NO, PRESENTATION, Presentations, PRICE,
                        PRODUCT_CODE, SAVE, TOTAL_IN_STOCK, VALID_DATE, YES)


class Cadastro(flet.UserControl):
    def __init__(self, save_fn, close_fn, title):
        super(Cadastro, self).__init__()
        self.title = title
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
        self.inputcon = Card(
            offset=transform.Offset(0, 0),
            animate_offset=Animation(500, curve=AnimationCurve.EASE_IN),
            elevation=30,
            content=Container(
                margin=10,
                padding=12,
                alignment=alignment.center,
                bgcolor=colors.GREEN_100,
                content=Column(
                    [
                        Row([
                            Text(self.title, size=20, weight=FontWeight.BOLD),
                            IconButton(
                                icon=icons.CLOSE, icon_size=30, data=self,
                                on_click=self.close
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

    def build(self):
        return self.inputcon


class Alterador(Cadastro):
    def __init__(self, save_fn, close_fn, title):
        super().__init__(save_fn, close_fn, title)
        self.prod_code.suffix = IconButton(icon=icons.SEARCH, icon_size=17)
        self.prod_code.dense = True
        self.product_name.text_size = 18
        self.prod_code.content_padding = self.product_name.content_padding
        self.product_lote.text_size = 18
        self.product_lab.cursor_height = 18
        self.product_date.text_size = 18
        self.product_info.text_size = 18
        self.product_presentation.text_size = 18
        self.product_total_cnt.text_size = 18
        self.product_price.text_size = 18
        self.inputcon.content.content.controls[0].controls[1].data = self
