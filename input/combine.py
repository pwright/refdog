import os
import re

def collect_markdown_files(root_dir):
    """
    Collect all Markdown files recursively, with their relative paths.
    """
    md_files = []
    for root, _, files in os.walk(root_dir):
        for file in sorted(files):
            if file.endswith(".md"):
                relative_path = os.path.relpath(os.path.join(root, file), root_dir)
                md_files.append(relative_path)
    return sorted(md_files, key=lambda f: f.count(os.sep))  # Sort by directory depth

def adjust_image_paths(content, file_path, root_dir):
    """
    Adjust image references in <img> tags to be relative to the combined file's location.
    """
    def replace_img_src(match):
        img_path = match.group(1)  # The original src path
        absolute_path = os.path.normpath(os.path.join(os.path.dirname(file_path), img_path))
        relative_path = os.path.relpath(absolute_path, root_dir)  # Adjusted relative path
        return f'<img src="{relative_path}"'

    # Regex to find <img src="...">
    return re.sub(r'<img src="([^"]+)"', replace_img_src, content)

def create_combined_md(files, root_dir, output_file):
    """
    Combine Markdown files into one, adding headers and adjusting image paths.
    """
    with open(output_file, "w") as combined:
        for file in files:
            header = f"# Source: {file}\n\n"
            combined.write(header)
            with open(os.path.join(root_dir, file), "r") as md_file:
                content = md_file.read()
                adjusted_content = adjust_image_paths(content, file, root_dir)
                combined.write(adjusted_content)
            combined.write("\n\n---\n\n")  # Separator between files

if __name__ == "__main__":
    # Define root directory containing Markdown files
    root_dir = "./"  # Default to current directory
    output_file = "combined.md"

    # Collect and combine Markdown files
    markdown_files = collect_markdown_files(root_dir)
    create_combined_md(markdown_files, root_dir, output_file)

    print(f"Combined Markdown file created: {output_file}")
