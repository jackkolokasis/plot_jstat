#!/usr/bin/env python3

###################################################
#
# file: plot_heap_size.py
#
# @Author:   Iacovos G. Kolokasis
# @Version:  16-04-2024
# @email:    kolokasis@ics.forth.gr
#
# @brief: Plot the size of the young and old generation
# during execution
#
###################################################

import optparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import config

def kb_to_gb(size):
    return float(size)/1024/1024

# Parse input arguments
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-i", "--input", dest="input", metavar="FILE", help="Input file")
parser.add_option("-o", "--outputPath", metavar="PATH", dest="outputPath", default="output.svg", help="Output Path")
(options, args) = parser.parse_args()

young_gen_min = []
young_gen_max = []
young_gen_cur = []

old_gen_min = []
old_gen_max = []
old_gen_cur = []

# Open input file 
with open(options.input, 'r') as inputFile:
    # Initialize a flag to track whether the first line has been bypassed
    first_line_skipped = False

    # Iterate over each line in the file
    for line in inputFile.readlines():
        # Check if it's the first line
        if not first_line_skipped:
            # Set the flag to True to indicate that the first line has been bypassed
            first_line_skipped = True
            continue  # Skip processing this line and move to the next one
        
        # Split the line into individual columns based on whitespace
        columns = line.strip().split()

        young_gen_min.append(kb_to_gb(columns[0]))
        young_gen_max.append(kb_to_gb(columns[1]))
        young_gen_cur.append(kb_to_gb(columns[2]))
        
        old_gen_min.append(kb_to_gb(columns[6]))
        old_gen_max.append(kb_to_gb(columns[7]))
        old_gen_cur.append(kb_to_gb(columns[8]))

#------------------------------------------------------------------------------
# Young Generation Capacity
#------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=config.fullfigsize)

# Grid
plt.grid(True, linestyle='--', color='grey', zorder=0)

# Prepare x-axis data
time = range(1, len(young_gen_min) + 1)

plt.plot(time, young_gen_min, color=config.B_color_cycle[0],
         label='New Generation Minimum Capacity', zorder=2)
plt.plot(time, young_gen_max, color=config.B_color_cycle[1],
         label='New Generation Maximum Capacity', zorder=2)
plt.plot(time, young_gen_cur, color=config.B_color_cycle[3],
         label='New Generation Current Capacity', zorder=2)

# Axis name
plt.ylabel('Memory (GB)', ha="center")
plt.xlabel('Time (s)')

# Legend
plt.legend(loc='upper right', bbox_to_anchor=(1, 1.25), ncol=3)

# Save figure
plt.savefig('%s/young_gen.png' % options.outputPath, bbox_inches='tight')

#------------------------------------------------------------------------------
# Old Generation Capacity
#------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=config.fullfigsize)

# Grid
plt.grid(True, linestyle='--', color='grey', zorder=0)

# Prepare x-axis data
time = range(1, len(young_gen_min) + 1)

plt.plot(time, old_gen_min, color=config.B_color_cycle[0],
         label='Old Generation Minimum Capacity', zorder=2)
plt.plot(time, old_gen_max, color=config.B_color_cycle[1],
         label='Old Generation Maximum Capacity', zorder=2)
plt.plot(time, old_gen_cur, color=config.B_color_cycle[3],
         label='Old Generation Current Capacity', zorder=2)

# Axis name
plt.ylabel('Memory (GB)', ha="center")
plt.xlabel('Time (s)')

# Legend
plt.legend(loc='upper right', bbox_to_anchor=(1, 1.25), ncol=3)

# Save figure
plt.savefig('%s/old_gen.png' % options.outputPath, bbox_inches='tight')
