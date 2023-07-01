#!/bin/bash

device_id="4C:87:5D:CF:63:4B"

# Start the bluetoothctl interactive command
bluetoothctl <<EOF
connect $device_id
exit
EOF