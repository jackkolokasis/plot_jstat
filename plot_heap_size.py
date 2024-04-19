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

##
# Transform size
# @param size: The size in killobytes
#
# @return The size in gigabytes
def kb_to_gb(size):
    return float(size)/1024/1024

##
# Plot data about the capacity of the heap
# @param time: The time points
# @param min_data: The minimum capacity of the heap
# @param max_data: The maximum capacity of the heap
# @param cur_data: The current capacity of the heap
# @param label_prefix: The label prefix for the plot
# @param output_filename: The output filename
#
# return None
##
def plot_capacity_data(time, min_data, max_data, cur_data, label_prefix, output_filename):
    fig, ax = plt.subplots(figsize=config.fullfigsize)

    # Grid
    plt.grid(True, linestyle='--', color='grey', zorder=0)

    # Plot data
    plt.plot(time, min_data, color=config.B_color_cycle[0],
             label=f'{label_prefix} Minimum Capacity', zorder=2)
    plt.plot(time, max_data, color=config.B_color_cycle[1],
             label=f'{label_prefix} Maximum Capacity', zorder=2)
    plt.plot(time, cur_data, color=config.B_color_cycle[3],
             label=f'{label_prefix} Current Capacity', zorder=2)

    # Axis labels
    plt.ylabel('Memory (GB)', ha="center")
    plt.xlabel('Time (s)')

    # Legend
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1.25), ncol=3)

    # Save figure
    plt.savefig(output_filename, bbox_inches='tight')

##
# @brief Main function
#
# return
def main():
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

    time = range(1, len(young_gen_min) + 1)

    # Plot Young Generation Capacity
    plot_capacity_data(time, young_gen_min, young_gen_max, young_gen_cur,
                       'New Generation', f'{options.outputPath}/young_gen.png')

    # Plot Old Generation Capacity
    plot_capacity_data(time, old_gen_min, old_gen_max, old_gen_cur,
                       'Old Generation', f'{options.outputPath}/old_gen.png')

if __name__ == "__main__":
    main()
