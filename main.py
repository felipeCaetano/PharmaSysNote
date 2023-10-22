from datetime import datetime

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
            text_align=TextAlign.LEFT,
            hint_text="Digite ou Pesquise",
            suffix=IconButton(icon=icons.SEARCH,
                              on_click=self.app.search_item_clicked),
            on_change=self.app.searchbox_changed,
            expand=True
        )

    def build(self):
        self.view = Row(width=self.app.page.window_width // 1.5,
                        controls=[self.search_field,
                                  FloatingActionButton(
                                      icon=icons.ADD,
                                      on_click=self.app.add_clicked
                                  )],
                        )
        return self.view


class Anotation(UserControl):
    def __init__(self, task_save, task_edit, task_delete, field_change):
        super(Anotation, self).__init__()
        self.item_value = Text()
        self.item_presentation = Text()
        self.item_count = Text()
        self.item_name = Text()
        self.timestamp = Text()
        self.item_name_field = TextField(label="Nome do Produto")
        self.item_count_field = TextField(
            label="Quantidade",
            keyboard_type=KeyboardType.NUMBER,
            width=150,
            on_change=self.field_change)
        self.item_value_field = TextField(
            label="valor",
            keyboard_type=KeyboardType.NUMBER,
            width=150,
            on_change=self.field_change)
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
        self.field_change = field_change
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

        self.edit_view = Row(  # NOQA
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
        return Row(controls=[self.view, self.saved_view, self.edit_view], expand=True)

    def field_change(self, e):
        self.field_change(self, e)

    def add_clicked(self, e):
        ...

    def delete_clicked(self, e):
        self.task_delete(self)

    def edit_clicked(self, e):
        self.task_edit(self)

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
                        ft.PopupMenuItem(
                            icon=icons.PIE_CHART, text="Relatórios"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            icon=icons.SETTINGS, text="Configurações"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=icons.HELP, text="Ajuda"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=icons.INFO, text="Sobre"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=icons.LOGOUT, text="Logout"),
                    ]
                )
            ]
        )
        self.anotation_name = ''
        self.anotation_count = 0
        self.anotation_value = 0
        self.anotation_presentation = ''
        self.page.update()

    def build(self):
        self.filter = Tabs(  # NOQA
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="Segunda"), Tab(text='Terça'), Tab(text='Quarta'),
                  Tab(text="Quinta"), Tab(text='Sexta'), Tab(text='Sábado'),
                  Tab(text="Domingo")]
        )
        self.filter.selected_index = self.get_tab_day()
        for i in range(self.filter.selected_index+1, 7):
            print(i)
            self.filter.tabs[i].disabled = True

        self.anotations = Column()  # NOQA
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
            # on_change=lambda e: print("Selected destination:",
            #                           e.control.selected_index),
        )
        self.search = SearchField(self)  # NOQA
        self.view = Row(  # NOQA
            controls=[
                rail,
                ft.VerticalDivider(width=1),
                Column([self.filter, self.search, self.anotations])
            ],
            expand=True
        )
        return self.view

    def search_item_clicked(self, e):
        print('pesquisando...')

    def searchbox_changed(self, e):
        self.search.search_field.value = e.control.value

    def add_clicked(self, e):
        anotacao = Anotation(
            self.anotation_save, self.anotation_edit, self.anotation_delete,
            self.field_change)
        anotacao.item_name_field.value = self.search.search_field.value
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
                content=ft.Text("Por favor,  CONFIRME:"),
                bgcolor=ft.colors.BLUE_GREY_200,
                padding=0,
                expand=True,
                border_radius=0,
                border=ft.border.all(1, ft.colors.BLUE_GREY_200)),
            content=ft.Text("Você realmente deseja deletar esse item?"),
            actions=[
                ft.TextButton("Sim", on_click=delete_anotation),
                ft.TextButton("Não", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            title_padding=1,
        )
        self.page.dialog = dlg_modal
        self.page.dialog.open = True
        self.page.update()

    def anotation_edit(self, anotation: Anotation):
        anotation.view.visible = True
        anotation.saved_view.visible = False
        anotation.update()
        item_name = anotation.item_name_field.value
        item_count = anotation.item_count_field.value
        item_value = anotation.item_value_field.value
        item_presentation = anotation.item_presentation_field.value
        self.anotation_name = anotation.item_name_field.value
        self.anotation_count = anotation.item_count_field.value
        self.anotation_value = anotation.item_value_field.value
        self.anotation_presentation = anotation.item_presentation_field.value
        anotation.item_name_field = TextField(
            label="Nome do Produto",
            value=item_name)
        anotation.item_count_field = TextField(label="Quantidade",
                                               value=item_count,
                                               width=150)
        anotation.item_value_field = TextField(label="valor",
                                               value=item_value,
                                               width=150)
        # anotation.item_presentation_field = ft.Dropdown(value=item_presentation_field, width=150)
        anotation.view.controls = [
            anotation.item_name_field, anotation.item_count_field,
            anotation.item_presentation_field, anotation.item_value_field]
        anotation.edit_view.controls[0].controls[0].visible = True
        anotation.edit_view.update()
        anotation.view.update()
        self.page.update()

    def field_change(self, anotation: Anotation, event):
        print(anotation.controls)
        print(event.control)

    def anotation_save(self, annotation: Anotation):
        if ("" != annotation.item_value_field.value
                and annotation.item_name_field.value != ""
                and annotation.item_count_field.value != ""
                and annotation.item_presentation_field.value is not None):

            item_name = annotation.item_name_field.value
            item_count = annotation.item_count_field.value
            item_value = annotation.item_value_field.value
            item_presentation = annotation.item_presentation_field.value
            if self.anotation_name != item_name:
                print("entrei no iff")
                print(f"{self.anotation_name=}, {item_name=}")
            elif (self.anotation_value != item_value
                  or self.anotation_count != item_count):
                print('entrei no elif')
                try:
                    item_value = float(item_value.replace(',', '.'))
                    item_value *= int(item_count)
                except ValueError:
                    print("deu errado nos numeros")
                    item_value = annotation.item_value_field.value
                    item_count = annotation.item_count_field.value
            annotation.item_name_field = Text(f'{item_name}')
            annotation.timestamp.value = self.get_timestamp()
            annotation.item_name.value = item_name
            annotation.item_count_field = Text(f'{item_count}')
            annotation.item_count.value = item_count
            annotation.item_value_field = Text(f'{float(item_value):.2f}')
            annotation.item_value.value = f'{float(item_value):.2f}'
            annotation.item_presentation.value = item_presentation
            annotation.view.controls = [
                annotation.item_name, annotation.item_count,
                annotation.item_presentation,
                annotation.item_value]
            annotation.edit_view.controls[0].controls[0].visible = False
            self.anotation_name = annotation.item_name_field.value
            self.anotation_count = annotation.item_count_field.value
            self.anotation_value = annotation.item_value_field.value
            annotation.edit_view.update()
            # annotation.view.update()
            annotation.view.visible = False
            annotation.saved_view.visible = True
            annotation.update()
            self.page.update()
        else:
            dlg = ft.AlertDialog(title=ft.Text("Preencher todos os campos!"))
            self.page.dialog = dlg
            self.page.dialog.open = True
            self.page.update()

    def tabs_changed(self, e):
        ...

    def get_timestamp(self):
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
        return timestamp

    def get_tab_day(self):
        now = datetime.now()
        return now.weekday()



def main(page: ft.Page):
    page.title = "PharmaSys"
    page.horizontal_alignment = "center"
    page.update()
    app = PharmaSysNoteApp(page)
    page.add(Row([app], expand=True))


ft.app(target=main)
