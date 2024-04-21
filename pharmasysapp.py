from datetime import datetime
from sqlite3 import Error

import flet as ft
from flet_core import (colors, Column, ControlEvent, DataCell, DataColumn,
                       DataRow, DataTable, FontWeight, IconButton, icons,
                       Page, Row, ScrollMode, SnackBar, Tab, Tabs, Text,
                       transform)

from annotation import Annotation
from appstrings import (ABOUT, ALTER_PROD, ALTER_PRODUCT, APP_NAME, CHARTS,
                        CLOSE_DAY,
                        COLUMN_0, COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4,
                        COLUMN_5, CONFIGS, DELETE_ITEM, FAIL, FILL_FIELDS,
                        FRIDAY, FT_ANOTA, HELP, INSERT_NUMBERS, LOGIN, LOGOUT,
                        MONDAY, NEW_REGISTER, NO, NOT_REGISTERED, PLS_CONFIRME,
                        PROD_NOTFOUND, REALLY_CLOSE, SATURDAY, SUCCESS, SUNDAY,
                        THURSDAY,
                        TUESDAY, WANT_TO_REGISTER, WEDNESDAY, YES,
                        PAGE_APP_BAR_TITLE)
from cadastro import Alterador, Cadastro, Form
from search_field import SearchField, SearchBar
from tablesdb import conn, create_table

ERROR_ON_LOAD = "Erro ao carregar dados!"

DELETE_ERROR = "Erro ao deletar!"

days_of_week = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]
column_names = [COLUMN_0, COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5]

data_table_style = {
    "expand": True,
    # "height": 350,
    "border_radius": 8,
    "border": ft.border.all(2, "#ebebeb"),
    "horizontal_lines": ft.border.BorderSide(1, '#ebebeb'),
    "columns": [
        ft.DataColumn(
            ft.Text(index, size=12, color='black', weight='bold')
        )
        for index in column_names
    ]
}

dummy_data = {
    0: {"Data/Hora": "18/02/1983", "Produto": "Apple", "Quantidade": 5,
        "Apresentação": "Red and Juicy", "Valor": 1.99, "Açoes": ""},
    1: {"Data/Hora": "18/02/1983", "Produto": "ABACAXI", "Quantidade": 10,
        "Apresentação": "Red and Juicy", "Valor": 1.99, "Açoes": ""},
    # 2: {"name": "Milk", "description": "Organic Whole Milk", "quantity": 1,
    #     "price": 2.99},
    # 3: {"name": "Carrot", "description": "Fresh and Crunchy", "quantity": 10,
    #     "price": 0.99},
    # 4: {"name": "Eggs", "description": "Free range Brown eggs", "quantity": 5,
    #     "price": 1.99},
    # 5: {"name": "Chicken", "description": "Whole wheat loaf", "quantity": 2,
    #     "price":
    #         3.49},
    # 6: {"name": "Banana", "description": "Organic Whole Milk", "quantity": 1,
    #     "price": 2.99},
}


class Controller:
    items = dummy_data
    counter = len(items)

    @staticmethod
    def get_items():
        return Controller.items

    @staticmethod
    def add_items(item):
        Controller.items[Controller.counter] = item
        Controller.counter += 1


def is_not_empty_fields(line):
    return (
            line.item_value_field.value != ""
            and line.item_name_field.value != ""
            and line.item_count_field.value != ""
            and line.item_presentation_field.value is not None
    )


def create_nav_rail():
    return ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(
            icon=ft.icons.LOCAL_PHARMACY, text=APP_NAME),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.CREATE,
                selected_icon=ft.icons.CREATE_OUTLINED,
                icon_content=IconButton(),
                label=FT_ANOTA,
            ),
        ],
    )


def get_weekday():
    now = datetime.now()
    return now.weekday()


class DataTable(ft.DataTable):
    def __init__(self):
        super().__init__(**data_table_style)
        self.df = Controller.get_items()

    def fill_datatable(self):
        self.rows = []
        for values in self.df.values():
            data = ft.DataRow()
            data.cells = [
                ft.DataCell(
                    ft.Text(value, color='black')
                ) for value in values.values()
            ]
            self.rows.append(data)
        # self.update()


