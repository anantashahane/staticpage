import os
import sys
import shutil
from markdown_to_blocks import extract_title
from markdown_to_html_node import markdown_to_html_node

SOURCE = "./static/"
DESTINATION = "./docs/"
FROM_PATH = "./content/"
TEMPLATE_PATH = "./template.html"
DESTINATION_PATH = "./docs/"

def clean_destination(destination):
    for file in os.listdir(destination):
        file = os.path.join(destination, file)
        if os.path.isfile(file):
            print(f"Removing File: {file}")
            os.remove(file)
        else:
            clean_destination(file)
            print(f"Removing Directory: {file}")
            os.rmdir(file)

def copy_static_files(source, destination):
    for file in os.listdir(source):
        source_file = os.path.join(source, file)
        destination_file = os.path.join(destination, file)
        if os.path.isfile(source_file):
            print(f"Copying file {source_file} to {destination_file}")
            shutil.copy(source_file, destination_file)
        else:
            os.mkdir(destination_file)
            copy_static_files(source_file, destination_file)
            print(f"Copying directory {source_file} to {destination_file}")


def generate_page(from_path, template_path, dest_path, base_path):
    print("*** Generating Page ***")
    for file in os.listdir(from_path):
        file_location = os.path.join(from_path, file)
        md_string = ""
        template = ""
        if os.path.isfile(file_location):
            with open(file_location) as f:
                md_string = f.read()
            with open(template_path) as f:
                template = f.read()
            content = markdown_to_html_node(md_string).to_html()
            title = extract_title(md_string)
            file_content = template.replace("{{ Title }}", title)
            file_content = file_content.replace("{{ Content }}", content)
            file_content = file_content.replace('href="/', f'href="{base_path}')
            file_content = file_content.replace('src="/', f'src="{base_path}')
            dest_file = os.path.join(dest_path, "index.html")
            print(f"\tWriting {title}, to {dest_file}")
            with open(dest_file, "x") as wf:
                wf.write(file_content)
        else:
            dest = os.path.join(dest_path, file)
            os.mkdir(dest)
            generate_page(file_location, template_path, dest, base_path)



if __name__ == "__main__":
    base_path = "/"
    if len(sys.argv) == 2:
        base_path = sys.argv[1]
    print(f"Building with base path {base_path}")
    clean_destination(DESTINATION)
    copy_static_files(SOURCE, DESTINATION)
    generate_page(FROM_PATH, TEMPLATE_PATH, DESTINATION_PATH, base_path)
