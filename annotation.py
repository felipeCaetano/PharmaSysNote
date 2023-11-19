import flet as ft
from flet_core import (colors, Column, ControlEvent, CrossAxisAlignment,
                       IconButton, icons, KeyboardType, MainAxisAlignment, Row,
                       Text, TextField, UserControl)

from appstrings import (CONFIRM, DELETE, PRESENTATION, Presentations,
                        PRODUCT_NAME, QUANTITY, VALUE)


class Annotation(UserControl):
    def __init__(self, task_save, task_edit, task_delete):
        super(Annotation, self).__init__()
        self.view = Row()
        self.item_value = Text()
        self.item_presentation = Text()
        self.item_count = Text()
        self.item_name = Text()
        self.timestamp = Text()
        self.item_name_field = TextField(label=PRODUCT_NAME)
        self.item_count_field = TextField(
            label=QUANTITY, keyboard_type=KeyboardType.NUMBER, width=150
        )
        self.item_value_field = TextField(
            label=VALUE, keyboard_type=KeyboardType.NUMBER, width=150
        )
        self.item_presentation_field = ft.Dropdown(
            label=PRESENTATION,
            options=[ft.dropdown.Option(x.value) for x in Presentations],
            autofocus=False,
            width=150,
        )
        self.task_save = task_save
        self.task_edit = task_edit
        self.task_delete = task_delete
        self.value_changed = False
        self.item_changed = False
        self.anotacoes = Column()

    def build(self):
        self.view.controls = [
            self.item_name_field,
            self.item_count_field,
            self.item_presentation_field,
            self.item_value_field,
        ]
        self.control_buttons = self.create_control_buttons()  # NOQA
        return Row(controls=[self.view, self.control_buttons], expand=True)

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
                            tooltip=CONFIRM,
                            on_click=self.save_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip=DELETE,
                            on_click=self.delete_clicked,
                        ),
                    ],
                )
            ],
        )

    def add_clicked(self, event):
        ...

    def delete_clicked(self, event):
        self.task_delete(self)

    def edit_clicked(self, event):
        self.task_edit(self)

    def save_clicked(self, event: ControlEvent):
        self.task_save(self)