def create_day_filter_tabs(create_line, day_filter, search_engine, close_day):
    day_of_week = get_weekday()
    for day_index in range(7):
        my_table = DataTable()

        tab = Tab(
            text=days_of_week[day_index],
            content=Column(
                expand=True,
                controls=[
                    SearchBar(create_line),
                    Column(
                        scroll=ScrollMode.HIDDEN,

                        controls=[Row(controls=[my_table])],
                    ),
                    ft.Divider(),
                    Row(
                        controls=[
                            ft.ElevatedButton(
                                CLOSE_DAY,
                                bgcolor='red',
                                color='white',
                                on_click=close_day)
                        ],
                        # alignment=ft.MainAxisAlignment.END
                    )
                ],
                # scroll=ScrollMode.ALWAYS
            )
        )
        # mytable = get_data_table()
        # my_table.fill_datatable()

        tab.content.disabled = True if day_of_week != day_index else False
        day_filter.tabs.append(tab)


def pharma_sys_note_app(page: Page):
    id_edit = Text()

    def search_product(event):
        product_code = up_cadastro.prod_code.value
        items = select_products(product_code)
        if not items:
            open_snackbar(PROD_NOTFOUND, colors.RED)
            show_confirm_dialog(
                _show_cadastrar,
                close_dlg, event,
                WANT_TO_REGISTER,
                colors.GREEN)
            page.update()
        else:
            set_con_fields(items[0])
            up_cadastro.data = items[0]

    def search_engine(event: ControlEvent):
        search_field, _ = get_search_field()
        items = select_products(search_field.search_field.value)
        if not items:
            open_snackbar(PROD_NOTFOUND, colors.RED)
            show_confirm_dialog(
                _show_cadastrar,
                close_dlg, event,
                WANT_TO_REGISTER,
                colors.GREEN)
            page.update()
        else:
            create_line(items[0])

    def open_snackbar(snack_msg, snack_color):
        page.snack_bar = SnackBar(Text(snack_msg), bgcolor=snack_color)
        page.snack_bar.open = True
        page.update()

    def select_products(product_code):
        cursor = conn.cursor()
        query = "SELECT * FROM produtos WHERE codigo = ? or name = ?"
        cursor.execute(
            query,
            (product_code, product_code)
        )
        items = cursor.fetchall()
        return items

    def editcon(event):
        my_id = up_cadastro.data[0]
        (status, i_name, i_code, i_info, i_price, i_cont, i_lab, i_validade,
         i_type, i_lote, i_pres) = get_con_fields(up_cadastro)
        # set_con_fields(item)
        status = update_products(
            i_code, i_cont, i_info, i_lab, i_lote, i_name, i_pres,
            i_price, i_type, i_validade, my_id)
        if status:
            hidecon(up_cadastro)
            open_snackbar(SUCCESS, colors.GREEN)
            read_sales_day()
        else:
            open_snackbar(FAIL, colors.RED)

    def update_products(i_code, i_cont, i_info, i_lab, i_lote, i_name, i_pres,
                        i_price, i_type, i_validade, my_id):
        c = conn.cursor()
        try:
            c.execute(
                "UPDATE produtos SET codigo=?, name=?, description=?, value=?, "
                "count=?, laboratorio=?, generico=?, lote=?, validade=?, "
                "presetation=? WHERE id=?",
                (i_code, i_name, i_info, i_price, i_cont, i_lab, i_validade,
                 i_type, i_lote, i_pres, my_id))
            conn.commit()
            return True
        except Error:
            return False

    def set_con_fields(item):
        up_cadastro.product_name.value = item[2]
        up_cadastro.product_info.value = item[3]
        up_cadastro.product_presentation.value = item[4]
        up_cadastro.product_total_cnt.value = item[5]
        up_cadastro.product_lab.value = item[6]
        up_cadastro.product_date.value = item[7]
        up_cadastro.product_generic.value = item[8]
        up_cadastro.product_lote.value = item[9]
        up_cadastro.product_price.value = item[10]
        up_cadastro.update()
        page.update()

    def savecon(event):
        (status, i_name, i_code, i_info, i_price, i_cont, i_lab, i_validade,
         i_type, i_lote, i_pres) = get_con_fields(cadastro)  # NOQA
        c = conn.cursor()
        c.execute(
            "INSERT INTO produtos (codigo, name, description, value, count, "
            "laboratorio, generico, lote, validade, presetation) VALUES(?,?,"
            "?,?,?,?,?,?,?,?)",
            (
                i_code, i_name, i_info, i_price, i_cont, i_lab, i_validade,
                i_type,
                i_lote, i_pres,))
        conn.commit()
        if status:
            hidecon(cadastro)
            open_snackbar(SUCCESS, colors.GREEN)
        else:
            open_snackbar(NOT_REGISTERED, colors.ORANGE)
        page.update()

    def get_con_fields(form):
        i_name = form.product_name.value
        i_code = form.prod_code.value
        i_info = form.product_info.value
        i_price = form.product_price.value
        i_cont = form.product_total_cnt.value
        i_lab = form.product_lab.value
        i_valid = form.product_date.value
        i_type = form.product_generic.value
        i_lote = form.product_lote.value
        i_pres = form.product_presentation.value
        if all([i_name, i_code, i_info, i_price, i_cont, i_lab, i_valid,
                i_type,
                i_lote, i_pres]):
            return (True, i_name, i_code, i_info, i_price, i_cont, i_lab,
                    i_valid, i_type, i_lote, i_pres)
        else:
            show_alert_dialog(FILL_FIELDS)
            return (False, i_name, i_code, i_info, i_price, i_cont, i_lab,
                    i_valid, i_type, i_lote, i_pres)

    def hidecon(hide_obj):
        hide_obj.offset = transform.Offset(0, 0)
        page.remove(hide_obj)
        page.update()

    def _show_cadastrar(event):
        close_dlg(event)
        search_field, _ = get_search_field()
        # cadastro.prod_code.value = search_field.search_field.value
        page.add(cadastro)
        cadastro.offset = transform.Offset(0, 0)
        page.update()

    def update_product(event):
        up_cadastro.offset = transform.Offset(0, 0)
        up_cadastro.prod_code.suffix.on_click = search_product
        up_cadastro.inputcon.content.content.controls[4].on_click = editcon
        page.add(up_cadastro)
        page.update()

    def annotation_edit(event: ControlEvent):
        index = day_filter.selected_index
        tab_of_day = day_filter.tabs[index]
        anotacao = Annotation(annotation_update, annotation_edit, del_line)
        anotacao.item_name_field.value = event.control.data[1]
        anotacao.item_count_field.value = event.control.data[3]
        anotacao.item_presentation_field.value = event.control.data[2]
        anotacao.item_value_field.value = event.control.data[5][3:]
        id_edit.value = event.control.data[0]
        tab_of_day.content.controls.append(anotacao)
        page.update()

    def annotation_update(line: Annotation):
        if is_not_empty_fields(line):
            i_cnt, i_name, i_pres, i_val = get_fields_values(line)
            valid, i_val, i_cnt = check_numeric_values(i_cnt, i_val)
            if not valid:
                return
            else:
                update_permanent_line(i_cnt, i_name, i_pres, i_val, line)
        else:
            show_alert_dialog(FILL_FIELDS)

    def annotation_save(line: Annotation):
        if is_not_empty_fields(line):
            i_cnt, i_name, i_pres, i_val = get_fields_values(line)
            valid, i_val, i_cnt = check_numeric_values(i_cnt, i_val)
            if not valid:
                return
            else:
                create_permanent_line(i_cnt, i_name, i_pres, i_val, line)
        else:
            show_alert_dialog(FILL_FIELDS)

    def update_permanent_line(i_cnt, i_name, i_pres, i_val, line):
        try:
            myid = id_edit.value
            set_fields_values(i_cnt, i_name, i_pres, i_val, line)
            selected_tab = day_filter.tabs[day_filter.selected_index]
            my_table = selected_tab.content.controls[1]
            c = conn.cursor()
            c.execute(
                "UPDATE items SET timestamp=?, name=?, count=?, "
                "presetation=?, value=? WHERE id=?",
                (
                    line.timestamp.value,
                    line.item_name.value,
                    line.item_count.value,
                    line.item_presentation.value,
                    line.item_value.value,
                    myid,
                ),
            )
            conn.commit()
            my_table.rows.clear()
            read_sales_day()
            change_line_visible(line)
            page.update()
        except Error as e:
            open_snackbar(FAIL, colors.RED_700)

    def create_permanent_line(i_cnt, i_name, i_pres, i_val, line):
        set_fields_values(i_cnt, i_name, i_pres, i_val, line)
        my_table = day_filter.tabs[day_filter.selected_index].content.controls[
            1]
        if insert_line(line):
            page.snack_bar = SnackBar(Text(SUCCESS), bgcolor="green")
            page.snack_bar.open = True
            my_table.rows.clear()
            read_sales_day()
            change_line_visible(line)
            page.update()
        else:
            page.snack_bar = SnackBar(Text(FAIL), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    def insert_line(line):
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO items (timestamp, name, count, presetation, "
                "value) VALUES(?,?,?,?,?)",
                (
                    line.timestamp.value,
                    line.item_name.value,
                    line.item_count.value,
                    line.item_presentation.value,
                    line.item_value.value,
                ),
            )
            conn.commit()
            return True
        except Error:
            return False

    def read_sales_day():
        my_table = get_data_table()
        _, cursor = get_sales_day()
        items = cursor.fetchall()
        if items:
            Controller.items = items
            my_table.fill_datatable()
            # my_table.rows.clear()
            # for item in items:
            #     my_table.rows.append(
            #         DataRow(
            #             cells=[
            #                 DataCell(Text(item[4])),
            #                 DataCell(Text(item[1])),
            #                 DataCell(Text(item[3])),
            #                 DataCell(Text(item[2])),
            #                 DataCell(Text(item[5])),
            #                 DataCell(
            #                     Row([
            #                         IconButton(
            #                             icons.EDIT,
            #                             data=item,
            #                             on_click=annotation_edit
            #                         ),
            #                         IconButton(
            #                             icons.DELETE,
            #                             data=item[0],
            #                             on_click=del_line
            #                         )
            #                     ])
            #                 )
            #             ]
            #         )
            #     )
        else:
            open_snackbar(ERROR_ON_LOAD, colors.RED)

    def get_sales_day():
        op_status = None
        cursor = conn.cursor()
        formated_date = get_formated_date()
        try:
            op_status = get_sales_on_date(cursor, formated_date, op_status)
        except Error:
            op_status = False
        return op_status, cursor

    def get_sales_on_date(cursor, formated_date, op_status):
        query = "SELECT * FROM items WHERE SUBSTR(timestamp, 1, 10) = ?"
        cursor.execute(query, (formated_date,))
        op_status = True
        return op_status

    def get_formated_date():
        date = datetime.today()
        fmt_date = date.strftime("%d/%m/%Y")
        return fmt_date

    def get_data_table():
        selected_tab = day_filter.tabs[day_filter.selected_index]
        my_table = selected_tab.content.controls[1]
        return my_table

    def close_dlg(event):
        page.dialog.open = False
        page.update()

    def del_line(event):
        def _delete(event):
            try:
                myid = int(event.control.data)
                c = conn.cursor()
                c.execute("DELETE FROM items WHERE id=?", (myid,))
                conn.commit()
                close_dlg(event)
                my_table.rows.clear()
                read_sales_day()
                my_table.update()
            except Error as e:
                open_snackbar(DELETE_ERROR, colors.ORANGE)

        if isinstance(event, Annotation):
            index = day_filter.selected_index
            tab_of_day = day_filter.tabs[index]
            search_field = tab_of_day.content.controls[0]
            tab_of_day.content.controls.pop()
            search_field.search_field.value = ""
            search_field.update()
            page.update()
            return
        my_table = get_data_table()
        show_confirm_dialog(_delete, close_dlg, event, DELETE_ITEM, "red")

    def show_confirm_dialog(confirm, refuse, event, sys_msg, confirm_color):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                content=ft.Text(PLS_CONFIRME, size=15),
                bgcolor=ft.colors.BLUE_GREY_200,
                padding=10,
                expand=True,
                border_radius=0,
                border=ft.border.all(1, ft.colors.BLUE_GREY_200),
            ),
            content=ft.Text(sys_msg, weight=FontWeight.BOLD),
            actions=[
                ft.ElevatedButton(
                    YES,
                    style=ft.ButtonStyle(color=confirm_color),
                    data=event.control.data,
                    on_click=confirm,
                ),
                ft.ElevatedButton(NO, on_click=refuse),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            title_padding=1,
        )
        page.dialog = dlg_modal
        page.dialog.open = True
        page.update()

    def change_line_visible(line):
        del day_filter.tabs[day_filter.selected_index].content.controls[4]
        line.view.visible = False
        line.control_buttons.update()

    def set_fields_values(i_cnt, i_name, i_pres, i_val, line):
        line.timestamp.value = get_timestamp()
        line.item_name.value = i_name
        line.item_count.value = i_cnt
        line.item_value.value = f"R$ {float(i_val):.2f}"
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
            item_value = float(item_value.replace(",", "."))
            item_count = int(item_count)
            return True, item_value, item_count
        except ValueError:
            show_alert_dialog(INSERT_NUMBERS)
            return False, item_value, item_count
        except AttributeError:
            item_value = item_value
            return True, item_value, item_count

    def create_line(element):
        anotacao = Annotation(annotation_save, annotation_edit, del_line)
        search_field, tab_of_day = get_search_field()
        if isinstance(element, ControlEvent):
            anotacao.item_name_field.value = search_field.search_field.value
        else:
            anotacao.item_name_field.value = element[2]
            anotacao.item_presentation_field.value = str(
                element[4]).capitalize()
            anotacao.item_value_field.value = element[-1]

        tab_of_day.content.controls.append(anotacao)
        search_field.search_field.value = ""
        search_field.update()
        page.update()

    def get_search_field():
        index = day_filter.selected_index
        tab_of_day = day_filter.tabs[index]
        search_field = tab_of_day.content.controls[0]
        return search_field, tab_of_day

    def get_timestamp():
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
        return timestamp

    def create_menu_item(icon=None, text="", callback=None):
        if not icon and not text:
            return ft.PopupMenuItem()
        return ft.PopupMenuItem(icon=icon, text=text, on_click=callback)

    def create_popupmenubuttons():
        return [
            ft.PopupMenuButton(
                items=[
                    create_menu_item(icons.LOGIN, LOGIN),
                    create_menu_item(),
                    create_menu_item(icons.PIE_CHART, CHARTS),
                    create_menu_item(),
                    create_menu_item(icons.PRICE_CHANGE, ALTER_PROD,
                                     update_product),
                    create_menu_item(),
                    create_menu_item(icons.SETTINGS, CONFIGS),
                    create_menu_item(),
                    create_menu_item(icons.HELP, HELP),
                    create_menu_item(),
                    create_menu_item(icons.INFO, ABOUT),
                    create_menu_item(),
                    create_menu_item(icons.LOGOUT, LOGOUT),
                ]
            )
        ]

    def close_day(event):
        total = 0

        def closing_day(event):
            nonlocal total
            close_dlg(event)
            status, cursor = get_sales_day()
            items = cursor.fetchall()
            if status:
                for item in items:
                    print(item)
                    total += item[3] * float(item[5][3:])
                day_filter.tabs[
                    day_filter.selected_index].content.controls.append(
                    Text(f'Total: R$ {total:.2f}',
                         size=30,
                         weight=FontWeight.BOLD)
                )
                page.update()
            else:
                open_snackbar(ERROR_ON_LOAD, colors.RED)

        show_confirm_dialog(closing_day, close_dlg, event, REALLY_CLOSE,
                            colors.RED)

    create_table()
    day_filter = Tabs(selected_index=0, animation_duration=300, expand=True)
    create_day_filter_tabs(create_line, day_filter, search_engine, close_day)
    day_filter.selected_index = get_weekday()
    page.appbar.actions = create_popupmenubuttons()
    # cadastro = Cadastro(savecon, hidecon, NEW_REGISTER)
    cadastro = Form(Controller)
    up_cadastro = Alterador(editcon, hidecon, ALTER_PRODUCT)
    rail = create_nav_rail()
    # page.scroll = "allways"
    mytable = get_data_table()
    mytable.fill_datatable()
    read_sales_day()
    page.add(
        Column(
            expand=True,
            controls=[
                Row(expand=True,
                    controls=[
                        rail,
                        ft.VerticalDivider(width=1),
                        day_filter],
                    )],

        )
    )


class PharmasysApp(ft.View):
    def __init__(self, page):
        super().__init__(route='/app', padding=10)
        self.appbar = page.appbar
        self.day_filter = Tabs(selected_index=0, animation_duration=300,
                          expand=True)
        create_day_filter_tabs(self.create_annotation, self.day_filter, None,
                               None)
        self.day_filter.selected_index = get_weekday()
        self.rail = create_nav_rail()
        self.expand = True,
        self.controls = [
            Row(
                expand=True,
                controls=[self.rail, ft.VerticalDivider(width=2),
                          self.day_filter]
            )
        ]

    def create_annotation(self, event: ControlEvent):
        annotation = Annotation(None, None, None)
        self.insert_anottation(annotation)

    def insert_anottation(self, annotation):
        tab = self.get_tab()
        tab.content.controls.insert(-2, annotation) #append(annotation)
        self.update()

    def get_tab(self):
        index = self.day_filter.selected_index
        tab_of_day = self.day_filter.tabs[index]
        return tab_of_day


