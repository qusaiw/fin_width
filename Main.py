#!/usr/bin/env python
# Written by Qusai Abu-Obaida
# 11-Jan-2017

import os
import re
import argparse
from collections import defaultdict
# \\parser
parser = argparse.ArgumentParser(description='Check if width and nfin values match in LVS files')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-all', help='test all cells inside "cells" folder', action="store_true")
group.add_argument('-list', help="test for provided list")
parser.add_argument('-path', help="path for the review folder", default=os.getcwd())
args = parser.parse_args()
# \\ parser outputs an object

mapping_dictionary = {}
errors_log = defaultdict(list)
cell_list = []
relative_path = args.path

if args.list:
    try:
        list_file = open(args.list, 'r')
        for i in list_file:
            i = i.strip()
            if len(i) != 0:
                cell_list.append(i)
        print cell_list
    except IOError:
        print "Error: \n" + args.list + " doesn't exist"
        quit()

else:
    if not os.path.isdir(relative_path + "/cells"):
        print"Error: \nCouldn't find \"cells\" directory"
        quit()
    cell_list = [name for name in os.listdir(relative_path + "/cells")]
print "\n%s cells found \n" % len(cell_list)
if os.path.isfile("fin_width.mapping"):
    os.system("cat fin_width.mapping")
    confirmation = (raw_input("Confirm values? y\\n:   ")).lower()
if not os.path.isfile("fin_width.mapping") or confirmation != "y":
    print "Please enter the width values in numbers only (ex: 0.98) or \"s\" to save"
    n = 0
    new_mapping_file = open("fin_width.mapping", 'w+')
    while True:
        n += 1
        new_input = raw_input("enter the width value for fin%d: " % n)
        if new_input.lower() == "s":
            break
        try:
            mapping_dictionary["fin%d" % n] = float(new_input)
            new_mapping_file.write("fin%d  " % n + str(float(new_input)) + '\n')
        except:
            print"invalid entry!"
            n -= 1

elif confirmation == 'y':
    mapping_file = open("fin_width.mapping", 'r')
    for line in mapping_file:
        line = line.strip()
        line = line.split()
        mapping_dictionary[line[0]] = float(line[1])

IS_TRANSISTOR = re.compile(r'(VB(P|N))|V(DD|SS)', re.I)
GET_W = re.compile(r' W *= *(\d*\.?\d+)', re.I)
GET_F = re.compile(r' n?fin *= *(\d+)', re.I)
for cell in cell_list:
    try:
        current_lvs = open(relative_path + "/cells/" + cell + "/" + cell + ".lvs", 'r')
        for line in current_lvs:
            if IS_TRANSISTOR.search(line) is not None and line[0].isalpha():
                try:
                    fin_file = int(GET_F.search(line).group(1))
                    width_file = float(GET_W.search(line).group(1))
                    if width_file != mapping_dictionary["fin%d" % fin_file]:
                        errors_log[cell].append(
                            line.split()[0].ljust(10, " ") + " nfin = " + str(fin_file) + " width = " + str(width_file))
                except:
                    errors_log[cell].append("Corrupted line:\n%s\n" % line)
    except IOError:
        errors_log[cell].append("No LVS file found.")
error_log = open("fin_width.log", 'w+')
if len(errors_log.keys()) == 0:
    print "Pass"
    error_log.write('pass')
    quit()
else:
    print str(len(errors_log.keys())) + " lvs failed"
    print "Check log at : " + os.getcwd() + "/fin_width.log"
for key, value in errors_log.items():
    error_log.write('*'*50 + "\n")
    error_log.write(key + "\n")
    error_log.write('*'*50 + "\n\n")
    for i in value:
        error_log.write(i)
        error_log.write("\n")
    error_log.write("\n")
error_log.write('*'*100)
error_log.write("\nFailed cells\n%s" % str(errors_log.keys()))
