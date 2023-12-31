#! /bin/bash

# check if the script is run as root

if [ "$EUID" -ne 0 ]; then
	echo "Please run as root"
	exit
fi

CURRENT_DIR=$(pwd)
SERVICE_FILE=/etc/systemd/system/fan-control.service

if [ -f "$SERVICE_FILE" ]; then
	echo "Service already installed"
	echo "Do you want to reinstall it? (y/n)"
	read -r answer
	if [ "$answer" != "${answer#[Yy]}" ]; then
		echo "Reinstalling service"
	else
		echo "Aborting"
		exit
	fi
fi

UNIT_TEMPLATE="
[Unit]
Description=Fan Control Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $CURRENT_DIR/main.py
ExecStop=/usr/bin/python3 $CURRENT_DIR/main.py --stop
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"

echo "$UNIT_TEMPLATE" >$SERVICE_FILE

if [ $? -eq 0 ]; then
	echo "Service installed"
	systemctl daemon-reload
	systemctl enable fan-control.service
	systemctl start fan-control.service
else
	echo "Error while installing service"
fi
