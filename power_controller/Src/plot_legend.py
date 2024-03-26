import flet as ft


# Simple class used to show each data series being plotted as well
# as provide callback functions to show/hide and remove each data series
class PlotLegend(ft.UserControl):
    def __init__(self, index, title, subtitle, color, chart_index, plot_page):
        super().__init__()
        self.index = index  # Index in various arrays of data related to this legend
        self.icon_color = color  # Color of the show/hide icon, used to identify each line
        self.chart_index = chart_index

        # Text on the card
        self.title = title
        self.subtitle = subtitle

        self.plot_page = plot_page

    def build(self):
        self.legend = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(self.title),
                            subtitle=ft.Text(self.subtitle),
                            leading=ft.IconButton(ft.icons.VISIBILITY, icon_color=self.icon_color, on_click=self.show_hide_callback),
                            trailing=ft.IconButton(ft.icons.DELETE_ROUNDED, on_click=self.delete_callback),
                            content_padding=ft.padding.all(0),
                        ),
                    ]
                ),
            ),
            color=ft.colors.TERTIARY_CONTAINER,
            width=250,
        )
        return self.legend

    def show_hide_callback(self, e):
        # Show/hide the line using function in plotting.py, update the icon
        if e.control.icon == ft.icons.VISIBILITY:
            e.control.icon = ft.icons.VISIBILITY_OFF

        else:
            e.control.icon = ft.icons.VISIBILITY

        self.plot_page.show_hide_data_series(self.index)
        self.update()

    def delete_callback(self, e):
        # Mark the color as unused, delete the data series using the function in plot_page.py
        self.plot_page.delete_data_series(self.index)
