import flet as ft
from flet_core import Row

from pharmasysapp import pharma_sys_note_app


def main(page: ft.Page):
    page.title = "PharmaSys"
    page.horizontal_alignment = "center"
    page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.CREATE),
            leading_width=40,
            title=ft.Text("Anotador do PharmaSys"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT)
    # app = PharmaSysNoteApp(page)
    pharma_sys_note_app(page)
    page.update()


ft.app(target=main)
