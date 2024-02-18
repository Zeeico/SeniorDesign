import flet as ft


class SettingsPage(ft.Stack):
    def __init__(self, page):
        super().__init__()

        self.controls = []
        self.page = page

    def did_mount(self):
        self.all_controls = ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Container(height=4),
                                ft.Text("Main Settings", size=20),
                            ],
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Container(height=4),
                                ft.Text("Output 1 Settings", size=20),
                            ],
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Container(height=4),
                                ft.Text("Output 2 Settings", size=20),
                            ],
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Container(height=4),
                                ft.Text("Output 3 Settings", size=20),
                            ],
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Container(height=4),
                                ft.Text("Output 4 Settings", size=20),
                            ],
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            ]
        )

        self.controls.append(self.all_controls)
        self.update()
