#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 00:54:04 2024

@author: caiazzo
"""
import xml.etree.ElementTree as ET

# Function to extract all tags from the <instance> subtree
def extract_tags(element, tags_list):
    for child in element:
        # Append the tag without namespace
        tags_list.append(child.tag.split('}')[-1])  # Remove namespace if present
        extract_tags(child, tags_list)
        
# Function to recursively extract tags and their state (open/closed)
def analyze_tags(element, level=0):
    if list(element):  # If the element has children
        print(f"{'  ' * level}<{element.tag.split('}')[-1]}> - Group begin:")
        for child in element:
            analyze_tags(child, level + 1)
        print(f"{'  ' * level}</{element.tag.split('}')[-1]}> - Group end")
    else:  # If the element is self-closed
        print(f"{'  ' * level}<{element.tag.split('}')[-1]}/> - Question")


survey_dir = "/Users/caiazzo/HEDERA/NextCloud/HEDERA-TEAM/BUSINESS_DEVELOPMENT/PROJECTS/2023/2023_11-TripleJump-Oxfam/Component1-AlignmentEnvPerformance-ClimateRiskAssessment/Mali/4.LoanOfficersSurvey/webform/"
survey_xml = survey_dir + "resilience_climatique_mali.xml"

# Parse the XML file
tree = ET.parse(survey_xml)  # Replace with your file path
root = tree.getroot()

# Define the XML namespaces used in the file
namespace = {'h': 'http://www.w3.org/2002/xforms'}

# the "instance" tag contains the list of names (questions and groups)
instances = root.findall(".//h:instance", namespace)
# Analyze tags within the <instance> tag
analyze_tags(instances[0])#

# Find all <translation> elements: this tag contains question labels, hints, and list of choices
translations = root.findall(".//h:translation", namespace)
questions = []
# Extract the content under the <translation> tag
for translation in translations:
    for text in translation.findall(".//h:text", namespace):
        label_id = text.attrib.get('id', '')
        values = text.findall("h:value", namespace)  # Find all <value> tags

        for value in values:
            form_attr = value.attrib.get('form', None)  # Get 'form' attribute if it exists
            if form_attr:
                #print(f"Label ID: {label_id}, Value: {value.text}, Form: {form_attr}")
                # Extract the tag name (in this case 'energy_efficient_cookstoves') from label_id
                tag_name = label_id.split("/")[-1].split(":")[0]
                # Extract the image file name from the value (in this case 'energyefficientcooking.jpg')
                image_name = value.text.split("/")[-1]
                print(f"{tag_name} - {image_name}")

               
            else:
                tag_name = label_id.split("/")[-1].split(":")[0]
                #print(f"{tag_name}")
