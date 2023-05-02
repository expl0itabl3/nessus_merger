#!/usr/bin/env python3

import os
import xml.etree.ElementTree as Et

# Pattern to match Nessus files
NESSUS_FILE_PATTERN = ".nessus"

# Name of the output file
OUTPUT_FILE_NAME = "merged.nessus"

# Find all Nessus files in the current directory
nessus_files = [file for file in os.listdir(".") if NESSUS_FILE_PATTERN in file]

# If no Nessus files are found, abort the script
if not nessus_files:
    print("No Nessus files found. Aborting.")
    exit()

# If the output file already exists, abort the script
if os.path.exists(OUTPUT_FILE_NAME):
    print(f"Output file {OUTPUT_FILE_NAME} already exists. Aborting.")
    exit()

# Parse each Nessus file and merge them into a single tree
main_tree = None
is_first = True
for file in nessus_files:
    try:
        with open(file, "r") as f:
            tree = Et.parse(f)
            if is_first:
                # If this is the first file, use its tree as the main tree
                main_tree = tree
                report = main_tree.find("Report")
                is_first = False
            else:
                # Otherwise, append the ReportHost elements to the main tree's Report element
                for element in tree.findall(".//ReportHost"):
                    report.append(element)
    except Exception as e:
        # If there is an error parsing a file, print an error message
        print(f"Error parsing {file}: {str(e)}")

# If there is a main tree, write it to the output file
if main_tree is not None:
    try:
        with open(OUTPUT_FILE_NAME, "wb") as f:
            main_tree.write(f, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        # If there is an error writing the output file, print an error message
        print(f"Error writing {OUTPUT_FILE_NAME}: {str(e)}")

# Finished message
print(f"Done. Check your directory for {OUTPUT_FILE_NAME}!")
