import os
import xml.etree.ElementTree as ET
from collections import defaultdict
import json

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Define subtype groups
SUBTYPE_GROUPS = {
    'auctores': {
        "auctorm", "autorum", "auctores"
    },
    'chapter': {
        "chapter", "chap0ter", "chapterer", "chaptser", "chaspter", " chapter", "chapter1"
    },
    'section': {
        "section", "sction", "sectionn", "setion", " section"
    },
    'subsection': {
        "subsection", "subdsection", "subection"
    },
    'sentence': {
        "sentence", "setence"
    },
    #'miscellaneous': {
    #    "page", "1", "2", "3", "dramatispersonae", "trochees", "proode", "poem", "iambics", "part", "lyric", "line", "lines", "hypothesis", "haeresis", "fabula", "fable"
    #}
}

def clean_path(path):
    return './' + path.split('/data/')[-1] if '/data/' in path else path

def analyze_div_types(root_dir):
    # Dictionary to store counts for each subtype
    subtype_counts = defaultdict(int)
    group_totals = defaultdict(int)
    total_files = 0

    for first_level_dir in os.listdir(root_dir):
        first_level_path = os.path.join(root_dir, first_level_dir)
        if not os.path.isdir(first_level_path):
            continue
            
        for second_level_dir in os.listdir(first_level_path):
            second_level_path = os.path.join(first_level_path, second_level_dir)
            if not os.path.isdir(second_level_path):
                continue
                
            for filename in os.listdir(second_level_path):
                if filename.startswith("__") or not filename.endswith(".xml"):
                    continue
                    
                file_path = os.path.join(second_level_path, filename)
                total_files += 1
                
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    
                    # Find all div elements
                    for div in root.findall(".//tei:div", ns):
                        subtype = div.get('subtype', '')
                        if subtype:
                            subtype_counts[subtype] += 1
                            
                except ET.ParseError:
                    print(f"Error parsing file: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

    # Calculate group totals
    for group_name, subtypes in SUBTYPE_GROUPS.items():
        group_total = sum(subtype_counts[subtype] for subtype in subtypes)
        group_totals[group_name] = group_total

    # Print results in a concise format
    print(f"\nSubtype Counts and Group Totals ({total_files} files processed):")
    print("-" * 40)
    
    for group_name, subtypes in SUBTYPE_GROUPS.items():
        print(f"\n{group_name.upper()} GROUP (Total: {group_totals[group_name]})")
        print("-" * 20)
        for subtype in sorted(subtypes):
            count = subtype_counts[subtype]
            if count > 0:  # Only show subtypes that were found
                print(f"{subtype:15} : {count}")

    print("\nTotal files processed:", total_files)

# Replace this with the actual path to your root directory
root_directory = "/home/fivos/Desktop/First1KGreek/data"
analyze_div_types(root_directory)