# IP Change Notifier

## Purpose
Without a static IP service, ISP's may allocate a new IP address to your router anytime. If you have a VPN Server configured to access your local network like I do, the profiles that you have created are not useable after the IP change, and needs to be recreated. 

This application checks the public IP address every 30 minutes, and if it changes, the app sends an email to me containing the new IP address and freshly generated OpenVPN profile ready to connect to the local network.

## Usage
Run command ```python ipchecker.py <current-public-ip-address>```

## Environment
- Python Version: 3.9.2
- OS: Raspberry Pi OS 64-bit
- Device: A Raspberry Pi 4B with 4GB of RAM.
- PiVPN should be installed and configured.
- See requirements.txt too see the python libraries used in this project
