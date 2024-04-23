import flet as ft
from output_settings import OutputSettings
import time
from enum import IntFlag


class can_ids(IntFlag):
    VSet = 0x100
    RelaySet = 0x200
    emeterFeedback = 0x300
    thermistorFeedback = 0x400  # Send 0xFFFF to indicate invalid temperature


outputNames = ["Output 1", "Output 2", "Output 3", "Output 4"]


class SettingsPage(ft.Stack):
    def __init__(self, page, appbar):
        super().__init__()
        self.running = True

        self.controls = []
        self.page = page
        self.appbar = appbar

        self.tx_queue = []
        self.temperature_values = [0, 0, 0, 0]

        self.output_col_1 = OutputSettings(1, self)
        self.output_col_2 = OutputSettings(2, self)
        self.output_col_3 = OutputSettings(3, self)
        self.output_col_4 = OutputSettings(4, self)

        self.show_all_outputs = True

    def did_mount(self):
        self.hide_unused_outputs_checkbox = ft.Checkbox(label="Only show connected outputs", value=False, on_change=lambda _: self.toggle_visible_outputs())

        self.all_controls = ft.Column(
            [
                ft.Row(
                    [
                        self.output_col_1,
                        self.output_col_2,
                        self.output_col_3,
                        self.output_col_4,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Column(
                    [
                        ft.Container(height=4),
                        ft.Text("Main Settings", size=20),
                        self.hide_unused_outputs_checkbox,
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ]
        )

        self.controls.append(self.all_controls)
        self.update()

    def run_can(self):
        while self.running:
            try:
                hndlr_ids = []
                for h_idx, can_handler in enumerate(self.appbar.can_handlers):
                    if can_handler.can_opened == True:
                        hndlr_ids.append(h_idx)

                if len(hndlr_ids) == 0:
                    time.sleep(1)
                    continue

                else:
                    while len(hndlr_ids) != 0:
                        canHandler = self.appbar.can_handlers[hndlr_ids.pop()]

                        for channel in range(canHandler.num_open_channels):
                            # Send messages first
                            while len(self.tx_queue) != 0:
                                message = self.tx_queue[0]
                                canHandler.send_message(channel, message["id"], message["data"])
                                self.tx_queue.remove(message)

                            # Read afterwards
                            frame = canHandler.read_message(channel)
                            if frame.id == 0:
                                continue

                            if frame.id == can_ids.emeterFeedback:
                                # Add emeter data here
                                output_name = outputNames[frame.data[0]]

                                for plot_dict in self.page.plots_page.plotted_data:
                                    if plot_dict["output_name"] == output_name:
                                        if plot_dict["data_name"] == "Voltage":
                                            plot_data = (frame.data[2]) + ((frame.data[3]) << 8)
                                            plot_data = plot_data * 0.004
                                            self.page.plots_page.add_data(plot_data, plot_dict["plot_index"])

                                        elif plot_dict["data_name"] == "Current":
                                            plot_data = (frame.data[4]) + ((frame.data[5]) << 8)
                                            plot_data = plot_data * (4 / (2**15))
                                            self.page.plots_page.add_data(plot_data, plot_dict["plot_index"])

                                        elif plot_dict["data_name"] == "Power":
                                            plot_data = (frame.data[6]) + ((frame.data[7]) << 8)
                                            self.page.plots_page.add_data(plot_data, plot_dict["plot_index"])

                            elif frame.id == can_ids.thermistorFeedback:
                                self.temperature_values = [0, 0, 0, 0]
                                for i in range(4):
                                    self.temperature_values[i] = frame.data[2 * i] + (frame.data[2 * i + 1] << 8)

                                self.show_hide_outputs()

                                for plot_dict in self.page.plots_page.plotted_data:
                                    if plot_dict["data_name"] == "Temperature":
                                        output_id = outputNames.index(plot_dict["output_name"])
                                        if self.temperature_values[output_id] != 0xFFFF:
                                            self.page.plots_page.add_data(self.temperature_values[output_id] / 100, plot_dict["plot_index"])

            except KeyboardInterrupt:
                exit()

        for handler in self.appbar.can_handlers:
            for channel in range(handler.num_open_channels):
                handler.close_channel(channel)

    def add_message_can_queue(self, id, data):
        self.tx_queue.append({"id": id, "data": data})

    def toggle_visible_outputs(self):
        self.show_all_outputs = not self.hide_unused_outputs_checkbox.value
        self.show_hide_outputs()

    def show_hide_outputs(self):
        if self.show_all_outputs:
            self.output_col_1.visible = True
            self.output_col_2.visible = True
            self.output_col_3.visible = True
            self.output_col_4.visible = True

        else:
            self.output_col_1.visible = True if self.temperature_values[0] != 0xFFFF else False
            self.output_col_2.visible = True if self.temperature_values[1] != 0xFFFF else False
            self.output_col_3.visible = True if self.temperature_values[2] != 0xFFFF else False
            self.output_col_4.visible = True if self.temperature_values[3] != 0xFFFF else False

        self.update()
