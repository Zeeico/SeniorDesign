import flet as ft
from CAN.kvaser_can_handler import KvaserCanHandler
from CAN.pcan_can_handler import PcanCanHandler

bitrate_dict = {
    "1 Mb/s": "1M",
    "500 kb/s": "500K",
    "250 kb/s": "250K",
    "125 kb/s": "125K",
    "100 kb/s": "100K",
}


class AppBarClass(ft.AppBar):
    def __init__(self, page):
        super().__init__()
        self.can_handlers = []
        self.num_of_channels = 0
        self.page = page
        self.can_params_flag = 0
        self.can_handler_offsets = []
        self.bitrate = ""
        self.handler_idx = 0

        self.selected_channel = ""
        self.connected = []

        # Connection indicator
        self.leading = ft.Icon(
            ft.icons.SIGNAL_CELLULAR_CONNECTED_NO_INTERNET_4_BAR_ROUNDED,
            size=40,
            color=ft.colors.RED,
            tooltip="Not connected to CAN",
        )

        self.title = ft.Text("Power Controller")
        self.center_title = True
        self.bgcolor = ft.colors.TERTIARY_CONTAINER

        self.load_channels_btn = ft.IconButton(
            ft.icons.REFRESH_ROUNDED,
            tooltip="Load Available CAN Channels",
            on_click=self.load_can_channels,
        )

        self.select_channel_btn = ft.PopupMenuButton(
            items=[],
            tooltip="Select CAN Channel",
            disabled=True,
            icon=ft.icons.FORMAT_LIST_BULLETED_ROUNDED,
        )

        self.select_bitrate_btn = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="1 Mb/s", on_click=self.set_can_bitrate),
                ft.PopupMenuItem(text="500 kb/s", on_click=self.set_can_bitrate),
                ft.PopupMenuItem(text="250 kb/s", on_click=self.set_can_bitrate),
                ft.PopupMenuItem(text="125 kb/s", on_click=self.set_can_bitrate),
                ft.PopupMenuItem(text="100 kb/s", on_click=self.set_can_bitrate),
            ],
            tooltip="Select Bitrate",
            disabled=True,
            icon=ft.icons.FORMAT_LIST_BULLETED_ROUNDED,
        )

        self.connect_btn = ft.IconButton(
            ft.icons.PLAY_ARROW_ROUNDED,
            tooltip="Connect to CAN",
            disabled=True,
            on_click=self.open_can_channel,
        )

        self.disconnect_btn = ft.PopupMenuButton(
            items=[],
            icon=ft.icons.STOP_ROUNDED,
            tooltip="Disconnect from CAN",
        )

        self.dark_mode_btn = ft.IconButton(
            ft.icons.WB_SUNNY_ROUNDED,
            tooltip="Switch to light mode",
            on_click=self.toggle_dark_mode,
        )

        self.actions = [
            self.load_channels_btn,
            self.select_channel_btn,
            self.select_bitrate_btn,
            self.connect_btn,
            self.disconnect_btn,
            self.dark_mode_btn,
        ]

    def did_mount(self):
        if self.page.platform_brightness == ft.ThemeMode.LIGHT:
            self.dark_mode_btn.icon = ft.icons.DARK_MODE_ROUNDED
            self.dark_mode_btn.tooltip = "Switch to dark mode"

        self.update()

    def platform_theme_changed(self):
        self.page.theme_mode = ft.ThemeMode.SYSTEM  # Update the theme to match the system setting

        # Set either light mode or dark mode
        if self.page.platform_brightness == ft.ThemeMode.LIGHT:
            self.dark_mode_btn.icon = ft.icons.DARK_MODE_ROUNDED
            self.dark_mode_btn.tooltip = "Switch to dark mode"

        else:
            self.dark_mode_btn.icon = ft.icons.WB_SUNNY_ROUNDED
            self.dark_mode_btn.tooltip = "Switch to light mode"

        self.page.update()

    def toggle_dark_mode(self, e):
        # Switch between dark and light mode based on current setting
        curr_theme = self.page.platform_brightness if self.page.theme_mode == ft.ThemeMode.SYSTEM else self.page.theme_mode

        # Switch button icon, tooltip, and page theme
        if curr_theme == ft.ThemeMode.DARK:
            e.control.icon = ft.icons.DARK_MODE_ROUNDED
            e.control.tooltip = "Switch to dark mode"
            self.page.theme_mode = ft.ThemeMode.LIGHT

        else:
            e.control.icon = ft.icons.WB_SUNNY_ROUNDED
            e.control.tooltip = "Switch to light mode"
            self.page.theme_mode = ft.ThemeMode.DARK

        self.page.update()

    # Function called when the refresh button is clicked
    def load_can_channels(self, e):
        self.select_channel_btn.items = []  # Clear the list of can channels in the next button over
        self.select_channel_btn.tooltip = "Select CAN Channel"

        # Determine how many CAN handlers have channels we can access
        self.can_handlers = []

        # Check PCAN channels
        try:
            pcan = PcanCanHandler()
            if len(pcan.load_channels()) != 0:
                self.can_handlers.append(pcan)
        except Exception:
            print("PCAN not available!")

        # Check Kvaser channels
        try:
            kvaser = KvaserCanHandler()
            if len(kvaser.load_channels()) != 0:
                self.can_handlers.append(kvaser)
        except Exception:
            print("Kvaser not available!")

        # Determine what channels are accessible in each can handler
        self.channels = []
        self.can_handler_offsets = []
        self.num_of_channels = 0

        for can_handler in self.can_handlers:
            new_channels = can_handler.load_channels()  # Get all the detected can channels from the CanHandler class

            self.can_handler_offsets.append(self.num_of_channels)  # Offset of the current handler's first channel
            self.num_of_channels += len(new_channels)  # Increment number of channels
            self.channels.extend(new_channels)  # Add new channels to channels list

        # Add each channel that isn't already opened to the pop up menu
        for ch in self.channels:
            if ch not in self.connected:
                self.select_channel_btn.items.append(ft.PopupMenuItem(text=ch, on_click=self.set_can_channel))

        # Update the tooltip
        e.control.tooltip = f"{self.num_of_channels} CAN channels detected!"

        # Allow the opening of the can channel and bitrate dropdowns
        self.select_channel_btn.disabled = False
        self.select_bitrate_btn.disabled = False

        self.update()

    # Called when a can channel is selected, sets the can channel in the matching can class
    def set_can_channel(self, e):
        # Save the selected channel and its index in all the channels
        self.selected_channel = e.control.text
        ch_index = self.channels.index(e.control.text)

        self.select_channel_btn.tooltip = f"Selected {self.selected_channel}"

        # Determine which can handler uses the current channel
        num_handlers = len(self.can_handler_offsets)
        i = 0
        while i < num_handlers:
            if i + 1 == num_handlers:  # Looking at last handler
                break

            if ch_index < self.can_handler_offsets[i + 1]:  # Looking at correct handler
                break

            i += 1

        can_handler = self.can_handlers[i]

        # Set the channel, mark the flag
        self.channel = ch_index - self.can_handler_offsets[i]
        self.handler_idx = i
        self.can_params_flag |= 1

        # If all parameters given, allow the user to start the can channel
        if self.can_params_flag == 3:
            self.connect_btn.disabled = False

        self.update()

    # Sets the can bitrate to be used when connecting
    def set_can_bitrate(self, e):
        # Set the can bitrate, mark the flag
        self.bitrate = bitrate_dict[e.control.text]
        self.select_bitrate_btn.tooltip = f"Selected {e.control.text}"
        self.can_params_flag |= 2

        # If all parameters given, allow the user to start the can channel
        if self.can_params_flag == 3:
            self.connect_btn.disabled = False

        self.update()

    # Called when the play button is clicked, tells the CanHandler class
    # to open the selected channel with the selected bitrate
    def open_can_channel(self, e):
        # Select the correct can handler, set the bitrate, open the channel
        can_handler = self.can_handlers[self.handler_idx]
        can_handler.open_channel(self.channel, self.bitrate)

        # If the channel opened successfully, update the leading icon
        if can_handler.can_opened == True:
            self.leading = ft.Icon(
                ft.icons.SIGNAL_CELLULAR_ALT_ROUNDED,
                size=40,
                color=ft.colors.GREEN,
                tooltip="Connected to CAN!",
            )

        self.connected.append(self.selected_channel)  # Mark the channel as connected

        self.can_params_flag = 0
        self.connect_btn.disabled = True

        # Remove it from the selectable channel options
        for option in self.select_channel_btn.items:
            if option.text == self.selected_channel:
                self.select_channel_btn.items.remove(option)
                break

        self.select_channel_btn.tooltip = "Select CAN Channel"
        self.select_bitrate_btn.tooltip = "Select Bitrate"

        # Add it to the disconnectable channel options
        self.disconnect_btn.items.append(ft.PopupMenuItem(text=f"{self.selected_channel}", on_click=self.close_can_channel))

        # Reset variables
        self.handler_idx = None
        self.selected_channel = None
        self.bitrate = ""
        self.update()

    # Used to disconnect from a can channel
    def close_can_channel(self, e):
        ch_index = self.channels.index(e.control.text)

        # Determine which can handler uses the channel we're disconnecting
        num_handlers = len(self.can_handler_offsets)
        i = 0
        while i < num_handlers:
            if i + 1 == num_handlers:
                break

            if ch_index < self.can_handler_offsets[i + 1]:
                break

            i += 1

        # TODO: Check if this code here closes the wrong channel when closing a channel after connecting a new adapter
        # Close the channel
        can_handler = self.can_handlers[i]
        can_handler.close_channel(ch_index - self.can_handler_offsets[i])

        # Remove it from the connected channels
        self.connected.remove(e.control.text)

        if len(self.connected) == 0:
            self.leading = ft.Icon(
                ft.icons.SIGNAL_CELLULAR_CONNECTED_NO_INTERNET_4_BAR_ROUNDED,
                size=40,
                color=ft.colors.RED,
                tooltip="Not connected to CAN",
            )

        # Remove it from the disconnectable channel options
        for option in self.disconnect_btn.items:
            if option.text == e.control.text:
                self.disconnect_btn.items.remove(option)
                break

        self.select_channel_btn.items = []
        self.select_channel_btn.tooltip = "Select CAN Channel"
        self.select_bitrate_btn.tooltip = "Select Bitrate"

        # Add it to the selectable channel options
        for ch in self.channels:
            if ch not in self.connected:
                self.select_channel_btn.items.append(ft.PopupMenuItem(text=ch, on_click=self.set_can_channel))

        self.update()
