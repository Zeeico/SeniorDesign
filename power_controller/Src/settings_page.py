import flet as ft
from output_settings import OutputSettings
import time
from enum import IntFlag


class can_ids(IntFlag):
    VSet = 0x100
    RelaySet = 0x200
    emeterFeedback = 0x300


outputNames = {0: "Output 1", 1: "Output 2", 2: "Output 3", 3: "Output 4"}


class SettingsPage(ft.Stack):
    def __init__(self, page, appbar):
        super().__init__()
        self.running = True

        self.controls = []
        self.page = page
        self.appbar = appbar

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
                                            self.page.plots_page.add_data(plot_data, plot_dict["plot_index"])

                                        elif plot_dict["data_name"] == "Current":
                                            plot_data = (frame.data[4]) + ((frame.data[5]) << 8)
                                            self.page.plots_page.add_data(plot_data, plot_dict["plot_index"])

                                        elif plot_dict["data_name"] == "Power":
                                            plot_data = (frame.data[6]) + ((frame.data[7]) << 8)
                                            self.page.plots_page.add_data(plot_data, plot_dict["plot_index"])

            except KeyboardInterrupt:
                exit()

        for handler in self.appbar.can_handlers:
            handler.close_channel()
