from flet_core import (UserControl, TextField, TextAlign, IconButton, icons,
                       Row, FloatingActionButton, Column, DataTable,
                       DataColumn, Text)

head_table = DataTable(
    columns=[

        DataColumn(Text("Data e Hora")),
        DataColumn(Text("Nome do Produto")),
        DataColumn(Text("Quantidade")),
        DataColumn(Text("Apresentação")),
        DataColumn(Text("Valor Unitário")),
        DataColumn(Text("Ações")),
    ],
    rows=[],
    visible=False
)


class SearchField(UserControl):
    # anotation = Column()

    def __init__(self, callback, search_engine):
        super(SearchField, self).__init__()
        self.callback = callback
        self.search_function = search_engine
        self.search_field = TextField(
            text_align=TextAlign.LEFT,
            hint_text="Digite ou Pesquise",
            suffix=IconButton(icon=icons.SEARCH,
                              on_click=self.search_function
                              ),
            # on_change=self.app.searchbox_changed,
            expand=True
        )

    def anotation_save(self, e):
        pass

    def anotation_edit(self, e):
        pass

    def anotation_delete(self, e):
        pass

    def field_change(self, e):
        pass

    def build(self):
        self.view = Column([
            Row([
                self.search_field,
                FloatingActionButton(icon=icons.ADD, on_click=self.callback)
            ]),
            head_table]
        )
        return self.view
