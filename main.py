import flet as ft
from flet_core import Row

from pharmasysapp import PharmaSysNoteApp


def main(page: ft.Page):
    page.title = "PharmaSys"
    page.horizontal_alignment = "center"
    page.update()
    app = PharmaSysNoteApp(page)
    page.add(Row([app], expand=True))


ft.app(target=main)
