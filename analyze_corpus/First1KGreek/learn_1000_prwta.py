import os
import xml.etree.ElementTree as ET
from collections import defaultdict
import json

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def clean_path(path):
    # Replace the path before 'data/' with './'
    return './' + path.split('/data/')[-1] if '/data/' in path else path

def analyze_div_types(root_dir):
    # Dictionary to store types and their subtypes with paths
    type_hierarchy = defaultdict(lambda: defaultdict(str))
    total_files = 0
    files_with_greek = 0

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

                    """# Check if file contains Greek
                        lang_usage = root.find(".//tei:langUsage", ns)
                        has_greek = False
                        if lang_usage is not None:
                        for lang in lang_usage.findall("tei:language", ns):
                            if lang.get('ident') == 'grc' and lang.text == 'Greek':
                                has_greek = True
                                files_with_greek += 1
                                break"""

                    #if has_greek:
                        # Find all div elements
                    for div in root.findall(".//tei:div", ns):
                        div_type = div.get('type', '')
                        div_subtype = div.get('subtype', '')
                        
                        if div_type and div_subtype:  # Only consider divs with both type and subtype
                            # Only store the path if we haven't seen this subtype for this type before
                            if not type_hierarchy[div_type][div_subtype]:
                                type_hierarchy[div_type][div_subtype] = clean_path(file_path)

                except ET.ParseError:
                    print(f"Error parsing file: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

    # Create JSON structure
    output_data = {
        "statistics": {
            "total_files": total_files,
            #"files_with_greek": files_with_greek
        },
        "types": {}
    }

    # Convert the defaultdict to regular dict structure
    for div_type in sorted(type_hierarchy.keys()):
        output_data["types"][div_type] = {
            "subtypes": {}
        }
        for subtype in sorted(type_hierarchy[div_type].keys()):
            output_data["types"][div_type]["subtypes"][subtype] = {
                "path": type_hierarchy[div_type][subtype]
            }

    # Write to JSON file
    with open('div_hierarchy.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    # Also print to console
    print(json.dumps(output_data, ensure_ascii=False, indent=2))

# Replace this with the actual path to your root directory
root_directory = "/home/fivos/Desktop/text_sources/OpenGreekAndLatin-First1KGreek-de360a3/data"
analyze_div_types(root_directory)