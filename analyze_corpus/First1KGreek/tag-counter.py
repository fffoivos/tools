import os
import xml.etree.ElementTree as ET
from collections import defaultdict

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def count_tag_variations(root_dir):
    tag_counts = defaultdict(int)
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
                    text_elem = root.find(".//tei:text", ns)
                    if text_elem is not None:
                        # Count all tags within text
                        for elem in text_elem.iter():
                            # Remove namespace from tag name
                            tag_name = elem.tag
                            if '}' in tag_name:
                                tag_name = tag_name.split('}')[1]
                            tag_counts[tag_name] += 1

                except ET.ParseError:
                    print(f"Error parsing file: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

    # Print results
    print(f"\nTotal XML files processed: {total_files}")
    print("\nTag counts within <text> element:")
    print("=================================")
    
    # Sort tags by count in descending order
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    
    for tag, count in sorted_tags:
        if tag != 'text':  # Skip the text tag itself
            print(f"<{tag}> : {count}")

# Replace this with the actual path to your root directory
root_directory = "/home/fivos/Desktop/text_sources/OpenGreekAndLatin-First1KGreek-de360a3/data"
count_tag_variations(root_directory)
