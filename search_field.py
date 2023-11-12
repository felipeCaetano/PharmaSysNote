from flet_core import (FloatingActionButton, IconButton, icons, Row, TextAlign,
                       TextField, UserControl)

from appstrings import SEARCH_FIELD


class SearchField(UserControl):
    def __init__(self, callback, search_engine):
        super(SearchField, self).__init__()
        self.view = Row()
        self.callback = callback
        self.search_function = search_engine
        self.search_field = TextField(
            text_align=TextAlign.LEFT,
            hint_text=SEARCH_FIELD,
            expand=True,
            suffix=IconButton(icon=icons.SEARCH, on_click=self.search_function),
        )

    def build(self):
        self.search_field.suffix.data = self.search_field.value
        self.view.controls.append(self.search_field)
        self.view.controls.append(
            FloatingActionButton(icon=icons.ADD, on_click=self.callback)
        )
        return self.view
