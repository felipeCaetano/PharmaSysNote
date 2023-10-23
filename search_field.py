from flet_core import UserControl, TextField, TextAlign, IconButton, icons, \
    Row, FloatingActionButton


class SearchField(UserControl):
    def __init__(self, app):
        super(SearchField, self).__init__()
        self.app = app
        self.search_field = TextField(
            text_align=TextAlign.LEFT,
            hint_text="Digite ou Pesquise",
            suffix=IconButton(icon=icons.SEARCH,
                              on_click=self.app.search_item_clicked),
            on_change=self.app.searchbox_changed,
            expand=True
        )

    def build(self):
        self.view = Row(width=self.app.page.window_width // 1.5,
                        controls=[self.search_field,
                                  FloatingActionButton(
                                      icon=icons.ADD,
                                      on_click=self.app.add_clicked
                                  )],
                        )
        return self.view
