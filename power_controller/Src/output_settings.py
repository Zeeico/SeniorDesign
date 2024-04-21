import flet as ft
from enum import IntFlag


class can_ids(IntFlag):
    VSet = 0x100
    RelaySet = 0x200
    emeterFeedback = 0x300
    thermistorFeedback = 0x400  # Send 0xFFFF to indicate invalid temperature


class OutputSettings(ft.Column):
    def __init__(self, output_num, settings_page):
        super().__init__()
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.output_num = output_num
        self.settings_page = settings_page

    def did_mount(self):
        self.header_text = ft.Text(f"Output {self.output_num} Settings", size=20)

        self.relay_checkbox = ft.Checkbox(label="Relay command", value=False, on_change=lambda _: self.relay_cmd())
        self.relay_status = ft.Icon(ft.icons.CLOSE_ROUNDED, color=ft.colors.RED)

        self.v3_3_btn = ft.FilledButton(text="3.3 V", expand=True, col={"md": 16, "lg": 8}, on_click=lambda _: self.vout_set(3.3))
        self.v5_btn = ft.FilledButton(text="5 V", expand=True, col={"md": 16, "lg": 8}, on_click=lambda _: self.vout_set(5))
        self.v12_btn = ft.FilledButton(text="12 V", expand=True, col={"md": 16, "lg": 8}, on_click=lambda _: self.vout_set(12))
        self.v24_btn = ft.FilledButton(text="24 V", expand=True, col={"md": 16, "lg": 8}, on_click=lambda _: self.vout_set(24))

        self.reset_controller_btn = ft.FilledButton(text="Reset Controller", on_click=lambda _: self.reset_controller())

        self.vout_btn_row = ft.ResponsiveRow([self.v3_3_btn, self.v5_btn, self.v12_btn, self.v24_btn], alignment=ft.MainAxisAlignment.CENTER, columns=16)

        # 241 = (24 * 10) + 1, for a tick every 0.1 V
        self.vout_slider = ft.Slider(min=0, max=24, divisions=241, label="{value} V", round=1, on_change_end=lambda e: self.vout_set(round(e.control.value, 1)))

        self.vout_text = ft.Text("No output", size=15, text_align=ft.TextAlign.LEFT)

        self.all_controls = [
            ft.Container(height=4),
            self.header_text,
            ft.Row([self.relay_checkbox, self.relay_status]),
            self.reset_controller_btn,
            self.vout_btn_row,
            ft.Container(height=7),
            self.vout_slider,
            ft.Row([self.vout_text, ft.Container(expand=True)]),
        ]

        self.controls.extend(self.all_controls)
        self.update()

    def vout_set(self, voltage):
        self.vout_slider.value = voltage
        self.vout_text.value = f"Output: {voltage} V"

        millivolts = int(voltage * 1000)

        can_data = [0, 0, 0, 0, 0, 0, 0, 0]
        can_data[0] = self.output_num - 1

        can_data[1] = millivolts & 0xFF
        can_data[2] = (millivolts >> 8) & 0xFF

        self.settings_page.add_message_can_queue(can_ids.VSet, can_data)

        self.update()

    def relay_cmd(self):
        if self.relay_checkbox.value:
            self.relay_status.name = ft.icons.CHECK_ROUNDED
            self.relay_status.color = ft.colors.GREEN
        else:
            self.relay_status.name = ft.icons.CLOSE_ROUNDED
            self.relay_status.color = ft.colors.RED

        can_data = [0, 0, 0, 0, 0, 0, 0, 0]
        can_data[0] = self.output_num - 1
        can_data[1] = self.relay_checkbox.value

        self.settings_page.add_message_can_queue(can_ids.RelaySet, can_data)

        self.update()

    def reset_controller(self):
        can_data = [0, 0, 0, 0, 0, 0, 0, 0]
        can_data[0] = self.output_num - 1
        can_data[1] = 0xFE
        can_data[2] = 0xFE

        self.settings_page.add_message_can_queue(can_ids.VSet, can_data)

        self.update()
