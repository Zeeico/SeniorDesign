import flet as ft
from appbar import AppBarClass
from settings_page import SettingsPage
from plots_page import PlotsPage


def main(page: ft.Page):
    def window_event_handler(e):
        if e.data == "close":
            page.settings_page.running = False
            page.window_destroy()

    appbar = AppBarClass(page)
    page.settings_page = SettingsPage(page, appbar)
    page.plots_page = PlotsPage(page)

    page.title = "Power Controller"
    page.on_window_event = window_event_handler
    page.window_prevent_close = True

    page.add(
        appbar,
        ft.Tabs(
            indicator_tab_size=True,
            expand=True,
            selected_index=0,
            tabs=[
                ft.Tab(text="Settings", content=page.settings_page, icon=ft.icons.SETTINGS_ROUNDED),
                ft.Tab(text="Charts", content=page.plots_page, icon=ft.icons.SSID_CHART_OUTLINED),
            ],
            scrollable=False,
        ),
    )

    page.update()

    page.settings_page.run_can()


ft.app(target=main)
