from flet import *
from useraction_table import create_table
from datatable import my_table, tb, calldb, conn
import sqlite3


def main(page: Page):
    create_table()
    page.scroll = "auto"

    def add_input(event):
        inputcon.offset = transform.Offset(0, 0)
        page.update()

    def hidecon(event):
        inputcon.offset = transform.Offset(2, 0)
        page.update()

    def savedata(event):
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO USERS (name, age, contact, email, address, gender) VALUES(?,?,?,?,?,?)",
                (
                    name.value,
                    age.value,
                    contact.value,
                    email.value,
                    address.value,
                    gender.value,
                ),
            )
            conn.commit()
            inputcon.offset = transform.Offset(2, 0)
            page.snack_bar = SnackBar(Text("Sucess Input"), bgcolor="green")
            page.snack_bar.open = True
            tb.rows.clear()
            calldb()
            tb.update()
            page.update()
        except Exception as e:
            print(e)

    name = TextField(label="Nome")
    age = TextField(label="age")
    contact = TextField(label="contact")
    email = TextField(label="email")
    address = TextField(label="address")
    gender = RadioGroup(
        content=Column(
            [Radio(value="M", label="Masculino"), Radio(value="F", label="Feminino")]
        )
    )

    inputcon = Card(
        offset=transform.Offset(2, 0),
        animate_offset=animation.Animation(600, curve="easeIn"),
        elevation=30,
        content=Container(
            bgcolor="green200",
            content=Column(
                [
                    Row(
                        [
                            Text("Novo Cadastro", size=20, weight="bold"),
                            IconButton(icon="close", icon_size=30, on_click=hidecon),
                        ]
                    ),
                    name,
                    contact,
                    age,
                    gender,
                    email,
                    address,
                    FilledButton("Salvar", on_click=savedata),
                ]
            ),
        ),
    )

    page.add(
        Column(
            [
                Text("CADASTRAR USUÁRIOS", size=30, weight="bold"),
                ElevatedButton("Cadastrar", on_click=add_input),
                my_table,
                inputcon,
            ]
        )
    )


app(target=main)
