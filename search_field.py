from flet_core import (colors, FloatingActionButton, IconButton, icons, Row, TextAlign,
                       TextField, UserControl, Container, CrossAxisAlignment, Icon, border_radius)

from appstrings import SEARCH_FIELD


def search_field(function):
    return TextField(
        expand=True,
        border_color=colors.SHADOW,
        height=40,
        text_size=20,
        content_padding=10,
        cursor_color=colors.BLACK,
        cursor_width=2,
        color=colors.BLACK,
        hint_text='Pesquisar',
        suffix=IconButton(icon=icons.SEARCH, on_click=function),
        # on_change=function
    )


def search_bar(control):
    return Container(
        width=350,
        bgcolor=colors.WHITE10,
        border_radius=6,
        opacity=0,
        animate_opacity=300,
        padding=8,
        content=Row(
            spacing=10,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Icon(
                    name=icons.SEARCH_ROUNDED,
                    size=17,
                    opacity=.85,
                ),
                control,
            ],
        ),
    )


class SearchBar(Container):
    def __init__(self, callback):
        super().__init__()
        self.datable = None
        self.search_field_value = search_field(self.filter_dt_rows)
        self.height = 60
        self.bgcolor = colors.PRIMARY_CONTAINER
        self.padding = 15
        self.border_radius = border_radius.only(top_left=10, top_right=10)
        self.opacity = 1
        self.animate_opacity = 300
        self.padding = 12
        self.content = Row(
            spacing=15,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[self.search_field_value, FloatingActionButton(icon=icons.ADD, on_click=callback)],
        )

    def filter_dt_rows(self, e):
        """
        função para pesquisar sobre a base de dados quando o botão de lupa for clicado
        :param e:
        :return:
        """
        # for data_rows in self.datable.rows:
        #     data_cell = data_rows.cells[0]
        #     data_rows.visible = (
        #         True
        #         if e.control.value.lower() in data_cell.content.value.lower()
        #         else False
        #     )
        #
        #     data_rows.update()
        print('pesquisa no banco')


class SearchField(UserControl):
    def __init__(self, callback, search_engine):
        super(SearchField, self).__init__()
        self.view = Row()
        self.callback = callback
        self.search_function = search_engine
        self.search_field = TextField(
            text_align=TextAlign.LEFT,
            hint_text=SEARCH_FIELD,
            expand=True,
            suffix=IconButton(icon=icons.SEARCH, on_click=self.search_function),
        )

    def build(self):
        self.search_field.suffix.data = self.search_field.value
        self.view.controls.append(self.search_field)
        self.view.controls.append(
            FloatingActionButton(icon=icons.ADD, on_click=self.callback)
        )
        return self.view
