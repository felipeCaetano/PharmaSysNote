from datetime import datetime

import flet as ft
from flet_core import (
    Page, icons, Tabs, Tab, Column, IconButton, Row, TextField, ControlEvent, DataTable, DataColumn, Text, DataRow,
    DataCell, Container)

from annotation import Anotation
from search_field import SearchField

days_of_week = [
    'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'
]



def is_not_empty_fields(line):
    return (line.item_value_field.value != ''
            and line.item_name_field.value != ''
            and line.item_count_field.value != ''
            and line.item_presentation_field.value is not None)


def pharma_sys_note_app(page: Page):
    def anotation_delete(anotation):
        def close_dlg():
            dlg_modal.open = False
            page.update()

        def delete_anotation(e):
            dlg_modal.open = False
            index = day_filter.selected_index
            tab_of_day = day_filter.tabs[index]
            tab_of_day.content.controls[2].controls.remove(anotation)
            anotation.update()
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                content=ft.Text("Por favor,  CONFIRME:", size=15),
                bgcolor=ft.colors.BLUE_GREY_200,
                padding=10,
                expand=True,
                border_radius=0,
                border=ft.border.all(1, ft.colors.BLUE_GREY_200)),
            content=ft.Text("Você realmente deseja deletar esse item?",
                            weight='bold'),
            actions=[
                ft.ElevatedButton("Sim", style=ft.ButtonStyle(color='red'),
                              on_click=delete_anotation),
                ft.ElevatedButton("Não", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            title_padding=1,
        )
        page.dialog = dlg_modal
        page.dialog.open = True
        page.update()

    def anotation_edit(line: Anotation):
        line.view.visible = True
        line.saved_view.visible = False
        line.update()
        i_cnt, i_name, i_pres, i_val = get_fields_values(line)
        line.item_name_field = TextField(label="Nome do Produto", value=i_name)
        line.item_count_field = TextField(label="Quantidade", value=i_cnt,
                                          width=150)
        line.item_value_field = TextField(label="valor", value=i_val,
                                          width=150)
        line.view.controls = [
            line.item_name_field, line.item_count_field,
            line.item_presentation_field, line.item_value_field]
        line.control_buttons.controls[0].controls[0].visible = True
        line.control_buttons.update()
        line.view.update()

    def anotation_save(line: Anotation):
        if is_not_empty_fields(line):
            i_cnt, i_name, i_pres, i_val = get_fields_values(line)
            valid, i_val, i_cnt = check_numeric_values(i_cnt, i_val)
            if not valid:
                return
            else:
                create_permant_line(i_cnt, i_name, i_pres, i_val, line)
                line.update()
        else:
            show_alert_dialog("Preencher todos os campos!")

    def create_permant_line(i_cnt, i_name, i_pres, i_val, line):
        set_fields_values(i_cnt, i_name, i_pres, i_val, line)
        line.view.controls = [
            line.item_name, line.item_count, line.item_presentation,
            line.item_value]
        change_line_visibles(line)

    def change_line_visibles(line):
        line.control_buttons.controls[0].controls[0].visible = False
        line.view.visible = False
        line.saved_view.visible = True
        line.control_buttons.update()

    def set_fields_values(i_cnt, i_name, i_pres, i_val, line):
        line.timestamp.value = get_timestamp()
        line.item_name.value = i_name
        line.item_count.value = i_cnt
        line.item_value.value = f'R$ {float(i_val):.2f}'
        line.item_presentation.value = i_pres

    def check_numeric_values(i_cnt, i_val):
        result, i_val, i_cnt = numeric_validator(i_cnt, i_val)
        return result, i_val, i_cnt

    def get_fields_values(line):
        item_name = line.item_name_field.value
        item_count = line.item_count_field.value
        item_value = line.item_value_field.value
        item_presentation = line.item_presentation_field.value
        return item_count, item_name, item_presentation, item_value

    def show_alert_dialog(msg):
        dlg = ft.AlertDialog(title=ft.Text(msg))
        page.dialog = dlg
        page.dialog.open = True
        page.update()

    def numeric_validator(item_count, item_value):
        try:
            item_value = float(item_value.replace(',', '.'))
            item_count = int(item_count)
            return True, item_value, item_count
        except ValueError:
            show_alert_dialog("Insira Valores numéricos!")
            return False, item_value, item_count

    # def tabs_changed(e):
    #     ...

    def create_line(e: ControlEvent):
        print("fui chamado por", e.control)

        index = day_filter.selected_index
        anotacao = Anotation(anotation_save, anotation_edit, anotation_delete)
        tab_of_day = day_filter.tabs[index]
        search_field = tab_of_day.content.controls[0]

        tab_of_day.content.controls[1].visible = True
        anotacao.item_name_field.value = search_field.search_field.value
        #tab_of_day.content.controls[1].update()
        tab_of_day.content.controls[2].controls.append(anotacao)
        #tab_of_day.content.controls[2].update()
        #tab_of_day.update()
        page.update()


    def get_timestamp():
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
        return timestamp

    def get_tab_day():
        now = datetime.now()
        return now.weekday()

    def create_menu_item(icon=None, text=""):
        if not icon and not text:
            return ft.PopupMenuItem()
        return ft.PopupMenuItem(icon=icon, text=text)

    def create_popupmenubuttons():
        return [
            ft.PopupMenuButton(
                items=[
                    create_menu_item(icons.LOGIN, "Login"),
                    create_menu_item(),  # divider
                    create_menu_item(icons.PIE_CHART, "Relatórios"),
                    create_menu_item(),
                    create_menu_item(icons.SETTINGS, "Configurações"),
                    create_menu_item(),
                    create_menu_item(icons.HELP, "Ajuda"),
                    create_menu_item(),
                    create_menu_item(icons.INFO, "Sobre"),
                    create_menu_item(),
                    create_menu_item(icons.LOGOUT, "Logout"),
                ]
            )
        ]

    day_filter = Tabs(selected_index=0, animation_duration=300, expand=True)
    create_day_filter_tabs(create_line, day_filter)
    day_filter.selected_index = get_tab_day()

    page.appbar.actions = create_popupmenubuttons()

    rail = create_nav_rail()

    page.add(Row([rail, ft.VerticalDivider(width=1), day_filter], expand=True))


def create_nav_rail():
    return ft.NavigationRail(
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


def create_day_filter_tabs(create_line, day_filter):
    print("create_day_filter_tabs")
    for i in range(7):
        anotations = Column()
        tab = Tab(
            text=days_of_week[i],
            content=Column([SearchField(create_line, search_engine),
                            Container(content=head_table, visible=False, bgcolor='blue'),
                            ft.ListView(
                                expand=1,
                                spacing=10,
                                padding=20,
                                auto_scroll=False,
                                controls=[anotations])
                            ])
        )
        day_filter.tabs.append(tab)


def search_engine(event: ControlEvent):
    print(event.control, "pesquisando no banco")
