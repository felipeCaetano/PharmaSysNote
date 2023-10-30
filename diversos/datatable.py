from flet import (
    DataTable, DataColumn, Text, Column, Row, DataRow, DataCell, Container,
    IconButton, TextField, RadioGroup, Radio, ElevatedButton)
import sqlite3

conn = sqlite3.connect("db/dbcad.db", check_same_thread=False)

tb = DataTable(
    columns=[
        DataColumn(Text("actions")),
        DataColumn(Text("name")),
        DataColumn(Text("age")),
        DataColumn(Text("contact")),
        DataColumn(Text("email")),
        DataColumn(Text("address")),
        DataColumn(Text("gender"))
    ],
    rows=[]
)

id_edit = Text()
name_edit = TextField(label="Nome")
age_edit = TextField(label="age")
contact_edit = TextField(label="contact")
gender_edit = RadioGroup(content=Column([
    Radio(value='M', label="Masculino"),
    Radio(value='F', label="Feminino")
]))
email_edit = TextField(label="email")
address_edit = TextField(label="address")


def hidedlg(event):
    dlg.visible = False
    dlg.update()


def saveandupdate(event):
    try:
        myid = id_edit.value
        c = conn.cursor()
        c.execute(
            "UPDATE users SET name=?, contact=?, age=?, gender=?, email=?, address=? WHERE id=?",
            (name_edit.value, contact_edit.value, age_edit.value,
             gender_edit.value, email_edit.value, address_edit.value, myid)
        )
        conn.commit()
        tb.rows.clear()
        calldb()
        dlg.visible = False
        dlg.update()
        tb.update()

    except Exception as e:
        print(e)


def showdelete(event):
    try:
        myid = int(event.control.data)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (myid,))
        conn.commit()
        print('deletado com sucesso')
        tb.rows.clear()
        calldb()
        tb.update()
    except:
        print(e)


dlg = Container(
    bgcolor='green200',
    padding=10,
    content=Column([
        Row([
            Text("Editar Cadastros", size=30, weight='bold'),
            IconButton(icon="Close", on_click=hidedlg)],
            alignment="spaceBetween"),
        name_edit,
        age_edit,
        contact_edit,
        Text("selecione Sexo", size=20, weight='bold'),
        gender_edit,
        email_edit,
        address_edit,
        ElevatedButton("Atualizar", on_click=saveandupdate)]
    )
)


def showedit(event):
    data_edit = event.control.data
    id_edit.value = data_edit['id']
    name_edit.value = data_edit['name']
    age_edit.value = data_edit['age']
    contact_edit.value = data_edit['contact']
    email_edit.value = data_edit['email']
    address_edit.value = data_edit['address']

    dlg.visible = True
    dlg.update()


def calldb():
    c = conn.cursor()
    c.execute("SELECT * from users")
    users = c.fetchall()
    print(users)

    if not users == "":
        keys = ["id", "name", "contact", "age", "email", "address", "gender"]

        result = [dict(zip(keys, values)) for values in users]
        for x in result:
            tb.rows.append(DataRow(
                cells=[DataCell(
                    Row([
                        IconButton(
                            icon="create", icon_color="green", data=x,
                            on_click=showedit),
                        IconButton(
                            icon="delete", icon_color="red", data=x['id'],
                            on_click=showdelete)
                    ])
                    ),
                    DataCell(Text(x["name"])),
                    DataCell(Text(x["age"])),
                    DataCell(Text(x["contact"])),
                    DataCell(Text(x["email"])),
                    DataCell(Text(x["address"])),
                    DataCell(Text(x["gender"]))
                ]
            )
            )


calldb()
dlg.visible = False
my_table = Column(
    [dlg, Row([tb], scroll="always")]
)
