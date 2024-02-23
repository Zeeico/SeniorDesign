import flet as ft


class OutputSettings(ft.Column):
    def __init__(self, output_num):
        super().__init__()
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.output_num = output_num

    def did_mount(self):
        self.header_text = ft.Text(f"Output {self.output_num} Settings", size=20)

        self.relay_checkbox = ft.Checkbox(label="Relay status", value=False)

        self.v3_3_btn = ft.FilledButton(text="3.3 V", expand=True, col={"md": 16, "lg": 8})
        self.v5_btn = ft.FilledButton(text="5 V", expand=True, col={"md": 16, "lg": 8})
        self.v12_btn = ft.FilledButton(text="12 V", expand=True, col={"md": 16, "lg": 8})
        self.v22_btn = ft.FilledButton(text="22 V", expand=True, col={"md": 16, "lg": 8})

        self.vout_btn_row = ft.ResponsiveRow([self.v3_3_btn, self.v5_btn, self.v12_btn, self.v22_btn], alignment=ft.MainAxisAlignment.CENTER, columns=16)

        self.vout_slider = ft.Slider(min=0, max=22, divisions=221, label="{value} V", round=1)  # 221 = (22 * 10) + 1, for a tick every 0.1 V

        self.all_controls = [
            ft.Container(height=4),
            self.header_text,
            self.relay_checkbox,
            self.vout_btn_row,
            ft.Container(height=7),
            self.vout_slider,
        ]

        self.controls.extend(self.all_controls)
