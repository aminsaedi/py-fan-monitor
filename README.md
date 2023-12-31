# py-fan-control

Using Python to control fan speed on a Raspberry Pi 5

This script will monitor the CPU temperature and fan speed level on a I2C character LCD display

It also allows use to manually set the fan speed level using two GPIO buttons

## Requirements

- Raspberry Pi 5
- I2C character LCD display
- 2x GPIO buttons
- `zerogpio` Python package

## Installation

To install the systemd service, run the following command:
```bash
sudo ./install-service.sh
```

You can also use it without the systemd service:
```bash
python3 main.py
```

