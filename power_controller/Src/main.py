import flet as ft
from appbar import AppBarClass
from settings_page import SettingsPage
from plots_page import PlotsPage


def main(page: ft.Page):
    appbar = AppBarClass(page)
    page.settings_page = SettingsPage(page)
    page.plots_page = PlotsPage(page)

    page.title = "Power Controller"

    page.add(
        appbar,
        ft.Tabs(
            indicator_tab_size=True,
            expand=True,
            selected_index=0,
            tabs=[
                ft.Tab(text="Settings", content=page.settings_page, icon=ft.icons.SETTINGS_ROUNDED),
                ft.Tab("Charts", content=page.plots_page, icon=ft.icons.SSID_CHART_OUTLINED),
            ],
            scrollable=False,
        ),
    )

    page.update()


ft.app(target=main)
