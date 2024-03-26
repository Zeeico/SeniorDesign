import flet as ft


class OutputSettings(ft.Column):
    def __init__(self, output_num):
        super().__init__()
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.output_num = output_num

    def did_mount(self):
        self.header_text = ft.Text(f"Output {self.output_num} Settings", size=20)

        self.relay_checkbox = ft.Checkbox(label="Relay command", value=False, on_change=lambda _: self.relay_cmd())
        self.relay_status = ft.Icon(ft.icons.QUESTION_MARK_ROUNDED, color=ft.colors.GREY)

        self.v3_3_btn = ft.FilledButton(text="3.3 V", expand=True, col={"md": 16, "lg": 8}, on_click=lambda _: self.vout_set(3.3))
        self.v5_btn = ft.FilledButton(text="5 V", expand=True, col={"md": 16, "lg": 8}, on_click=lambda _: self.vout_set(5))
        self.v12_btn = ft.FilledButton(text="12 V", expand=True, col={"md": 16, "lg": 8}, on_click=lambda _: self.vout_set(12))
        self.v22_btn = ft.FilledButton(text="24 V", expand=True, col={"md": 16, "lg": 8}, on_click=lambda _: self.vout_set(24))

        self.vout_btn_row = ft.ResponsiveRow([self.v3_3_btn, self.v5_btn, self.v12_btn, self.v22_btn], alignment=ft.MainAxisAlignment.CENTER, columns=16)

        # 221 = (22 * 10) + 1, for a tick every 0.1 V
        self.vout_slider = ft.Slider(min=0, max=24, divisions=241, label="{value} V", round=1, on_change_end=lambda e: self.vout_set(round(e.control.value, 1)))

        self.vout_text = ft.Text("No output", size=15, text_align=ft.TextAlign.LEFT)

        self.all_controls = [
            ft.Container(height=4),
            self.header_text,
            ft.Row([self.relay_checkbox, self.relay_status]),
            self.vout_btn_row,
            ft.Container(height=7),
            self.vout_slider,
            ft.Row([self.vout_text, ft.Container(expand=True)]),
        ]

        self.controls.extend(self.all_controls)

    def vout_set(self, voltage):
        self.vout_slider.value = voltage
        self.vout_text.value = f"Output: {voltage} V"

        # Send can message to set voltage value

        self.update()

    def relay_cmd(self):
        if self.relay_checkbox.value:
            self.relay_status.name = ft.icons.CHECK_ROUNDED
            self.relay_status.color = ft.colors.GREEN
        else:
            self.relay_status.name = ft.icons.CLOSE_ROUNDED
            self.relay_status.color = ft.colors.RED
        self.update()
