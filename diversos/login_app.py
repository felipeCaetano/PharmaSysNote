import flet
import requests
from flet import Page, Text, Column, Row
from flet_core import SnackBar, LinearGradient, alignment, TextField, View, \
    Card, Container, padding, border_radius, FilledButton
from flet_core.types import MainAxisAlignment, CrossAxisAlignment


def main(page: Page):
    page.title = "Login"

    snack = SnackBar(
        Text("Registration successfull!")
    )

    def GradientGenerator(start, end):
        ColorGradient = LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=[start, end]
        )
        return ColorGradient

    def reg_register(event, email, password):
        data = {
            "email": email,
            "password": password
        }
        res = requests.post("http://127.0.0.1:5000/register", json=data)

        if res.status_code == 201:
            snack.open = True
            page.update()
        else:
            snack.content.value = "You were not registered! Try again"
            snack.open = True
            page.update()

    def reg_login(event, email, password):
        data = {
            "email": email,
            "password": password
        }
        res = requests.post("http://127.0.0.1:5000/login", json=data)

        if res.status_code == 201:
            snack.open = True
            page.update()

    def route_change(route):
        email = TextField(
            label="Email",
            border="underline",
            width=180,
            text_size=14,
            color='white'
        )
        password = TextField(
            label="PassWord",
            border="underline",
            width=180,
            text_size=14,
            color='white',
            password=True,
            can_reveal_password=True
        )
        page.views.clear()
        page.views.append(
            View(
                "/register",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                vertical_alignment=MainAxisAlignment.CENTER,
                controls=[Column(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Card(
                            elevation=15,
                            content=Container(
                                width=550,
                                height=550,
                                padding=padding.all(30),
                                gradient=GradientGenerator(
                                    "#2f2937", "#251827"
                                ),
                                border_radius=border_radius.all(12),
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.START,
                                    controls=[Text(
                                        "Mock Registration",
                                        size=32,
                                        weight="w700",
                                        text_align=alignment.center,
                                        color="#64748b"
                                    ),
                                        Text(
                                            "This is web-app/registration page",
                                            size=14,
                                            weight="w700",
                                            text_align=alignment.center,
                                            color="#64748b"
                                        ),
                                        Container(
                                            padding=padding.only(bottom=20)
                                        ),
                                        email,
                                        Container(
                                            padding=padding.only(bottom=20)
                                        ),
                                        password,
                                        Container(
                                            padding=padding.only(bottom=20)),
                                        Row(
                                            alignment="center",
                                            spacing=20,
                                            controls=[
                                                FilledButton(
                                                    content=Text(
                                                        "Register",
                                                        weight="w700",
                                                    ),
                                                    width=160,
                                                    height=40,
                                                    on_click=lambda
                                                        e: reg_register(
                                                        e,
                                                        email.value,
                                                        password.value,
                                                    )
                                                ),
                                                FilledButton(
                                                    content=Text(
                                                        "Login",
                                                        weight="w700",
                                                    ),
                                                    width=160,
                                                    height=40,
                                                    on_click=lambda
                                                        e: reg_register(
                                                        e,
                                                        email.value,
                                                        password.value,
                                                    )
                                                ),
                                            ]
                                        )
                                    ]
                                )
                            )
                        )
                    ]
                )
                ]
            )
        )
        if route == "/login":
            page.views.append(
                View(
                    "/login",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Column(
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Card(
                                    elevation=15,
                                    content=Container(
                                        width=550,
                                        height=550,
                                        padding=padding.all(30),
                                        gradient=GradientGenerator('#2f2937',
                                                                   '#251867'),
                                        border_radius=border_radius.all(12),
                                        content=Column(
                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                            alignment=MainAxisAlignment.START,
                                            controls=[
                                                Text(
                                                    "Mock Registration",
                                                    size=32,
                                                    weight="w700",
                                                    text_align=alignment.center,
                                                    color="#64748b"
                                                ),
                                                Text(
                                                    "This is web-app/login page",
                                                    size=14,
                                                    weight="w700",
                                                    text_align=alignment.center,
                                                    color="#64748b"
                                                ),
                                                Container(
                                                    padding=padding.only(
                                                        bottom=20)
                                                ),
                                                email,
                                                Container(padding=padding.only(
                                                    bottom=10)
                                                ),
                                                password,
                                                Container(padding=padding.only(
                                                    bottom=20)
                                                ),
                                                Row(
                                                    alignment="center",
                                                    spacing=20,
                                                    controls=[
                                                        FilledButton(
                                                            content=Text(
                                                                "Login",
                                                                weight="w700",
                                                            ),
                                                            width=160,
                                                            height=40,
                                                            on_click=lambda
                                                                e: reg_login(
                                                                e,
                                                                email.value,
                                                                password.value,
                                                            )
                                                        ),
                                                        FilledButton(
                                                            content=Text(
                                                                "Create Account",
                                                                weight="w700",
                                                            ),
                                                            width=160,
                                                            height=40,
                                                            on_click=lambda
                                                                _: page.go(
                                                                "register",
                                                                email.value,
                                                                password.value,
                                                            )
                                                        ),
                                                    ]
                                                )
                                            ]
                                        )
                                    )
                                )
                            ]
                        )
                    ]
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


flet.app(target=main, view=flet.WEB_BROWSER)
# host="localhost", port=51271,
