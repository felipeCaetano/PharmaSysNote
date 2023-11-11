import flet as ft


def main(page: ft.Page):
    c = ft.Container(
        width=150,
        height=150,
        bgcolor="blue",
        border_radius=10,
        offset=ft.transform.Offset(-2, 0),
        animate_offset=ft.animation.Animation(1000),
        content=ft.Text("AQUI")
    )

    def animate(e):
        c.offset = ft.transform.Offset(0, 0)
        c.update()

    page.add(
        ft.Text("não coluna"),
        c,
        ft.Column([ft.Text("coluna"), c]),

        ft.ElevatedButton("Reveal!", on_click=animate),
    )


ft.app(target=main)
