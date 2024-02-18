from CAN.PCANBasic import *
from CAN.base_can_handler import AbstractCanHandler, CanMessage

bitrates = {
    "1M": PCAN_BAUD_1M,
    "500K": PCAN_BAUD_500K,
    "250K": PCAN_BAUD_250K,
    "125K": PCAN_BAUD_125K,
    "100K": PCAN_BAUD_100K,
    "83K": PCAN_BAUD_83K,
    "50K": PCAN_BAUD_50K,
    "10K": PCAN_BAUD_10K,
}

usb_channels = [
    PCAN_USBBUS1,
    PCAN_USBBUS2,
    PCAN_USBBUS3,
    PCAN_USBBUS4,
    PCAN_USBBUS5,
    PCAN_USBBUS6,
    PCAN_USBBUS7,
    PCAN_USBBUS8,
    PCAN_USBBUS9,
    PCAN_USBBUS10,
    PCAN_USBBUS11,
    PCAN_USBBUS12,
    PCAN_USBBUS13,
    PCAN_USBBUS14,
    PCAN_USBBUS15,
    PCAN_USBBUS16,
]


# This class has all the functions needed to interface with PEAK system's PCANBasic library
class PcanCanHandler(AbstractCanHandler):
    def __init__(self):
        super().__init__()

        self.pcan_basic = PCANBasic()

    # Check and return which can channels are available, store how many there are
    def load_channels(self):
        self.num_channels = 0
        channels = []
        for idx, channel in enumerate(usb_channels):
            if self.pcan_basic.GetValue(channel, PCAN_CHANNEL_CONDITION)[1] & PCAN_CHANNEL_AVAILABLE:
                channels.append(f"PCAN Channel {idx}")

        self.num_channels = len(channels)
        return channels

    # Open a channel, only if a channel and a bitrate have been selected
    def open_channel(self, channel, bitrate):
        if channel != None and bitrate != None and channel not in self.active_channels:
            self.active_channels[channel] = PCANBasic()

            if self.active_channels[channel].Initialize(usb_channels[channel], bitrates[bitrate]) == PCAN_ERROR_OK:
                self.num_open_channels = len(self.active_channels.keys())
                self.can_opened = True

            else:
                del self.active_channels[channel]

    # Close the channel
    def close_channel(self, channel):
        if channel in self.active_channels:
            self.active_channels[channel].Uninitialize(usb_channels[channel])
            del self.active_channels[channel]

            self.num_open_channels = len(self.active_channels.keys())
            self.can_opened = False  # ?

    # Read messages from the bus, returns an instance of CanMessage if one was received
    def read_message(self, i):
        if i < 0 or i >= self.num_open_channels:
            return -1

        key = list(self.active_channels.keys())[i]

        frame = self.active_channels[key].Read(usb_channels[key])[1]
        if frame.ID == 0:
            return CanMessage(0, [], 0)

        return CanMessage(frame.ID, frame.DATA[:], frame.LEN)
