import flet as ft

from appstrings import PAGE_APP_BAR_TITLE, PAGE_TITLE
from pharmasysapp import pharma_sys_note_app


def main(page: ft.Page):
    page.title = PAGE_TITLE
    page.horizontal_alignment = "center"
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.CREATE),
        leading_width=40,
        title=ft.Text(PAGE_APP_BAR_TITLE),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT
    )
    pharma_sys_note_app(page)
    page.update()


ft.app(target=main)
