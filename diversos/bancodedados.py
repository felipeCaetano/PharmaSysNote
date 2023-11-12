from flet import *
import useraction_table
import sqlite3

conexao = sqlite3.connect("dados.db", check_same_thread=False)
cursor = conexao.cursor()


def tabela_base():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY
        AUTOINCREMENT, nome TEXT)
        """
    )


class App(UserControl):
    def __init__(self):
        super(App, self).__init__()
        self.todos_dados = Column(auto_scroll=True)
        self.adicionar_dados = TextField(label="Adicionar dados")
        self.editar_dados = TextField(label="Editar")

    def add_dados(self, event):
        cursor.execute(
            "INSERT INTO clientes (nome) VALUES (?)", [self.adicionar_dados.value]
        )
        conexao.commit()
        self.adicionar_dados.value = ""
        self.renderizar_todos()
        self.page.update()

    def renderizar_todos(self):
        cursor.execute("SELECT * FROM clientes")
        conexao.commit()
        meus_dados = cursor.fetchall()
        for dado in meus_dados:
            self.todos_dados.controls.append(
                ListTile(
                    subtitle=Text(dado[0]),
                    title=Text(dado[1]),
                    on_click=self.abrir_acoes,
                )
            )
        self.update()

    def abrir_acoes(self, event):
        id_user = event.control.subtitle.value
        self.editar_dados.value = event.control.title.value
        self.update()

        alert_dialog = AlertDialog(
            title=Text(f"Editar ID{id_user}"),
            content=self.editar_dados,
            actions=[
                ElevatedButton(
                    "Deletar",
                    color="white",
                    bgcolor="red",
                    on_click=lambda e: self.deletar(id_user, alert_dialog),
                ),
                ElevatedButton(
                    "Atualizar",
                    on_click=lambda e: self.atualizar(
                        id_user, self.editar_dados, alert_dialog
                    ),
                ),
            ],
            actions_alignment="spaceBetween",
        )
        self.page.dialog = alert_dialog
        alert_dialog.open = True
        self.page.update()

    def deletar(self, id_user, alert):
        cursor.execute("DELETE FROM clientes WHERE  id= ?", [id_user])
        alert.open = False

        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    def atualizar(self, id_user, editar, alert):
        cursor.execute(
            "UPDATE clientes SET nome = ? WHERE id=?", (editar.value, id_user)
        )
        conexao.commit()
        alert.open = False

        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    def ciclo(self):
        self.renderizar_todos()

    def build(self):
        return Column(
            [
                Text("CRUD com SQLite"),
                self.adicionar_dados,
                ElevatedButton("Adicionar", on_click=self.add_dados),
                self.todos_dados,
            ]
        )


def main(page: Page):
    page.add(App())


tabela_base()
app(target=main)
