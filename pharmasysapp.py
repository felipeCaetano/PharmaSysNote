from datetime import datetime

import flet as ft
from flet_core import (
    Page, icons, Tabs, Tab, Column, IconButton, Row, ControlEvent,
    DataTable, DataColumn, Text, DataRow,
    DataCell, SnackBar, transform)

from annotation import Anotation
from cadastro import Cadastro
from search_field import SearchField
from tablesdb import create_table, conn

days_of_week = [
    'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'
]


def is_not_empty_fields(line):
    return (line.item_value_field.value != ''
            and line.item_name_field.value != ''
            and line.item_count_field.value != ''
            and line.item_presentation_field.value is not None)


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
    )


def get_tab_day():
    now = datetime.now()
    return now.weekday()


def create_day_filter_tabs(create_line, day_filter, search_engine):
    day_of_week = get_tab_day()
    for i in range(7):
        my_table = DataTable(
            columns=[
                DataColumn(Text('Data/Hora')),
                DataColumn(Text('Produto')),
                DataColumn(Text('Quantidade')),
                DataColumn(Text('Apresentação')),
                DataColumn(Text('Valor')),
                DataColumn(Text('Ações')),
            ],
            rows=[],
        )

        tab = Tab(
            text=days_of_week[i],
            content=Column(
                [SearchField(create_line, search_engine),
                 my_table],
                scroll=True
            )
        )
        if day_of_week != i:
            tab.content.disabled = True
        day_filter.tabs.append(tab)


