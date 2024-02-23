import flet as ft
from output_settings import OutputSettings


class SettingsPage(ft.Stack):
    def __init__(self, page):
        super().__init__()

        self.controls = []
        self.page = page

        self.output_col_1 = OutputSettings(1)
        self.output_col_2 = OutputSettings(2)
        self.output_col_3 = OutputSettings(3)
        self.output_col_4 = OutputSettings(4)

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
                        self.output_col_1,
                        self.output_col_2,
                        self.output_col_3,
                        self.output_col_4,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            ]
        )

        self.controls.append(self.all_controls)
        self.update()
