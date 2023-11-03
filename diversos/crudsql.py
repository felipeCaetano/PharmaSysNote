from flet import *
import sqlite3


def main(page: Page):
    page.scroll = "allways"

    name = TextField(label="You name")
    your_id = Text("")
    my_table = DataTable(
        columns=[
            DataColumn(Text('id')),
            DataColumn(Text('name')),
            DataColumn(Text('address'))
        ],
        rows=[]
    )

    def edit_index(e_id, r):
        print("your id is = ", e_id)
        print("your selected name is = ", r)

        name.value = r
        your_id.value = int(e_id)
        change_visible_buttons()
        page.update()

    def add_new_data(event):
        my_table.rows.append(
            DataRow(
                cells=[DataCell(Text(len(my_table.rows))),
                       DataCell(Text(name.value)),
                       DataCell(Text("Fake adress"))],
                on_select_changed=lambda e: edit_index(
                    e.control.cells[0].content.value,
                    e.control.cells[1].content.value, )
            )
        )
        name.value = ""
        page.update()

    add_button = ElevatedButton(
        "add", bgcolor="blue", color='white', on_click=add_new_data
    )

    def delete_index(event):
        print("you id is= ", your_id.value)
        del my_table.rows[int(your_id.value)]
        page.snack_bar = SnackBar(
            Text(f'succes delete {your_id.value=}', color='white'),
            bgcolor='red',
        )
        page.snack_bar.open = True
        change_visible_buttons()
        page.update()

    def change_visible_buttons():
        add_button.visible = not add_button.visible
        delete_button.visible = not delete_button.visible
        edit_button.visible = not edit_button.visible

    delete_button = ElevatedButton(
        "delete", bgcolor="red", color='white', on_click=delete_index
    )

    def editandsave(event):
        my_table.rows[your_id.value].cells[1].content = Text(name.value)
        change_visible_buttons()
        page.update()

    edit_button = ElevatedButton(
        "edit", bgcolor="orange", color='white', on_click=editandsave
    )

    delete_button.visible = False
    edit_button.visible = False

    page.add(
        Column([
            Text("My CRUD sample", size=30, weight='bold'),
            name,
            Row([
                add_button,
                delete_button,
                edit_button
            ]),
            my_table
        ])
    )


app(target=main)
