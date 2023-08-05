import flet as ft
from flet_core import (
    IconButton, UserControl, TextField, Row, MainAxisAlignment,
    CrossAxisAlignment, icons, colors, Column, Tabs, Tab, FloatingActionButton,
    Page, KeyboardType, TextAlign)


class SearchField(UserControl):
    def __init__(self, app):
        super(SearchField, self).__init__()
        self.app = app
        self.search_field = TextField(
            text_align=TextAlign.CENTER,
            hint_text="Digite ou Pesquise",
            suffix=IconButton(icon=icons.SEARCH,
                              on_click=self.app.search_item_clicked),
            on_change=self.app.searchbox_changed,
            expand=True
        )

    def build(self):
        self.view = Column(
            width=800,
            controls=[
                Row(controls=[
                    self.search_field,
                    FloatingActionButton(
                        icon=icons.ADD, on_click=self.app.add_clicked)])
            ])
        return self.view


class Anotacao(UserControl):
    def __init__(self, task_delete):
        super(Anotacao, self).__init__()
        self.item_name = TextField(hint_text="nome do produto")
        self.item_count = TextField(hint_text="quantidade",
                                    keyboard_type=KeyboardType.NUMBER,
                                    width=150)
        self.item_value = TextField(hint_text="valor",
                                    keyboard_type=KeyboardType.NUMBER,
                                    width=150)
        self.task_delete = task_delete

    def build(self):
        self.anotacoes = Column()
        self.view = Row(controls=[
            self.item_name, self.item_count, self.item_value
        ])
        self.edit_name = TextField()
        self.display_view = Row(
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

        self.edit_view = Row(
            visible=False,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Atualizar",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return Row(
            controls=[self.view, self.display_view],
            expand=True)

    def add_clicked(self, e):
        ...

    def delete_clicked(self, e):
        self.task_delete(self)

    def edit_clicked(self, e):
        ...

    def save_clicked(self, e):
        self.item_name.read_only = True
        self.item_value.read_only = True
        self.item_count.read_only = True
        self.update()


class PharmaSysNoteApp(UserControl):
    def __init__(self, page: Page):
        super(PharmaSysNoteApp, self).__init__()
        self.page = page
        self.page.appbar = ft.AppBar(
            leading=ft.Icon(icons.CREATE),
            leading_width=40,
            title=ft.Text("Anotador do PharmaSys"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(icon=icons.LOGIN, text="Login"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(icon=icons.PIE_CHART,
                                         text="Relatórios"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=icons.SETTINGS,
                                         text="Configurações"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=icons.HELP, text="Ajuda"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=icons.INFO, text="Sobre"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=icons.LOGOUT, text="Logout"),
                    ]
                ),
            ],
        )
        self.page.update()

    def build(self):
        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="Segunda"), Tab(text='Terça'), Tab(text='Quarta'),
                  Tab(text="Quinta"), Tab(text='Sexta'), Tab(text='Sábado'),
                  Tab(text="Domingo")]
        )
        self.anotations = Column()
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            # extended=True,
            min_width=100,
            min_extended_width=400,
            leading=ft.FloatingActionButton(icon=ft.icons.LOCAL_PHARMACY,
                                            text="PharmaSys"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.CREATE,
                    selected_icon=ft.icons.CREATE_OUTLINED,
                    icon_content=IconButton(),
                    label="Anotações"
                ),
            ],
            on_change=lambda e: print("Selected destination:",
                                      e.control.selected_index),
        )
        self.search = SearchField(self)
        self.view = Row(
            controls=[
                rail,
                ft.VerticalDivider(width=1),
                Column([self.filter, SearchField(self), self.anotations])
            ],
            expand=True
        )
        return self.view

    def search_item_clicked(self, e):
        print('pesquisando...')

    def searchbox_changed(self, e):
        self.search.search_field.value = e.control.value

    def add_clicked(self, e):
        anotacao = Anotacao(self.anotation_delete)
        anotacao.item_name.value = self.search.search_field.value
        self.anotations.controls.append(anotacao)
        self.anotations.update()
        self.page.update()

    def anotation_delete(self, anotation):
        self.anotations.controls.remove(anotation)
        self.update()

    def tabs_changed(self, e):
        ...


def main(page: ft.Page):
    page.title = "PharmaSys"
    page.horizontal_alignment = "center"
    page.update()
    app = PharmaSysNoteApp(page)
    page.add(Row([app], expand=True))


ft.app(target=main)
