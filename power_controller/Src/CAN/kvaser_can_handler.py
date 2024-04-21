from canlib import canlib, Frame
from CAN.base_can_handler import AbstractCanHandler, CanMessage

# The bitrates canlib supports
bitrates = {
    "1M": canlib.Bitrate.BITRATE_1M,
    "500K": canlib.Bitrate.BITRATE_500K,
    "250K": canlib.Bitrate.BITRATE_250K,
    "125K": canlib.Bitrate.BITRATE_125K,
    "100K": canlib.Bitrate.BITRATE_100K,
    "83K": canlib.Bitrate.BITRATE_83K,
    "50K": canlib.Bitrate.BITRATE_50K,
    "10K": canlib.Bitrate.BITRATE_10K,
}


# This class has all the functions needed to interface with Kvaser's canlib library
class KvaserCanHandler(AbstractCanHandler):
    def __init__(self):
        super().__init__()

    # Check and return whichcan channels are available, store how many there are
    def load_channels(self):
        self.num_channels = canlib.enumerate_hardware()
        channels = []
        for ch in range(self.num_channels):
            chd = canlib.ChannelData(ch)
            channels.append(f"{chd.channel_name}")

        return channels

    # Open a channel, only if a channel and a bitrate have been selected
    def open_channel(self, channel, bitrate):
        if channel != None and bitrate != None and channel not in self.active_channels:
            self.active_channels[channel] = canlib.openChannel(channel=channel, bitrate=bitrates[bitrate], flags=canlib.canOPEN_ACCEPT_VIRTUAL)
            self.active_channels[channel].setBusOutputControl(canlib.canDRIVER_NORMAL)
            self.active_channels[channel].busOn()

            self.num_open_channels = len(self.active_channels.keys())
            self.can_opened = True

    # Close the channel
    def close_channel(self, channel):
        if channel in self.active_channels:
            self.active_channels[channel].busOff()
            self.active_channels[channel].close()
            del self.active_channels[channel]

            self.num_open_channels = len(self.active_channels.keys())
            self.can_opened = False  # ?

    # Read messages from the bus, returns an instance of CanMessage if one was received
    def read_message(self, i):
        if i < 0 or i >= self.num_open_channels:
            return -1

        key = list(self.active_channels.keys())[i]

        try:
            frame = self.active_channels[key].read(timeout=10)

        except (canlib.exceptions.CanGeneralError, canlib.CanNoMsg):
            return CanMessage(id=0, data=[], dlc=0)

        return CanMessage(id=frame.id, data=frame.data, dlc=frame.dlc)

    def send_message(self, i, id, data):
        if i < 0 or i >= self.num_open_channels:
            return -1

        key = list(self.active_channels.keys())[i]

        frame = Frame(id_=id, data=data)
        self.active_channels[key].write(frame)
