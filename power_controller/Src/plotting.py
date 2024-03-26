import flet as ft
from math import ceil, floor
import time


# Class used to handle the chart itself. plot_page gives commands to this class,
# which then updates various parameters (axis ranges, what data is plotted...) accordingly
class Plotting:
    def __init__(self, page):
        self.sliding_window = False
        self.trimmed_flag = False
        self.num_data_series = 0  # Number of lines currently added

        self.raw_data = []  # 2d array of raw received data. Indexing: [series_index][x_val]
        self.trimmed_data = []  # 2d array of trimmed received data, trimmed to match sliding window
        self.data = []  # 2d array of LineChartData. Basically has all the values of one of the previous arrays
        self.series_max_y = []  # Each series' max y value, used to scale the y axis

        self.page = page

        self.small_y_axis_scaling = [10, 5, 4, 2, 1]

        self.chart = ft.LineChart(
            data_series=self.data,
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(interval=5, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1),
            vertical_grid_lines=ft.ChartGridLines(interval=5, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1),
            left_axis=ft.ChartAxis(
                show_labels=True,
                labels_size=45,
                labels_interval=10,
                title=ft.Text("Value"),
                title_size=20,
            ),
            bottom_axis=ft.ChartAxis(
                show_labels=True,
                labels_size=25,
                labels_interval=10,
                title=ft.Text("Time (s)"),
                title_size=20,
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
            min_y=0,
            max_y=50,
            min_x=0,
            max_x=50,
            baseline_x=0,
            expand=True,
            animate=25,
            interactive=True,
        )

    def toggle_slide(self):
        # Callback function to toggle sliding the chart window
        self.sliding_window = not self.sliding_window
        if self.sliding_window:
            self.trimmed_flag = True

    def toggle_rounded(self):
        # Callback function to toggle the curved property of all the LineChartData
        # Makes sure all lines have the same settings for consistency
        if self.num_data_series == 0:  # Prevent error when there is no data
            return

        master_curved = not self.data[0].curved
        for d in self.data:
            d.curved = master_curved

        self.chart.update()

    def toggle_animate(self):
        # Toggle whether the chart animations should happen
        self.chart.animate = 25 if self.chart.animate != 25 else 0

    def clear_data(self):
        # Clear all the data received, but keeps the current data series
        # Also resets the x axis
        for i in range(self.num_data_series):
            self.raw_data[i].clear()
            self.trimmed_data[i].clear()
            self.data[i].data_points.clear()

        self.chart.min_x = 0
        self.chart.max_x = 50
        self.chart.update()

    def add_data(self, val, data_index):
        # Function used to add data to the chart
        # data_index is the index of the data series

        x = time.time() - self.page.start_time  # x value based on time elapsed

        # Add the new data to the data arrays
        self.raw_data[data_index].append(ft.LineChartDataPoint(x, val))
        self.trimmed_data[data_index].append(ft.LineChartDataPoint(x, val))

        # Update the data points, as well as the chart's min_x value if necessary
        if self.sliding_window:
            self.data[data_index].data_points = self.trimmed_data[data_index]
        else:
            self.data[data_index].data_points = self.raw_data[data_index]
            self.chart.min_x = min(self.data[data_index].data_points[0].x, self.chart.min_x)

        if self.trimmed_flag:
            self.trimmed_flag = 0
            self.chart.min_x = self.chart.max_x - 50

            for i in range(self.num_data_series):
                self.trimmed_data[i] = [point for point in self.trimmed_data[i] if point.x >= self.chart.min_x]
                self.data[i].data_points = self.trimmed_data[i]

        # If we're about to go out of bounds on the x axis, increase max_x
        if x >= self.chart.max_x:
            while x >= self.chart.max_x:
                self.chart.max_x += 5

            # The window should be sliding, so update the minimum
            # As well as trimming all the data
            if self.sliding_window:
                self.chart.min_x = self.chart.max_x - 50
                # For all the data we're displaying, trim any values that would be outside the chart
                for i in range(self.num_data_series):
                    self.trimmed_data[i] = [point for point in self.trimmed_data[i] if point.x >= self.chart.min_x]
                    self.data[i].data_points = self.trimmed_data[i]

        # If the current series has a new max y value, store it
        if val > self.series_max_y[data_index]:
            self.series_max_y[data_index] = val

        # If the current series is visible and the value is above the current maximum, increase max_y
        if val > self.chart.max_y and self.data[data_index].visible:
            self.check_curr_max_y()

        if len(self.raw_data[data_index]) == 1:
            self.check_curr_max_y()

        self.check_curr_max_x()

        # Only update the chart if the current series is visible to avoid the chart moving when all series are hidden
        if self.data[data_index].visible:
            self.chart.update()

    def add_data_series(self, color):
        # Function used to add a new data series to the chart
        # Add entries in these arrays for the new series
        self.raw_data.append([])
        self.trimmed_data.append([])
        self.series_max_y.append(0)

        self.data.append(
            ft.LineChartData(
                self.raw_data[self.num_data_series],  # num_data_series will be the index of the new series
                stroke_width=5,
                color=color,
                curved=False,
                stroke_cap_round=True,
                prevent_curve_over_shooting=True,
            )
        )

        # Increment num_data_series to mark the new series
        self.num_data_series += 1
        self.check_curr_max_y()
        self.check_curr_max_x()
        self.chart.update()

    def check_curr_max_y(self):
        # Check the current max y value of all DISPLAYED series, update some y axis settings based on it
        max_y = 0
        for i in range(self.num_data_series):
            if self.data[i].visible and self.series_max_y[i] > max_y:
                max_y = self.series_max_y[i]

        if max_y == 0:  # Avoid hiding the chart completely if no series are being displayed
            max_y = 50

        # Edge cases for y < 10 and y < 25
        if max_y < 10:
            self.chart.max_y = 10
            self.chart.left_axis.labels_interval = 10 / self.small_y_axis_scaling[len(self.page.plots) - 1]
            self.chart.horizontal_grid_lines.interval = max(self.chart.left_axis.labels_interval / 2, 1)

        elif max_y < 25:
            self.chart.max_y = 25
            self.chart.left_axis.labels_interval = 25 / self.small_y_axis_scaling[len(self.page.plots) - 1]
            self.chart.horizontal_grid_lines.interval = self.chart.left_axis.labels_interval / 2

        # General case, treat everything in multiples of 50
        else:
            self.chart.max_y = ceil(max_y / 50) * 50
            self.chart.left_axis.labels_interval = self.chart.max_y / (6 - len(self.page.plots))
            self.chart.horizontal_grid_lines.interval = self.chart.left_axis.labels_interval / 2

    def check_curr_max_x(self):
        if self.chart.max_x - self.chart.min_x <= 50:
            self.chart.bottom_axis.labels_interval = 10
            self.chart.vertical_grid_lines.interval = 5

        else:
            self.chart.bottom_axis.labels_interval = 10 * floor((self.chart.max_x - self.chart.min_x) / 50)
            self.chart.vertical_grid_lines.interval = self.chart.bottom_axis.labels_interval / 2

    def show_hide_data_series(self, index):
        # Show/hide the series at an index, update the y axis
        self.data[index].visible = not self.data[index].visible
        self.check_curr_max_y()
        self.check_curr_max_x()
        self.chart.update()

    def delete_data_series(self, index):
        # Delete a data series from the chart
        # Pop its values from all arrays using its index
        self.raw_data.pop(index)
        self.trimmed_data.pop(index)
        self.data.pop(index)
        self.series_max_y.pop(index)

        # Decrement num_data_series to mark the removal, update the y axis
        self.num_data_series -= 1
        self.check_curr_max_y()
        self.check_curr_max_x()

        self.chart.update()

    def update_y_labels(self):
        self.check_curr_max_y()
