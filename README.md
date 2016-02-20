# sentrygun

Rogue AP killer

## Installation

To install sentrygun using git, first clone the git repo as follows:

	git clone https://github.com/s0lst1c3/sentrygun.git

Then install dependencies using pip:

	pip install -r pip.req

## Features

## Setup

Before using sentrygun, first create a whitelist file with the ssids and bssids of your
wireless access points. The whitelist file should have the following format:

	<ssid 0> <bssid 0>
	<ssid 1> <bssid 1>
	.
	.
	.
	<ssid n> <bssid n>

For example:

	FreeWifi 00:11:22:33:44:00
	FreeWifi 44:11:22:33:44:00
	FreeWifi 55:11:55:11:55:11

If you want sentrygun to send alerts to an email address or sms gateway, you can
add these configurations in the "SMTP settings" section of config.py.

## Usage

Sentrygun takes four command line arguments:

- __-i__ (required) - This flag is used to specify your wireless network interface.
- __--whitelist__ (required) - This flag should be set to the path of your whitelist file.
- __--evil-twin__ (optional) - Use this flag to have sentrygun protect against evil-twins
- __--karma__ (optional) - Use this flag to have sentrygun protect against karma attacks
- __--pacifist (option)__ - Tell sentrygun ___not___ to retaliate against rogue AP attacks.


To protect your wireless network against evil-twin attacks, use the following command:

	sentrygun --whitelist <path to whitelist file> -i <wifi interface> --evil-twin

To protect your wiresess network against Karma attacks:

	sentrygun --whitelist <path to whitelist file> -i <wifi interface> --karma

To protect your network against both Karma and evil twin attacks:

	sentrygun --whitelist <path to whitelist file> -i <wifi interface> --karma --evil-twin
