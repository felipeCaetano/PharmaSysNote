import flet as ft
from flet_core import (
    IconButton, UserControl, TextField, Row, MainAxisAlignment,
    CrossAxisAlignment, icons, colors, Column, Tabs, Tab, FloatingActionButton,
    Page, KeyboardType, TextAlign, Text)


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


class Anotation(UserControl):
    def __init__(self, task_save, task_delete):
        super(Anotation, self).__init__()
        self.item_name = TextField(hint_text="nome do produto")
        self.item_count = TextField(hint_text="quantidade",
                                    keyboard_type=KeyboardType.NUMBER,
                                    width=150)
        self.item_value = TextField(hint_text="valor",
                                    keyboard_type=KeyboardType.NUMBER,
                                    width=150)
        self.task_save = task_save
        self.task_delete = task_delete

    def build(self):
        self.anotacoes = Column()
        self.view = Row(controls=[
            self.item_name, self.item_count, self.item_value
        ])
        self.edit_view = Row(
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

        return Row(
            controls=[self.view, self.edit_view],
            expand=True)

    def add_clicked(self, e):
        ...

    def delete_clicked(self, e):
        self.task_delete(self)

    def edit_clicked(self, e):
        ...

    def save_clicked(self, e):
        self.task_save(self)


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
        anotacao = Anotation(self.task_save, self.anotation_delete)
        anotacao.item_name.value = self.search.search_field.value
        self.anotations.controls.append(anotacao)
        self.anotations.update()
        self.page.update()

    def anotation_delete(self, anotation):
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

        def delete_anotation(e):
            dlg_modal.open = False
            self.anotations.controls.remove(anotation)
            self.update()
            self.page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                content=ft.Text("Por favor Confirme:"),
                bgcolor=ft.colors.BLUE_GREY_200,
                padding=0,
                expand=True,
                border_radius=0,
                border=ft.border.all(1, ft.colors.BLUE_GREY_200)
            ),  # ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete these item?"),
            actions=[
                ft.TextButton("Yes", on_click=delete_anotation),
                ft.TextButton("No", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            title_padding=1,
        )
        self.page.dialog = dlg_modal
        self.page.dialog.open = True
        self.page.update()

    def task_save(self, anotation: Anotation):
        if (anotation.item_value.value is not ""
                and anotation.item_name.value is not ""
                and anotation.item_count.value is not ""):
            item_name = anotation.item_name.value
            item_count = anotation.item_count.value
            item_value = anotation.item_value.value
            try:
                item_value = float(item_value.replace(',', '.'))
                item_value *= int(item_count)
            except ValueError:
                print("deu errado nos numeros")
                item_value = anotation.item_value.value
                item_count = anotation.item_count.value
            anotation.item_name = Text(str(item_name))
            anotation.item_count = Text(str(item_count))
            anotation.item_value = Text(str(item_value))
            anotation.view.controls = [anotation.item_name,
                                       anotation.item_count,
                                       anotation.item_value]
            anotation.edit_view.controls[0].controls[0].visible = False
            anotation.edit_view.update()
            anotation.view.update()
            self.page.update()
        else:
            dlg = ft.AlertDialog(
                title=ft.Text("Preencher todos os campos!"),
            )
            self.page.dialog = dlg
            self.page.dialog.open = True
            self.page.update()

    def tabs_changed(self, e):
        ...


def main(page: ft.Page):
    page.title = "PharmaSys"
    page.horizontal_alignment = "center"
    page.update()
    app = PharmaSysNoteApp(page)
    page.add(Row([app], expand=True))


ft.app(target=main)