def pharma_sys_note_app(page: Page):
    id_edit = Text()

    def search_engine(event: ControlEvent):
        index = day_filter.selected_index
        tab_of_day = day_filter.tabs[index]
        search_field = tab_of_day.content.controls[0]

        print(event.control, "pesquisando no banco")
        print(search_field.search_field.value, "pesquisando no banco")
        cursor = conn.cursor()
        query = "SELECT * FROM produtos WHERE codigo = ? or name = ?"
        cursor.execute(query, (search_field.search_field.value, search_field.search_field.value))
        items = cursor.fetchall()
        print(items)
        if not items:
            page.snack_bar = SnackBar(Text("Produto não cadastrado"), bgcolor='red')
            page.snack_bar.open = True
            show_confirm_dialog(_cadastrar, close_dlg, event, "Deseja Cadastrar este produto?", 'green')
        else:
            create_line(items[0])

    def savecon(event):
        status, i_name, i_code, i_info, i_price, i_cont, i_lab, i_validade, i_type, i_lote, i_pres = get_con_fields()
        print(i_name, i_code, i_info, i_price, i_cont, i_lab, i_validade, i_type, i_lote, i_pres)
        c = conn.cursor()
        c.execute(
            "INSERT INTO produtos (codigo, name, description, value, count, laboratorio, generico, lote, validade, presetation) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (i_code, i_name, i_info, i_price, i_cont, i_lab, i_validade, i_type, i_lote, i_pres)
        )
        conn.commit()
        if status:
            hidecon(event)
            page.snack_bar = SnackBar(Text("Sucess Input"), bgcolor='green')
            page.snack_bar.open = True
        else:
            page.snack_bar = SnackBar(Text("Não Cadastrado"), bgcolor='orange')
            page.snack_bar.open = True
        page.update()

    def get_con_fields():
        i_name = cadastro.product_name.value
        i_code = cadastro.product_code.value
        i_info = cadastro.product_info.value
        i_price = cadastro.product_price.value
        i_cont = cadastro.product_total_cnt.value
        i_lab = cadastro.product_lab.value
        i_valid = cadastro.product_date.value
        i_type = cadastro.product_generic.value
        i_lote = cadastro.product_lote.value
        i_pres = cadastro.product_presentation.value
        if all([i_name, i_code, i_info, i_price, i_cont, i_lab, i_valid, i_type, i_lote, i_pres]):
            return True, i_name, i_code, i_info, i_price, i_cont, i_lab, i_valid, i_type, i_lote, i_pres
        else:
            show_alert_dialog("Preencha todos os campos!")
            return False, i_name, i_code, i_info, i_price, i_cont, i_lab, i_valid, i_type, i_lote, i_pres

    def hidecon(event):
        cadastro.offset = transform.Offset(2, 0)
        page.remove(cadastro)
        page.update()

    cadastro = Cadastro(savecon, hidecon)

    def _cadastrar(event):
        close_dlg(event)
        cadastro.offset = transform.Offset(0, 0)
        page.add(cadastro)
        page.update()

    def anotation_edit(event: ControlEvent):
        index = day_filter.selected_index
        tab_of_day = day_filter.tabs[index]
        anotacao = Anotation(anotation_update, anotation_edit, delete_line)
        anotacao.item_name_field.value = event.control.data[1]
        anotacao.item_count_field.value = event.control.data[3]
        anotacao.item_presentation_field.value = event.control.data[2]
        anotacao.item_value_field.value = event.control.data[5][3:]
        id_edit.value = event.control.data[0]
        tab_of_day.content.controls.append(anotacao)
        page.update()

    def anotation_update(line: Anotation):
        if is_not_empty_fields(line):
            i_cnt, i_name, i_pres, i_val = get_fields_values(line)
            valid, i_val, i_cnt = check_numeric_values(i_cnt, i_val)
            if not valid:
                return
            else:
                update_permanent_line(i_cnt, i_name, i_pres, i_val, line)
        else:
            show_alert_dialog("Preencher todos os campos!")

    def anotation_save(line: Anotation):
        if is_not_empty_fields(line):
            i_cnt, i_name, i_pres, i_val = get_fields_values(line)
            valid, i_val, i_cnt = check_numeric_values(i_cnt, i_val)
            if not valid:
                return
            else:
                create_permanent_line(i_cnt, i_name, i_pres, i_val, line)
        else:
            show_alert_dialog("Preencher todos os campos!")

    def update_permanent_line(i_cnt, i_name, i_pres, i_val, line):
        try:
            myid = id_edit.value
            set_fields_values(i_cnt, i_name, i_pres, i_val, line)
            my_table = day_filter.tabs[day_filter.selected_index].content.controls[1]
            c = conn.cursor()
            c.execute(
                "UPDATE items SET timestamp=?, name=?, count=?, presetation=?, value=? WHERE id=?",
                (line.timestamp.value, line.item_name.value,
                 line.item_count.value,
                 line.item_presentation.value, line.item_value.value, myid)
            )
            conn.commit()
            my_table.rows.clear()
            read_db()
            change_line_visibles(line)
            page.update()
        except Exception as e:
            print(e)

    def create_permanent_line(i_cnt, i_name, i_pres, i_val, line):
        set_fields_values(i_cnt, i_name, i_pres, i_val, line)
        my_table = day_filter.tabs[day_filter.selected_index].content.controls[
            1]
        if insert_line(line):
            page.snack_bar = SnackBar(Text("Sucess Input"), bgcolor='green')
            page.snack_bar.open = True
            my_table.rows.clear()
            read_db()
            change_line_visibles(line)
            page.update()
        else:
            page.snack_bar = SnackBar(Text("Falha ao salvar "), bgcolor='red')
            page.snack_bar.open = True
            page.update()


    def insert_line(line):
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO items (timestamp, name, count, presetation, value) VALUES(?,?,?,?,?)",
                (line.timestamp.value, line.item_name.value, line.item_count.value,
                 line.item_presentation.value, line.item_value.value)
            )
            conn.commit()
            return True
        except Exception:
            return False

    def read_db():
        my_table = get_data_table()
        cursor = conn.cursor()
        data_atual = datetime.today()
        data_atual_formatada = data_atual.strftime("%d/%m/%Y")
        query = "SELECT * FROM items WHERE SUBSTR(timestamp, 1, 10) = ?"
        cursor.execute(query, (data_atual_formatada,))
        items = cursor.fetchall()
        for item in items:
            my_table.rows.append(
                DataRow(
                    cells=[DataCell(Text(item[4])),
                           DataCell(Text(item[1])),
                           DataCell(Text(item[3])),
                           DataCell(Text(item[2])),
                           DataCell(Text(item[5])),
                           DataCell(
                               Row([
                                   IconButton(
                                       "edit",
                                       data=item,
                                       on_click=anotation_edit),
                                   IconButton("delete",
                                              data=item[0],
                                              on_click=delete_line)
                               ]
                               ))],
                )
            )

    def get_data_table():
        my_table = day_filter.tabs[day_filter.selected_index].content.controls[
            1]
        return my_table

    def close_dlg(event):
        page.dialog.open = False
        page.update()

    def delete_line(event):

        def _delete(event):
            try:
                myid = int(event.control.data)
                c = conn.cursor()
                c.execute("DELETE FROM items WHERE id=?", (myid,))
                conn.commit()
                close_dlg(event)
                my_table.rows.clear()
                read_db()
                my_table.update()
            except Exception as e:
                print(e.args)

        if isinstance(event, Anotation):
            index = day_filter.selected_index
            tab_of_day = day_filter.tabs[index]
            search_field = tab_of_day.content.controls[0]
            tab_of_day.content.controls.pop()
            search_field.search_field.value = ""
            search_field.update()
            page.update()
            return
        my_table = get_data_table()
        show_confirm_dialog(_delete, close_dlg, event, "Deseja realmente DELETAR este item?", 'red')

    def show_confirm_dialog(confirm, refuse, event, sys_msg, confirm_color):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                content=ft.Text("Por favor,  CONFIRME:", size=15),
                bgcolor=ft.colors.BLUE_GREY_200,
                padding=10,
                expand=True,
                border_radius=0,
                border=ft.border.all(1, ft.colors.BLUE_GREY_200)),
            content=ft.Text(sys_msg, weight='bold'),
            actions=[
                ft.ElevatedButton(
                    "Sim",
                    style=ft.ButtonStyle(color=confirm_color),
                    data=event.control.data,
                    on_click=confirm),
                ft.ElevatedButton(
                    "Não",
                    on_click=refuse),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            title_padding=1,
        )
        page.dialog = dlg_modal
        page.dialog.open = True
        page.update()

    def change_line_visibles(line):
        # print(day_filter.tabs[day_filter.selected_index].content.controls)
        del day_filter.tabs[day_filter.selected_index].content.controls[2]
        line.view.visible = False
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

    def create_line(e: ControlEvent):
        print(f'create line for {e}')
        anotacao = Anotation(anotation_save, anotation_edit, delete_line)
        index = day_filter.selected_index
        tab_of_day = day_filter.tabs[index]
        search_field = tab_of_day.content.controls[0]
        if isinstance(e, ControlEvent):
            anotacao.item_name_field.value = search_field.search_field.value
        else:
            anotacao.item_name_field.value = e[2]
            anotacao.item_presentation_field.value = e[3]
            anotacao.item_value_field.value = e[-2]

        tab_of_day.content.controls.append(anotacao)
        search_field.search_field.value = ""
        search_field.update()
        page.update()

    def get_timestamp():
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
        return timestamp

    def create_menu_item(icon=None, text=""):
        if not icon and not text:
            return ft.PopupMenuItem()
        return ft.PopupMenuItem(icon=icon, text=text)

    def create_popupmenubuttons():
        return [
            ft.PopupMenuButton(
                items=[
                    create_menu_item(icons.LOGIN, "Login"),
                    create_menu_item(),
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

    create_table()
    day_filter = Tabs(
        selected_index=0, animation_duration=300, expand=True)
    create_day_filter_tabs(create_line, day_filter, search_engine)
    day_filter.selected_index = get_tab_day()

    page.appbar.actions = create_popupmenubuttons()

    rail = create_nav_rail()
    page.scroll = "allways"
    read_db()
    # cadastro = Cadastro()
    page.add(Column([
        Row(
            [rail, ft.VerticalDivider(width=1), day_filter],
            expand=True),
        # cadastro
    ], expand=True)
    )
