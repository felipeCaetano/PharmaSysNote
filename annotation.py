import flet as ft
from flet_core import (UserControl, Text, TextField, KeyboardType, Column, Row,
                       MainAxisAlignment, CrossAxisAlignment, IconButton,
                       icons, colors,
                       ControlEvent)


class Anotation(UserControl):
    def __init__(self, task_save, task_edit, task_delete):
        super(Anotation, self).__init__()
        self.item_value = Text()
        self.item_presentation = Text()
        self.item_count = Text()
        self.item_name = Text()
        self.timestamp = Text()
        self.item_name_field = TextField(label="Nome do Produto")
        self.item_count_field = TextField(label="Quantidade",
                                          keyboard_type=KeyboardType.NUMBER,
                                          width=150)
        self.item_value_field = TextField(label="valor",
                                          keyboard_type=KeyboardType.NUMBER,
                                          width=150)
        self.item_presentation_field = ft.Dropdown(
            label="Apresentação",
            hint_text="Apresentação",
            options=[
                ft.dropdown.Option("unidade"),
                ft.dropdown.Option("cartela"),
                ft.dropdown.Option("caixa"),
            ],
            autofocus=False,
            width=150
        )
        self.task_save = task_save
        self.task_edit = task_edit
        self.task_delete = task_delete
        self.value_changed = False
        self.item_changed = False

    def build(self):
        self.anotacoes = Column()  # NOQA
        self.view = Row(controls=[  # NOQA
            self.item_name_field,
            self.item_count_field,
            self.item_presentation_field,
            self.item_value_field
        ])
        self.saved_view = Row(controls=[  # NOQA
            self.timestamp,
            self.item_name,
            self.item_count,
            self.item_presentation,
            self.item_value
        ],
            visible=False)

        self.control_buttons = self.create_control_buttons()    # NOQA
        return Row(controls=[self.view, self.saved_view, self.control_buttons],
                   expand=True)

    def create_control_buttons(self):
        return Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.DONE_OUTLINE_OUTLINED,
                            icon_color=colors.GREEN,
                            tooltip="Confirmar",
                            on_click=self.save_clicked,
                        ),
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Editar",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Apagar",
                            on_click=self.delete_clicked)
                    ],
                )
            ]
        )

    def add_clicked(self, e):
        ...

    def delete_clicked(self, e):
        self.task_delete(self)

    def edit_clicked(self, e):
        self.task_edit(self)

    def save_clicked(self, e: ControlEvent):
        self.task_save(self)
