import flet
from flet_core import Card, animation, Container, transform, Column, Row, Text, \
    IconButton, FilledButton, Page, TextField


class Cadastro(flet.UserControl):
    def __init__(self):
        super(Cadastro, self).__init__()

    def build(self):
        inputcon = Card(
            offset=transform.Offset(0, 0),
            animate_offset=animation.Animation(600, curve="easeIn"),
            elevation=30,
            content=Container(
                bgcolor="green200",
                content=Column([
                    Row([
                        Text("Novo Cadastro", size=20, weight="bold"),
                        IconButton(icon="close", icon_size=30,
                                   on_click=None)
                    ]),
                    Row([TextField(), TextField()]),
                    FilledButton("Salvar", on_click=None)
                ]
                )
            ))

        return inputcon
            # Card(
            # offset=transform.Offset(2, 0),
            # animate_offset=animation.Animation(600, curve="easeIn"),
            # elevation=30,
            # content=Container(
            #     bgcolor="green200",
            #     content=Row(
            #         [Text("Cadastro de Produtos", size=20, weight="bold"),
            #          IconButton(icon="close", icon_size=30, on_click=None)])
            # ),
            # expand=True)



