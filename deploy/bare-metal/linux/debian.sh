#!/usr/bin/env bash

# Define system packages required for the project
pkgs=(build-essential python3 python3-dev python3-pip python3-venv)

# Add sudo to elevated commands when not running as root already
CMD_PREFIX=
if [ ! "$EUID" -eq 0 ]; then
  CMD_PREFIX=sudo
fi

# Install missing system packages
$CMD_PREFIX apt update
$CMD_PREFIX apt-get -y --ignore-missing install "${pkgs[@]}"

rm -fr venv
python3 -m venv venv
source venv/bin/activate

pip install -e .
