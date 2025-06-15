import os 
import glob
from tools import load_json, save_json
from markdown2 import markdown
from bs4 import BeautifulSoup

def convert_md_to_html(md_content):
    # Convert Markdown to HTML
    html_content = markdown(md_content)
    return html_content

def process_markdown_file_to_json(extracted_data_file = "jan_2025_course_data.json"):
    # Read the Markdown file
    try:
        all_md_files_path = glob.glob(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools-in-data-science-public', '*.md'))
    except Exception as e:
        print(f"Error finding Markdown files: {e}")
        return

    if not all_md_files_path:
        print("No Markdown files found in the specified directory.")
        return
    
    base_url = "https://tds.s-anand.net/#/"
    count = 1
    total_files = len(all_md_files_path)
    print(f"Total Markdown files found:  {total_files}") 

    
    all_contents = []
    for md_file_path in all_md_files_path:
        md_file = md_file_path.split(sep="\\")[-1]
        if md_file.startswith('_sidebar'):
            continue
        print(f"({count}/{total_files}) Processing {md_file}...")
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
            return
        else:
            html_content = convert_md_to_html(md_content)       # Convert Markdown to HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            text_elements = soup.get_text(separator=" ",strip=True)

            content = {
                "text" : text_elements,
                "url" : base_url + md_file.replace('.md', ''),
            }
            all_contents.append(content)
            count += 1
            print(f">>> Successfully Processed {md_file} .")
            data={
                "contents" : all_contents,
                "count" : len(all_contents)
            }
    save_json(extracted_data_file, data)     # save to json file

                                                    

if __name__ == "__main__":
    extracted_data_file = "jan_2025_course_data.json"
    process_markdown_file_to_json(extracted_data_file)
    print(f"Markdown files have been processed and saved to {extracted_data_file}.")
