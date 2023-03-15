#!/usr/bin/env python3

import xml.etree.ElementTree as Et
import os

output_file = "merged.nessus"
mainTree = None
first = True

nessus_files = [file for file in os.listdir(".") if ".nessus" in file]

if not nessus_files:
    print("No Nessus files found. Aborting.")
    exit()

if os.path.exists(output_file):
    print(f"Output file {output_file} already exists. Aborting.")
    exit()

for file in nessus_files:
    try:
        with open(file, "r") as f:
            tree = Et.parse(f)
            if first:
                mainTree = tree
                report = mainTree.find("Report")
                first = False
            else:
                for element in tree.findall(".//ReportHost"):
                    report.append(element)
    except Exception as e:
        print(f"Error parsing {file}: {str(e)}")

if mainTree is not None:
    with open(output_file, "wb") as f:
        mainTree.write(f, encoding="utf-8", xml_declaration=True)

print(f"Done. Check your directory for {output_file}!")
