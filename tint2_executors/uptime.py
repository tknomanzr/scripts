#!/usr/bin/env python

from datetime import timedelta

with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])
    uptime_seconds = int(uptime_seconds)
    uptime_string = str(timedelta(seconds = uptime_seconds))

print("Uptime: " + uptime_string)
