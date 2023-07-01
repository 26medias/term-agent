#!/bin/bash
device_id="C4:30:18:DD:79:16"
# Start the bluetoothctl interactive command
bluetoothctl <<EOF
connect $device_id
exit
EOF