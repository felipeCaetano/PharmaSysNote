import flet as ft
from flet_core import UserControl, TextField, TextAlign, IconButton, icons, \
    Row, FloatingActionButton


class SearchField(UserControl):
    def __init__(self, app):
        super(SearchField, self).__init__()
        self.app = app
        self.search_field = TextField(
            text_align=TextAlign.LEFT,
            hint_text="Digite ou Pesquise",
            suffix=IconButton(icon=icons.SEARCH,),
            expand=True
        )

    def build(self):
        self.view = Row(
                        controls=[self.search_field,
                                  FloatingActionButton(
                                      icon=icons.ADD,
                                  )],
                        )
        return self.view


def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("Anotador do PharmaSys"),)
    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Tab 1",
                content=ft.Container(
                    content=SearchField(ft.app)
                ),
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=100,
        leading=ft.FloatingActionButton(icon=ft.icons.LOCAL_PHARMACY,
                                        text="PharmaSys"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.CREATE,
                selected_icon=ft.icons.CREATE_OUTLINED,
                icon_content=ft.IconButton(),
                label="Anotações"
            ),
        ],
        # on_change=lambda e: print("Selected destination:",
        #                           e.control.selected_index),
    )

    page.add(
        ft.Row(
            [
               rail,
                ft.VerticalDivider(width=1),
                t
            ],
            expand=True
        )
    )

ft.app(target=main)
