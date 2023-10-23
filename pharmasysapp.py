from datetime import datetime

import flet as ft
from flet_core import (
    UserControl, Page, icons, Tabs, Tab, Column, IconButton, Row, TextField)

from annotation import Anotation
from search_field import SearchField


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
            actions=self.create_popupmenubuttons()
        )
        self.anotation_name = ''
        self.anotation_count = 0
        self.anotation_value = 0
        self.anotation_presentation = ''

    def create_popupmenubuttons(self):
        return [
            ft.PopupMenuButton(
                items=[
                    self.create_menu_item(icons.LOGIN, "Login"),
                    self.create_menu_item(),  # divider
                    self.create_menu_item(icons.PIE_CHART, "Relatórios"),
                    self.create_menu_item(),
                    self.create_menu_item(icons.SETTINGS, "Configurações"),
                    self.create_menu_item(),
                    self.create_menu_item(icons.HELP, "Ajuda"),
                    self.create_menu_item(),
                    self.create_menu_item(icons.INFO, "Sobre"),
                    self.create_menu_item(),
                    self.create_menu_item(icons.LOGOUT, "Logout"),
                ]
            )
        ]

    def create_menu_item(self, icon=None, text=""):
        if not icon and not text:
            return ft.PopupMenuItem()
        return ft.PopupMenuItem(icon=icon, text=text)

    def build(self):
        self.anotations = Column()  # NOQA
        self.filter = Tabs(  # NOQA
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="Segunda"), Tab(text='Terça'), Tab(text='Quarta'),
                  Tab(text="Quinta"), Tab(text='Sexta'), Tab(text='Sábado'),
                  Tab(text="Domingo")]
        )
        self.filter.selected_index = self.get_tab_day()
        # for i, tab in enumerate(self.filter.tabs):
        #     print(tab.text)
        #     tab.content = Column(controls=[SearchField(self), self.anotations])


        self.search = SearchField(self)  # NOQA
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
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

    def anotation_edit(self, line: Anotation):
        line.view.visible = True
        line.saved_view.visible = False
        line.update()
        i_cnt, i_name, i_pres, i_val = self.get_fields_values(line)
        self.anotation_name = line.item_name_field.value
        self.anotation_count = line.item_count_field.value
        self.anotation_value = line.item_value_field.value
        self.anotation_presentation = line.item_presentation_field.value
        line.item_name_field = TextField(label="Nome do Produto", value=i_name)
        line.item_count_field = TextField(label="Quantidade", value=i_cnt,
                                          width=150)
        line.item_value_field = TextField(label="valor", value=i_val,
                                          width=150)
        line.view.controls = [
            line.item_name_field, line.item_count_field,
            line.item_presentation_field, line.item_value_field]
        line.edit_view.controls[0].controls[0].visible = True
        line.edit_view.update()
        line.view.update()

    def field_change(self, anotation: Anotation, event):
        print(anotation.controls)
        print(event.control)

    def anotation_save(self, line: Anotation):
        if ("" != line.item_value_field.value
                and line.item_name_field.value != ""
                and line.item_count_field.value != ""
                and line.item_presentation_field.value is not None):
            i_cnt, i_name, i_pres, i_val = self.get_fields_values(line)
            if (self.anotation_value != i_val
                    or self.anotation_count != i_cnt):
                i_cnt, i_val = self.price_validator(line, i_cnt, i_val)
            line.timestamp.value = self.get_timestamp()
            line.item_name.value = i_name
            line.item_count.value = i_cnt
            line.item_value.value = f'{float(i_val):.2f}'
            line.item_presentation.value = i_pres
            line.view.controls = [
                line.item_name, line.item_count, line.item_presentation,
                line.item_value]
            line.edit_view.controls[0].controls[0].visible = False
            self.anotation_name = line.item_name_field.value
            self.anotation_count = line.item_count_field.value
            self.anotation_value = line.item_value_field.value
            line.edit_view.update()
            line.view.visible = False
            line.saved_view.visible = True
            line.update()
        else:
            self.show_alert_dialog("Preencher todos os campos!")

    def get_fields_values(self, annotation):
        item_name = annotation.item_name_field.value
        item_count = annotation.item_count_field.value
        item_value = annotation.item_value_field.value
        item_presentation = annotation.item_presentation_field.value
        return item_count, item_name, item_presentation, item_value

    def show_alert_dialog(self, msg):
        dlg = ft.AlertDialog(title=ft.Text(msg))
        self.page.dialog = dlg
        self.page.dialog.open = True

    def price_validator(self, annotation, item_count, item_value):
        try:
            item_value = float(item_value.replace(',', '.'))
        except ValueError:
            print("deu errado nos numeros")
            item_value = annotation.item_value_field.value
            item_count = annotation.item_count_field.value
        return item_count, item_value

    def tabs_changed(self, e):
        ...

    def get_timestamp(self):
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
        return timestamp

    def get_tab_day(self):
        now = datetime.now()
        return now.weekday()
