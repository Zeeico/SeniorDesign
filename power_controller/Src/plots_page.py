import flet as ft
from plotting import Plotting
from plot_legend import PlotLegend
import re
import time
from math import pi

unit_dict = {"Voltage": "V", "Current": "A", "Power": "W", "Temperature": "C"}


# The page housing the chart as well as all the necessary controls
class PlotsPage(ft.Stack):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.start_time = 0
        self.plots = [Plotting(self)]  # The actual charts
        self.plotted_data = []  # Keeps track of what data the chart is displaying
        self.num_data_series = 0
        self.num_series_per_plot = [0]
        self.data_location = []

        # Option lists for the dropdowns
        self.output_options = [
            ft.dropdown.Option("Output 1"),
            ft.dropdown.Option("Output 2"),
            ft.dropdown.Option("Output 3"),
            ft.dropdown.Option("Output 4"),
        ]
        self.data_options = [
            ft.dropdown.Option("Voltage"),
            ft.dropdown.Option("Current"),
            ft.dropdown.Option("Power"),
            ft.dropdown.Option("Temperature"),
        ]

        # Legends and a couple buttons to control each data series
        self.legends = ft.ListView(controls=[], spacing=10, width=250)  # , expand=True)

        self.picked_color = None  # Which color is currently selected

        # Dict of the colors that can be picked and containers that can be used to select them
        self.colors = {
            ft.colors.LIGHT_GREEN: self.color_option_creator(ft.colors.LIGHT_GREEN),
            ft.colors.RED_200: self.color_option_creator(ft.colors.RED_200),
            ft.colors.AMBER_500: self.color_option_creator(ft.colors.AMBER_500),
            ft.colors.PINK_300: self.color_option_creator(ft.colors.PINK_300),
            ft.colors.ORANGE_300: self.color_option_creator(ft.colors.ORANGE_300),
            ft.colors.LIGHT_BLUE: self.color_option_creator(ft.colors.LIGHT_BLUE),
            ft.colors.DEEP_ORANGE_300: self.color_option_creator(ft.colors.DEEP_ORANGE_300),
            ft.colors.PURPLE_100: self.color_option_creator(ft.colors.PURPLE_100),
            ft.colors.RED_700: self.color_option_creator(ft.colors.RED_700),
            ft.colors.TEAL_500: self.color_option_creator(ft.colors.TEAL_500),
            ft.colors.YELLOW_400: self.color_option_creator(ft.colors.YELLOW_400),
            ft.colors.PURPLE_400: self.color_option_creator(ft.colors.PURPLE_400),
            ft.colors.BROWN_300: self.color_option_creator(ft.colors.BROWN_300),
            ft.colors.CYAN_500: self.color_option_creator(ft.colors.CYAN_500),
            ft.colors.BLUE_GREY_500: self.color_option_creator(ft.colors.BLUE_GREY_500),
        }

    def did_mount(self):
        # All the buttons used to control stuff about the chart
        primary_button_style = ft.ButtonStyle(bgcolor=ft.colors.OUTLINE_VARIANT, side=ft.BorderSide(width=0, color=ft.colors.OUTLINE_VARIANT))

        self.sliding_button = ft.OutlinedButton("Slide", on_click=self.toggle_slide, style=primary_button_style, width=95)
        self.plot_curved = ft.OutlinedButton("Curve", on_click=self.toggle_rounded, style=primary_button_style, width=95)
        self.plot_animate = ft.OutlinedButton("Animate", on_click=self.toggle_animate, style=primary_button_style, width=115)
        self.plot_clear = ft.OutlinedButton("Clear data", on_click=self.clear_data, style=primary_button_style, width=115)
        self.color_picker_btn = ft.IconButton(ft.icons.PALETTE_ROUNDED, tooltip="Color Picker", on_click=self.open_color_picker)
        self.set_plot_btn = ft.OutlinedButton("Select plot source", on_click=self.add_data_series, style=primary_button_style, expand=True)

        self.add_plot_btn = ft.IconButton(ft.icons.ADD_CIRCLE_ROUNDED, on_click=self.add_plot, tooltip="Add a chart")
        self.rm_plot_btn = ft.IconButton(ft.icons.REMOVE_CIRCLE_ROUNDED, on_click=self.rm_plot, tooltip="Remove the last chart", disabled=True)

        # Dropdown with all the PGNs that can be charted
        self.all_pgns_dropdown = ft.Dropdown(
            label="Outputs",
            hint_text="Source output for the plots",
            options=self.output_options,
            # on_change=self.populate_data_dropdown,
            alignment=ft.alignment.center_left,
            width=250,
        )

        # Dropdown that updated when a PGN is selected with its data options
        self.data_to_display_dropdown = ft.Dropdown(
            label="Data",
            hint_text="Data to display",
            options=self.data_options,
            alignment=ft.alignment.center_left,
            width=250,
        )

        self.plot_select_text = ft.Text("Select the signal's plot", text_align=ft.TextAlign.CENTER)
        self.plot_num_select = ft.Slider(min=0, max=0, divisions=1, label="Plot {value}", width=250, disabled=True, value=0)

        # Button to hide or show the plotting menu
        self.show_menu_btn = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD_IOS_ROUNDED,
            icon_size=25,
            tooltip="Hide plotting menu",
            on_click=self.show_menu,
            animate_rotation=ft.Animation(200, ft.AnimationCurve.LINEAR),
            rotate=pi,
        )

        # Laying out all the buttons
        self.plot_menu = ft.Column(
            [
                ft.Row(
                    [self.sliding_button, self.plot_clear, self.add_plot_btn],
                    width=250,
                    spacing=5,
                ),
                ft.Row(
                    [self.plot_curved, self.plot_animate, self.rm_plot_btn],
                    width=250,
                    spacing=5,
                ),
                self.all_pgns_dropdown,
                self.data_to_display_dropdown,
                self.plot_select_text,
                self.plot_num_select,
                ft.Row([self.set_plot_btn, self.color_picker_btn], width=250, spacing=5),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=5,
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(200, ft.AnimationCurve.LINEAR),
            on_animation_end=self.anim_end_callback,
        )

        # Grid view that will contain the color options
        self.color_options = ft.GridView(runs_count=3, max_extent=40, data="", height=150)

        # Add the color options to the grid view
        for key, val in self.colors.items():
            self.color_options.controls.append(val)

        # Alert dialog used to show the color picker as a pop up window. Needs to be linked to the page
        self.color_picker = ft.AlertDialog(title=ft.Text("Color Picker", text_align=ft.TextAlign.CENTER), content=self.color_options)
        self.page.dialog = self.color_picker

        self.charts = ft.Column([self.plots[0].chart], expand=True)

        # All the controls on the page
        self.all_controls = ft.Column(
            [
                ft.Container(height=2),
                ft.Row(
                    [
                        ft.Column(
                            [
                                self.show_menu_btn,
                                self.plot_menu,
                            ]
                        ),
                        self.legends,
                        self.charts,
                        ft.Container(width=2),
                    ],
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            expand=True,
        )

        # Add all the controls
        self.controls.append(self.all_controls)
        self.update()

    # Callback function to hide and show the menu
    def show_menu(self, e):
        if self.show_menu_btn.rotate == pi:
            self.show_menu_btn.rotate = 2 * pi
        else:
            self.show_menu_btn.rotate = pi

        if self.plot_menu.visible == False:
            self.plot_menu.visible = True
            self.update()
            time.sleep(0.1)

        if self.plot_menu.offset == ft.Offset(0, 0):
            self.plot_menu.offset = ft.Offset(-1, 0)
        else:
            self.plot_menu.offset = ft.Offset(0, 0)

        self.update()

    def anim_end_callback(self, e):
        self.show_menu_btn.tooltip = "Hide plotting menu"

        if self.plot_menu.offset == ft.Offset(-1, 0):
            self.plot_menu.visible = False
            self.show_menu_btn.tooltip = "Show plotting menu"

        self.update()

    # Callback functions simply calling the matching function in the plots themselves
    def toggle_slide(self, e):
        for p in self.plots:
            p.toggle_slide()

    def toggle_rounded(self, e):
        for p in self.plots:
            p.toggle_rounded()

    def toggle_animate(self, e):
        for p in self.plots:
            p.toggle_animate()

    def clear_data(self, e):
        self.start_time = 0
        for p in self.plots:
            p.clear_data()

    # Callback function to add a plot to the page
    def add_plot(self, e):
        self.plot_num_select.disabled = False  # When we add a plot, we have to be able to select it

        # Create the plot and add it to the relevant lists
        new_plot = Plotting(self)
        self.plots.append(new_plot)
        self.charts.controls.append(new_plot.chart)

        # Modify other variables to indicate the new plat
        self.num_series_per_plot.append(0)
        self.plot_num_select.max += 1
        self.plot_num_select.divisions = self.plot_num_select.max

        if len(self.charts.controls) == 5:  # Can't add more than 5 plots
            self.add_plot_btn.disabled = True

        if self.rm_plot_btn.disabled == True:  # When we add a plot, we have to be able to remove it
            self.rm_plot_btn.disabled = False

        for p in self.plots:  # Update the y axis labels for all the plots to update the scaling
            p.update_y_labels()

        self.update()

    def rm_plot(self, e):
        if len(self.charts.controls) <= 1:  # Should never be true, but added just in case
            return

        # Remove stuff that was in removed plot from self.data_location, self.plotted_data, updated the indices
        for l in reversed(self.legends.controls):  # Using reversed since otherwise some would be missed
            if l.chart_index == self.plot_num_select.max:
                l.delete_callback(0)

        # Then update all the variables and lists to indicate the plot was removed
        self.charts.controls.pop()
        self.plots.pop()
        if self.plot_num_select.value == self.plot_num_select.max:
            self.plot_num_select.value -= 1

        self.plot_num_select.max -= 1

        if self.plot_num_select.max == 0:
            self.plot_num_select.divisions = 1

        else:
            self.plot_num_select.divisions = self.plot_num_select.max

        self.num_series_per_plot.pop(self.plot_num_select.max + 1)

        if len(self.charts.controls) == 1:
            self.rm_plot_btn.disabled = True

        if self.add_plot_btn.disabled == True:
            self.add_plot_btn.disabled = False

        for p in self.plots:  # Update the y axis labels for all the plots to update the scaling
            p.update_y_labels()

        self.update()

    def set_color(self, e):
        # Callback function when a color is clicked on the color picker
        for key, val in self.colors.items():
            # If we're looking at the clicked color
            if key == e.control.data:
                # Set the picked_color
                val.border = ft.border.all(3, color=ft.colors.TERTIARY)
                self.picked_color = key

            else:
                val.border = None  # Mark all other colors as not selected

        # If a valid color is picked, close the pop up
        self.color_picker.open = False

        self.page.update()

    def color_option_creator(self, color):
        # Create a clickable container displaying the color
        return ft.Container(bgcolor=color, border_radius=ft.border_radius.all(50), height=10, width=10, padding=ft.padding.all(5), data=color, on_click=self.set_color)

    def open_color_picker(self, e):
        # Callback function for a button, simply opens the color picker
        for key, val in self.colors.items():
            val.border = None

        self.color_picker.open = True
        self.page.update()

    def populate_data_dropdown(self, e):
        # Function that updates the data_to_display_dropdown options
        # based on the newly selected PGN
        pgn_name = self.all_pgns_dropdown.value  # Get the PGN name

        for pgn in self.page.n2k_msg_list:  # Find the matching PGN value
            if pgn.name == pgn_name:
                break

        # Populate the data options for the dropdown
        data_options = []
        for data_name in pgn.data_list:
            data_options.append(ft.dropdown.Option(data_name))

        self.data_to_display_dropdown.options = data_options
        self.update()

    def make_legend(self, title, subtitle, color, chart_index):
        # Create a legend for a new data series
        return PlotLegend(self.num_data_series, title, subtitle, color, chart_index, self)

    def show_hide_data_series(self, index):
        # Simply pass the function call to the chart itself
        plot_idx, data_idx = self.data_location[index]
        self.plots[plot_idx].show_hide_data_series(data_idx)

    def delete_data_series(self, index):
        # Function called when a data series is being deleted
        # First, decrement the indices of legends and plotted_data entries
        # to make sure they still match the arrays in the chart class
        for l in self.legends.controls:
            if l.index > index:
                l.index -= 1

        for dict in self.plotted_data:
            if dict["plot_index"] > index:
                dict["plot_index"] -= 1

        plot_idx, data_idx = self.data_location[index]
        for loc in self.data_location:
            if loc[0] == plot_idx:
                if loc[1] > data_idx:
                    loc[1] -= 1

        # Remove the entries for the series we're removing
        self.legends.controls.pop(index)
        self.plotted_data.pop(index)
        self.data_location.pop(index)

        # Finally, delete the series from the chart using its function
        # and decrement num_data_series to mark the removal
        self.plots[plot_idx].delete_data_series(data_idx)
        self.num_data_series -= 1
        self.num_series_per_plot[plot_idx] -= 1
        self.update()

    def add_data_series(self, e):
        # Function to add a new data series to the chart
        # Check if a valid color has been picked, default to CYAN otherwise
        if self.picked_color == None:
            self.picked_color = ft.colors.CYAN

        # Check if a PGN and a value within that PGN have been selected,
        # set error flag high if either of those requirements hasn't been met
        # and inform the user using the error text
        self.all_pgns_dropdown.error_text = ""
        self.data_to_display_dropdown.error_text = ""

        error = 0
        if self.all_pgns_dropdown.value in [None, ""]:
            self.all_pgns_dropdown.error_text = "Need to select an output"
            error = 1

        if self.data_to_display_dropdown.value in [None, ""]:
            self.data_to_display_dropdown.error_text = "Need to select data!"
            error = 1

        self.update()
        if error:  # Error present, can't add the data series
            return

        plot_idx = int(self.plot_num_select.value)

        name_str = self.data_to_display_dropdown.value
        pgn_str = self.all_pgns_dropdown.value

        # Get the signal's unit, format it nicely if it has a valid one
        unit_str = unit_dict[self.data_to_display_dropdown.value]
        if unit_str == "None":
            unit_str = ""
        else:
            unit_str = "\nUnit: " + unit_str

        # Add the new series to plotted_data to enable it to be updated by the CAN loop
        self.plotted_data.append({"output_name": self.all_pgns_dropdown.value, "data_name": self.data_to_display_dropdown.value, "plot_index": self.num_data_series, "chart_number": plot_idx})

        # Create a legend to view and control the series
        self.legends.controls.append(self.make_legend(name_str, f"{pgn_str}{unit_str}", self.picked_color, int(self.plot_num_select.value)))

        # Add the new series to the chart
        self.plots[plot_idx].add_data_series(self.picked_color)
        self.data_location.append([plot_idx, self.num_series_per_plot[plot_idx]])

        # Clear picked color, increment num_data_series
        self.picked_color = None
        self.num_data_series += 1
        self.num_series_per_plot[plot_idx] += 1
        self.update()

    def add_data(self, data, data_index):
        # Called from the CAN loop, just passes the call to the chart
        if self.start_time == 0:
            self.start_time = time.time()

        plot_idx, data_idx = self.data_location[data_index]
        self.plots[plot_idx].add_data(data, data_idx)

    def import_preset(self, config):
        while config["num_plots"] > len(self.charts.controls):
            self.add_plot(0)

        for x in config["plot_list"]:
            pgn = x["pgn"]
            plot_idx = x["plot_idx"]
            name_str = x["name_str"]
            subtitle = x["subtitle"]
            data_name = x["data_name"]
            color = x["color"]

            # Add the new series to plotted_data to enable it to be updated by the CAN loop
            self.plotted_data.append({"data_name": data_name, "plot_index": self.num_data_series, "chart_number": plot_idx})

            # Create a legend to view and control the series
            self.legends.controls.append(self.make_legend(name_str, subtitle, color, plot_idx))

            # Add the new series to the chart
            self.plots[plot_idx].add_data_series(color)
            self.data_location.append([plot_idx, self.num_series_per_plot[plot_idx]])

            # Increment num_data_series
            self.num_data_series += 1
            self.num_series_per_plot[plot_idx] += 1

        self.update()

    def export_preset(self):
        plot_list = []

        for idx, p in enumerate(self.plotted_data):
            l = self.legends.controls[idx]

            plot_list.append(
                {
                    "data_name": p["data_name"],
                    "plot_idx": p["chart_number"],
                    "name_str": l.title,
                    "subtitle": l.subtitle,
                    "color": l.icon_color,
                }
            )

        return len(self.charts.controls), plot_list
