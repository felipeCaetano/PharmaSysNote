import flet as ft
from flet_core import CrossAxisAlignment
from appstrings import PAGE_APP_BAR_TITLE, PAGE_TITLE
from pharmasysapp import pharma_sys_note_app, PharmasysApp


def main(page: ft.Page):
    page.bgcolor = "#fdfdfd"
    page.title = PAGE_TITLE
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.padding = 20
    # page.appbar = ft.AppBar(
    #     leading=ft.Icon(ft.icons.CREATE),
    #     leading_width=40,
    #     title=ft.Text(PAGE_APP_BAR_TITLE),
    #     center_title=False,
    #     bgcolor=ft.colors.SURFACE_VARIANT,
    #
    # )

    def router(route: ft.View):
        page.views.clear()

        if page.route == '/':
            view = PharmasysApp(route.page)
            page.views.append(view)
            print("printando o app")
        else:
            page.views.append(
                ft.View("ERROR", [ft.Text("Algo deu errado!")])
            )

        page.update()

    page.on_route_change = router
    page.go(page.route)


ft.app(target=main)
