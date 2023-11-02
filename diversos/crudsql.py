from flet import *
import sqlite3


def main(page: Page):
    page.scroll = "allways"

    name = TextField(label="You name")
    you_id = Text("")
    my_table = DataTable(
        columns=[
            DataColumn(Text('id')),
            DataColumn(Text('name')),
            DataColumn(Text('address'))
        ],
        rows=[]
    )
    def edit_index(event, r):
        print("your id is = ", event)
        print("your selected name is = ", r )

        name.value = r
        you_id = int(event)
        add_button.visible = False
        delete_button.visible = True
        edit_button.visible = True
        page.update()

    def add_new_Data(event):
        my_table.rows.append(
            DataRow(
                cells=[DataCell(Text(len(my_table.rows))),
                       DataCell(Text(name.value)),
                       DataCell(Text("Fake adress"))],
                on_select_changed=lambda e: edit_index(
                    e.control.cells[0].content.value,
                    e.control.cells[1].content.value,)
            )

        )
        name.value = ""
        page.update()

    add_button = ElevatedButton(
        "add", bgcolor="blue", color='white', on_click=add_new_Data
    )

    def delete_index(event):
        print("you id is= ", you_id.value)
        del my_table.rows[you_id.value]
        page.snack_bar = SnackBar(
            Text(f'succes delete {you_id.value=}', color='white'),
            bgcolor='red',
        )
        page.snack_bar.open = True
        page.update()

    delete_button = ElevatedButton(
        "delete", bgcolor="red", color='white', on_click=delete_index
    )

    def editandsave(event):
        my_table.rows[you_id.value].cells[1].content = Text(name.value)
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
