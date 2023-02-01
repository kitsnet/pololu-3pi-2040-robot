# This program prints out some basic information about the system.

import sys
import gc
import os
import machine
import re
import pololu_3pi_plus_2040_robot as robot

display = robot.Display()

gc.collect()

match = re.search("MicroPython (v\S+?)-(g\S+)", sys.version)
version1 = match.group(1)
version2 = match.group(2)

file_stats = os.statvfs('//')
disk_free_kb = file_stats[0]*file_stats[3]/1024
disk_total_kb = file_stats[0]*file_stats[2]/1024
disk_used_kb = disk_total_kb-disk_free_kb

ram_free_kb = gc.mem_free()/1024
ram_used_kb = gc.mem_alloc()/1024
ram_total_kb = ram_free_kb + ram_used_kb

freq_mhz = machine.freq()/1000000

cpuid = machine.mem32[0xe0000000+0xed00]

display.fill(0)
display.text("CPU: {:x}".format(cpuid), 0, 0)
display.text("frq: {:.0f}MHz".format(freq_mhz), 0, 10)
display.text("mpy: "+version1, 0, 23)
display.text(version2, 0, 33)
display.text("dsk: {:.01f}k/{:.0f}M".format(disk_used_kb, disk_total_kb/1024), 0, 47)
display.text("RAM: {:.01f}k/{:.0f}k".format(ram_used_kb, ram_total_kb), 0, 57)
display.show()