import flet as ft
from enum import IntFlag


class can_ids(IntFlag):
    VSet = 0x100
    RelaySet = 0x200
    EmeterFeedback = 0x300
    ThermistorFeedback = 0x400  # Send 0xFFFF to indicate invalid temperature
    RelayFeedback = 0x500
    SignOfLife = 0x600


class OutputSettings(ft.Column):
    def __init__(self, output_num, settings_page):
        super().__init__()
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.detected = False
        self.relay_enabled = False
        self.output_num = output_num
        self.settings_page = settings_page

    def did_mount(self):
        self.header_text = ft.Text(f"Output {self.output_num} Settings", size=20)

        self.connection_text = ft.Text("Board Not Detected")
        self.connection_status = ft.Icon(ft.icons.LINK_OFF_ROUNDED, color=ft.colors.RED)

        self.relay_checkbox = ft.Checkbox(label="Relay command", value=False, on_change=lambda _: self.relay_cmd())
        self.relay_status = ft.Icon(ft.icons.CLOSE_ROUNDED, color=ft.colors.RED)

        self.v3_3_btn = ft.FilledButton(text="3.3 V", expand=True, col={"md": 16, "lg": 8, "xxl": 4}, on_click=lambda _: self.vout_set(3.3))
        self.v5_btn = ft.FilledButton(text="5 V", expand=True, col={"md": 16, "lg": 8, "xxl": 4}, on_click=lambda _: self.vout_set(5))
        self.v12_btn = ft.FilledButton(text="12 V", expand=True, col={"md": 16, "lg": 8, "xxl": 4}, on_click=lambda _: self.vout_set(12))
        self.v24_btn = ft.FilledButton(text="24 V", expand=True, col={"md": 16, "lg": 8, "xxl": 4}, on_click=lambda _: self.vout_set(24))

        self.vout_btn_row = ft.ResponsiveRow([self.v3_3_btn, self.v5_btn, self.v12_btn, self.v24_btn], alignment=ft.MainAxisAlignment.CENTER, columns=16)

        self.reset_controller_btn = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("Reset Controller", text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            col={"lg": 16, "xl": 8},
            on_click=lambda _: self.reset_controller(),
        )

        self.turn_off_output_btn = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("Turn Off Output", text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            col={"lg": 16, "xl": 8},
            on_click=lambda _: self.turn_off_output(),
        )

        self.controller_reset_row = ft.ResponsiveRow([self.reset_controller_btn, self.turn_off_output_btn], alignment=ft.MainAxisAlignment.CENTER, columns=16)

        self.vout_slider = ft.Slider(min=0, max=24, divisions=240, label="{value} V", round=1, on_change_end=lambda e: self.vout_set(round(e.control.value, 1)))

        self.vout_text = ft.Text("No output", size=15, text_align=ft.TextAlign.LEFT)

        self.all_controls = [
            ft.Container(height=4),
            self.header_text,
            ft.Row([self.connection_text, self.connection_status], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.relay_checkbox, self.relay_status], alignment=ft.MainAxisAlignment.CENTER),
            self.controller_reset_row,
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
        can_data = [0, 0, 0, 0, 0, 0, 0, 0]
        can_data[0] = self.output_num - 1
        can_data[1] = self.relay_checkbox.value

        self.settings_page.add_message_can_queue(can_ids.RelaySet, can_data)

        self.update()

    def update_relay_status(self, status):
        if self.relay_enabled == status:
            return

        self.relay_enabled = status

        if self.relay_enabled:
            self.relay_status.name = ft.icons.CHECK_ROUNDED
            self.relay_status.color = ft.colors.GREEN

            if self.relay_checkbox.value == False:
                self.relay_checkbox.value = True

        else:
            self.relay_status.name = ft.icons.CLOSE_ROUNDED
            self.relay_status.color = ft.colors.RED

            if self.relay_checkbox.value == True:
                self.relay_checkbox.value = False

        self.update()

    def reset_controller(self):
        can_data = [0, 0, 0, 0, 0, 0, 0, 0]
        can_data[0] = self.output_num - 1
        can_data[1] = 0xFE
        can_data[2] = 0xFE

        self.settings_page.add_message_can_queue(can_ids.VSet, can_data)

        self.update()

    def turn_off_output(self):
        can_data = [0, 0, 0, 0, 0, 0, 0, 0]
        can_data[0] = self.output_num - 1
        # Leaving everything else at 0 because we want to send a 0 mV command

        self.settings_page.add_message_can_queue(can_ids.VSet, can_data)

        self.update()

    def set_detected(self, detected):
        if detected == self.detected:
            return

        self.detected = detected
        if self.detected:
            self.connection_status.name = ft.icons.LINK_ROUNDED
            self.connection_status.color = ft.colors.GREEN
            self.connection_text.value = "Board Detected"
        else:
            self.connection_status.name = ft.icons.LINK_OFF_ROUNDED
            self.connection_status.color = ft.colors.RED
            self.connection_text.value = "Board Not Detected"

        self.update()
