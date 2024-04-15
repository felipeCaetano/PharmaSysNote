import flet
from flet_core import (alignment, Animation, AnimationCurve, Card,
                       colors, Column, Container, Dropdown, dropdown,
                       FilledButton,
                       FontWeight, IconButton, icons, MainAxisAlignment, Radio,
                       RadioGroup, Row, Text, TextField, transform)

from appstrings import (DESCRIPTION, GENERIC_DRUG, LOTE, MANUFACTURER, NAME,
                        NO, PRESENTATION, Presentations, PRICE,
                        PRODUCT_CODE, SAVE, TOTAL_IN_STOCK, VALID_DATE, YES)
# from pharmasysapp import Controller

form_style = {
    "bgcolor": "white10",
    "border_radius": 8,
    "border": flet.border.all(1, '#ebebeb'),
    "padding": 15,
}


def text_field():
    return flet.TextField(
        border_color="transparent",
        height=20,
        text_size=13,
        content_padding=0,
        cursor_color='black',
        cursor_width=1,
        cursor_height=18,
        color='black'
    )


def text_field_container(expand, name, control):
    return flet.Container(
        expand=expand,
        height=45,
        bgcolor='#ebebeb',
        border_radius=6,
        padding=8,
        content=flet.Column(
            spacing=1,
            controls=[
                flet.Text(
                    value=name,
                    size=9,
                    color='black',
                    width='bold',
                ),
                control
            ]
        )
    )


class Form(flet.Container):
    def __init__(self, controller):
        super().__init__(**form_style)
        # self.datatable = datatable
        self.controller = controller
        self.row1_value = text_field()
        self.row2_value = text_field()
        self.row3_value = text_field()
        self.row4_value = text_field()

        self.row1 = text_field_container(
            True, "Row one", self.row1_value)
        self.row2 = text_field_container(
            3, "Row two", self.row2_value)
        self.row3 = text_field_container(
            1, "Row three", self.row3_value)
        self.row4 = text_field_container(
            1, "Row four", self.row4_value)

        self.submit = flet.ElevatedButton(
            text='Submit',
            style=flet.ButtonStyle(
                shape={"": flet.RoundedRectangleBorder(radius=8)}),
            on_click=self.submit_data
        )

        self.content = flet.Column(
            expand=True,
            controls=[
                flet.Row(controls=[self.row1]),
                flet.Row(controls=[self.row2, self.row3, self.row4]),
                flet.Row(controls=[self.submit], alignment='end'),
            ],
        )

    def submit_data(self, e):
        data = {
            "col1": self.row1_value.value,
            "col2": self.row2_value.value,
            "col3": self.row3_value.value,
            "col4": self.row4_value.value
        }
        # Controller.add_items(data)
        self.controller.add_items(data)
        self.clear_entries()
        # self.datatable.fill_datatable()

    def clear_entries(self):
        self.row1_value.value = ""
        self.row2_value.value = ""
        self.row3_value.value = ""
        self.row4_value.value = ""

        self.content.update()


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
