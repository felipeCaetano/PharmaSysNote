from flet_core import UserControl, TextField, TextAlign, IconButton, icons, \
    Row, FloatingActionButton, Column

from annotation import Anotation


class SearchField(UserControl):
    anotation = Column()

    def __init__(self, anotations):
        super(SearchField, self).__init__()
        self.anotation = anotations
        self.search_field = TextField(
            text_align=TextAlign.LEFT,
            hint_text="Digite ou Pesquise",
            suffix=IconButton(icon=icons.SEARCH,
                              # on_click=self.app.search_item_clicked
                              ),
            # on_change=self.app.searchbox_changed,
            expand=True
        )

    def anotation_save(self, e):
        print("depois eu")

    def anotation_edit(self, e):
        pass

    def anotation_delete(self, e):
        pass

    def field_change(self, e):
        pass

    def build(self):
        def add_clicked(e):
            print("clicou no mais")
            anotacao = Anotation(
                self.anotation_save, self.anotation_edit,
                self.anotation_delete, self.field_change
            )
            anotacao.item_name_field.value = self.search_field.value  # search_field.value
            self.anotation.controls.append(anotacao)
            self.anotation.update()
            self.update()

        self.view = Row(
            controls=[self.search_field,
                      FloatingActionButton(
                          icon=icons.ADD,
                          on_click=add_clicked
                      )
                      ],
        )
        return self.view
