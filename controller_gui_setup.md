# Power Controller GUI Setup

| Table of Contents                   |
| ----------------------------------- |
| [Downloads and installs](#downloads-and-installs) |
| [Running the code](#running-the-code)|

## Downloads and installs

### Install Steps

For each of these steps, the necessary download links and more detailed instructions can be found in the [Download Links and Commands](#download-links-and-commands) section below. 

#### Python

This is a Python project, so Python 3 is needed. When installing, make sure to add it to your path, otherwise you will encounter issues in the next steps.

#### Flet

Flet is the library we are using to let us control Flutter from Python. To install it, open your terminal of choice and run `pip install flet`.

#### Kvaser CANlib

Kvaser makes one of the supported CAN USB adapters in this project, which means we are using the Kvaser CANlib python library. First, install the [drivers](https://www.kvaser.com/download/?utm_source=software&utm_ean=7330130980013&utm_status=latest) and the [SDK](https://www.kvaser.com/download/?utm_source=software&utm_ean=7330130980150&utm_status=latest).

Once both of these are installed, open your terminal of choice and run `pip install canlib` to complete the install of the library.

#### PCANBasic

PEAK System makes the other supported CAN USB adapter in this project. To install the drivers for their adapters, download and install the PCAN driver for your operating system using [this executable](https://www.peak-system.com/Drivers.523.0.html?&L=1).

---

### Download Links and Commands

#### Windows

[Python](https://www.python.org/downloads/) (Click the yellow download button towards the top)

[Kvaser drivers](https://www.kvaser.com/download/?utm_source=software&utm_ean=7330130980013&utm_status=latest)

[Kvaser SDK](https://www.kvaser.com/download/?utm_source=software&utm_ean=7330130980150&utm_status=latest)

[PCAN drivers](https://www.peak-system.com/Drivers.523.0.html?&L=1) 

#### Linux (Debian-based distros)

##### Python

To install Python, run `sudo apt-get install python3 python3-pip`. You might also want to install `sudo apt-get install python-is-python3` for a little quality of life improvement.

##### Kvaser CANlib

[Kvaser drivers and SDK](https://www.kvaser.com/download/?utm_source=software&utm_ean=7330130980754&utm_status=latest). After downloading the archive, extract it. As you can see, it isn't compiled yet, it is up to us to compile it.

To install the necessary build tools, run `sudo apt-get install build-essential pkg-config`. You might also need to install the linux headers for your machine, which is done with `sudo apt-get install linux-headers-$(uname -r) `. 

Then, in your terminal, navigate to the linuxcan folder you extracted (should be similar to `cd ~/Downloads/linuxcan`). Run `make`, then `sudo make install`, and finally `sudo make load`.

This is a basic instruction of the Kvaser tools, more information about potential modifications can be found in the README within the `linuxcan` folder.

##### PCANBasic

The drivers should be included in the Linux kernel, but I don't have a good way of testing this so your mileage may vary.

#### MacOs

MacOs isn't formally supported for this project. Some aspects of it might work, but to my knowledge, neither of the necessary CAN libraries have MacOs versions. The project could technically be run in a VM.

---

## Running the code

I suggest running the code in an IDE (such as [VS Code](https://code.visualstudio.com/)), but it can also be run directly from a terminal.

To do so, navigate to the `Src` folder from the project root, and run `python main.py`.

