from abc import ABC, abstractmethod


class CanMessage:
    def __init__(self, id, data, dlc):
        self.id = id
        self.data = data
        self.dlc = dlc


class AbstractCanHandler(ABC):
    def __init__(self):
        self.num_channels = 0
        self.can_opened = False

        self.active_channels = {}
        self.num_open_channels = 0

    # Should check and return which can channels are available, and store how many there are
    @abstractmethod
    def load_channels(self):
        pass

    # Should open a channel, only if a channel and a bitrate have been selected
    @abstractmethod
    def open_channel(self, channel, bitrate):
        pass

    # Should close the specified channel
    @abstractmethod
    def close_channel(self, channel):
        pass

    # Should read the latest message from the bus, and return an instance of CanMessage if a message was received
    @abstractmethod
    def read_message(self, i):
        pass

    # Should send the message over CAN
    @abstractmethod
    def send_message(self,i, id, data):
        pass
