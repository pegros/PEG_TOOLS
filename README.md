---
# SFPEG TOOLS
---

## Introduction

This repository contains a set of tools aiming at easing various adùministrative tasks on 
the Salesforce platform. They are mainly implemented in python and often leverage the
SFDX command line tool to interact with Salesforce Orgs.

## List of Tools

This package proposes the following **python** command line tools in the `/python` folder:
* **convertGeoJson.py** enables to initialise a CRM Analytics compatible GeoJson file out of 
a standard GeoJson one (slight generalisation of the tool available on [Trailhead](https://trailhead.salesforce.com/content/learn/projects/wave_charts_custom_map/wave_charts_custom_map_geojson)) 
* **generateDatesDataset.py** enables to generate a simple CRM Analytics dataset with all
dates between 1970 and 2070 to be used in date selectors in Dashboards.
* **getGlobalValueSets.py** enables to extract all values of all Global Value Sets from
an Org via SFDX and list them into a single CSV file.
* **loadApexDebugLogs.py** enables to extract all debug log files available on an Org
for a user connected via SFDX
* **mergeDataflows.py** and **mergeXmd.py** enable to merge reference data within 
dataflow and xmd CRM Analytics metadata files (to ensure e.g. that all augments with
an Account fetch the same set of fields and all picklist values have the same colors
in all datasets displaying a given field)

TO BE CONTINUED

## Technical Details

These tools have been implemented originally on a macOS system but portability to Windows
has been anticipated (but not tested) as much as possible.

Many rely on SFDX as a Salesforce data and metadata extraction tool.

Most support `--help` as parameter to provide explanations about how to use them. 